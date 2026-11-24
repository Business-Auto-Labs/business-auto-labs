"""Small transactional services for tenant-safe CRM writes and local lead matching.

These helpers do not perform discovery, email validation, sending, or network calls.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit

from sqlalchemy import select
from sqlalchemy.orm import Session

from models import (
    Campaign, Country, DataSource, DoNotContact, EmailVerification, Lead,
    LeadAssignment, LeadContact, LeadNiche, LeadScore, LeadSource, LeadStatusHistory,
    Niche, Organization, OrganizationNiche, Region, City, Team, TeamMember, User,
    CRMActivity,
)
from normalization import (
    make_dedupe_key, normalize_business_name, normalize_contact_value, normalize_url,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _require_org(db: Session, organization_id: int) -> Organization:
    org = db.get(Organization, organization_id)
    if org is None:
        raise ValueError("Organization does not exist.")
    return org


def _validate_geography(
    db: Session, country_id: int, region_id: int | None, city_id: int | None
) -> None:
    if db.get(Country, country_id) is None:
        raise ValueError("Country does not exist.")
    region = db.get(Region, region_id) if region_id is not None else None
    if region_id is not None and region is None:
        raise ValueError("State or region does not exist.")
    if region is not None and region.country_id != country_id:
        raise ValueError("State or region must belong to the selected country.")
    city = db.get(City, city_id) if city_id is not None else None
    if city_id is not None and city is None:
        raise ValueError("City does not exist.")
    if city is not None:
        if region is None:
            raise ValueError("A city requires its state or region.")
        if city.region_id != region.id:
            raise ValueError("City must belong to the selected state or region.")


def _ensure_niche(db: Session, organization_id: int, niche_id: int) -> None:
    if db.get(Niche, niche_id) is None:
        raise ValueError("Niche does not exist.")
    link = db.scalar(select(OrganizationNiche).where(
        OrganizationNiche.organization_id == organization_id,
        OrganizationNiche.niche_id == niche_id,
    ))
    if link is None:
        db.add(OrganizationNiche(organization_id=organization_id, niche_id=niche_id))


def _ensure_lead_niche(db: Session, lead: Lead, niche_id: int) -> None:
    link = db.scalar(select(LeadNiche).where(
        LeadNiche.lead_id == lead.id,
        LeadNiche.niche_id == niche_id,
    ))
    if link is None:
        db.add(LeadNiche(
            lead_id=lead.id,
            niche_id=niche_id,
            is_primary=(lead.niche_id == niche_id),
        ))


def _add_source(
    db: Session, lead: Lead, source_url: str | None, data_source_id: int | None
) -> None:
    normalized = normalize_url(source_url)
    if not source_url or not normalized:
        return
    existing = db.scalar(select(LeadSource).where(
        LeadSource.lead_id == lead.id,
        LeadSource.normalized_url == normalized,
    ))
    if existing is None:
        db.add(LeadSource(
            lead_id=lead.id,
            data_source_id=data_source_id,
            source_url=source_url.strip(),
            normalized_url=normalized,
            is_original=(lead.original_source_url == source_url.strip()),
            discovered_at=_now(),
        ))
    if lead.original_source_url is None:
        lead.original_source_url = source_url.strip()


def _find_duplicate(
    db: Session,
    organization_id: int,
    business_name: str,
    country_id: int,
    region_id: int | None,
    city_id: int | None,
    dedupe_key: str,
    website: str | None,
    phone: str | None,
    email: str | None,
) -> Lead | None:
    found = db.scalar(select(Lead).where(
        Lead.organization_id == organization_id,
        Lead.dedupe_key == dedupe_key,
    ))
    if found is not None:
        return found

    strong = []
    if website:
        strong.append(("website", normalize_url(website)))
    if phone:
        strong.append(("phone", normalize_contact_value("phone", phone)))
    if email:
        strong.append(("email", normalize_contact_value("email", email)))

    # Contact matches only merge when they are in the same country. A caller can
    # enrich a legacy lead while retaining its original geography and source.
    for kind, value in strong:
        if not value:
            continue
        candidates = db.scalars(
            select(Lead)
            .join(LeadContact, LeadContact.lead_id == Lead.id)
            .where(
                Lead.organization_id == organization_id,
                Lead.country_id == country_id,
                LeadContact.contact_type == kind,
                LeadContact.normalized_value == value,
            )
        ).all()
        if candidates:
            return candidates[0]

    normalized_name = normalize_business_name(business_name)
    candidates = db.scalars(select(Lead).where(
        Lead.organization_id == organization_id,
        Lead.normalized_name == normalized_name,
        Lead.country_id == country_id,
    )).all()
    new_site = normalize_url(website)
    for candidate in candidates:
        if region_id is not None and candidate.region_id is not None and candidate.region_id != region_id:
            continue
        if city_id is not None and candidate.city_id is not None and candidate.city_id != city_id:
            continue
        old_site = normalize_url(candidate.website)
        if new_site and old_site and urlsplit(new_site).netloc != urlsplit(old_site).netloc:
            continue
        return candidate
    return None


def discover_or_merge_lead(
    db: Session,
    *,
    organization_id: int,
    niche_id: int,
    country_id: int,
    business_name: str,
    region_id: int | None = None,
    city_id: int | None = None,
    business_category: str | None = None,
    address: str | None = None,
    website: str | None = None,
    public_phone: str | None = None,
    public_email: str | None = None,
    source_url: str | None = None,
    source_name: str | None = None,
    data_source_id: int | None = None,
    score: float | None = None,
    notes: str | None = None,
    contacts: list[dict[str, Any]] | None = None,
) -> Lead:
    """Add or enrich an organization-scoped lead using normalized local matching.

    Existing first-source URLs and original niche links are retained. Missing
    input does not erase previously captured values.
    """
    _require_org(db, organization_id)
    _validate_geography(db, country_id, region_id, city_id)
    _ensure_niche(db, organization_id, niche_id)
    if not business_name.strip():
        raise ValueError("Business name is required.")

    norm_name = normalize_business_name(business_name)
    key = make_dedupe_key(
        business_name, country_id, region_id, city_id, website, public_phone, public_email
    )
    lead = _find_duplicate(
        db, organization_id, business_name, country_id, region_id, city_id,
        key, website, public_phone, public_email,
    )
    is_new = lead is None
    now = _now()

    if is_new:
        lead = Lead(
            organization_id=organization_id,
            business_name=business_name.strip(),
            niche_id=niche_id,
            country_id=country_id,
            region_id=region_id,
            city_id=city_id,
            original_source=source_name,
            original_source_url=source_url.strip() if source_url else None,
            data_source_id=data_source_id,
            discovered_at=now,
            crm_status="discovered",
            qualification_score=score or 0.0,
            normalized_name=norm_name,
            dedupe_key=key,
            business_category=business_category,
            address=address,
            website=website,
            public_phone=public_phone,
            public_email=public_email,
            notes=notes,
        )
        db.add(lead)
        db.flush()
    else:
        # Keep the first useful display name, first source, and first primary niche.
        lead.normalized_name = lead.normalized_name or norm_name
        lead.dedupe_key = key
        if not lead.business_category and business_category:
            lead.business_category = business_category
        if not lead.address and address:
            lead.address = address
        if not lead.website and website:
            lead.website = website
        if not lead.public_phone and public_phone:
            lead.public_phone = public_phone
        if not lead.public_email and public_email:
            lead.public_email = public_email
        if not lead.notes and notes:
            lead.notes = notes
        if lead.data_source_id is None and data_source_id is not None:
            lead.data_source_id = data_source_id
        if lead.original_source is None and source_name:
            lead.original_source = source_name
        if lead.region_id is None and region_id is not None:
            lead.region_id = region_id
        if lead.city_id is None and city_id is not None:
            lead.city_id = city_id

    _ensure_lead_niche(db, lead, niche_id)
    _add_source(db, lead, source_url, data_source_id)

    contact_inputs = list(contacts or [])
    if public_email:
        contact_inputs.append({"contact_type": "email", "value": public_email, "is_primary": True})
    if public_phone:
        contact_inputs.append({"contact_type": "phone", "value": public_phone, "is_primary": True})
    if website:
        contact_inputs.append({"contact_type": "website", "value": website, "is_primary": True})

    for item in contact_inputs:
        kind = str(item.get("contact_type", "")).strip().casefold()
        value = str(item.get("value", "")).strip()
        if not kind or not value:
            continue
        normalized = normalize_contact_value(kind, value)
        existing = db.scalar(select(LeadContact).where(
            LeadContact.lead_id == lead.id,
            LeadContact.contact_type == kind,
            LeadContact.normalized_value == normalized,
        ))
        if existing is None:
            db.add(LeadContact(
                lead_id=lead.id,
                contact_type=kind,
                value=value,
                normalized_value=normalized,
                is_primary=bool(item.get("is_primary", False)),
                is_public=bool(item.get("is_public", True)),
            ))

    if score is not None and (is_new or lead.qualification_score != score):
        lead.qualification_score = score
        db.add(LeadScore(
            lead=lead,
            score=score,
            score_type="qualification",
            factors={},
            notes="Captured during lead discovery or enrichment.",
        ))

    db.flush()
    return lead


def change_lead_status(
    db: Session,
    *,
    organization_id: int,
    lead_id: int,
    to_status: str,
    actor_user_id: int,
    note: str | None = None,
) -> Lead:
    lead = db.scalar(select(Lead).where(
        Lead.id == lead_id, Lead.organization_id == organization_id
    ))
    if lead is None:
        raise ValueError("Lead does not exist in this organization.")
    actor = db.get(User, actor_user_id)
    if actor is None or actor.organization_id != organization_id:
        raise ValueError("Actor must belong to the lead's organization.")
    status = to_status.strip().casefold()
    if not status:
        raise ValueError("Lead status cannot be empty.")
    if lead.crm_status == status:
        return lead

    old_status = lead.crm_status
    lead.crm_status = status
    db.add(LeadStatusHistory(
        lead=lead,
        actor_user_id=actor_user_id,
        from_status=old_status,
        to_status=status,
        note=note,
    ))
    db.add(CRMActivity(
        lead=lead,
        user_id=actor_user_id,
        activity_type="status_change",
        details=note or f"Status changed from {old_status} to {status}.",
    ))
    db.flush()
    return lead


def assign_lead(
    db: Session,
    *,
    organization_id: int,
    lead_id: int,
    user_id: int,
    team_id: int | None = None,
    assigned_by_user_id: int | None = None,
) -> LeadAssignment:
    lead = db.scalar(select(Lead).where(
        Lead.id == lead_id, Lead.organization_id == organization_id
    ))
    user = db.get(User, user_id)
    if lead is None or user is None or user.organization_id != organization_id:
        raise ValueError("Lead and assigned team member must belong to the organization.")
    if team_id is not None:
        team = db.get(Team, team_id)
        member = db.scalar(select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user_id,
            TeamMember.is_active.is_(True),
        ))
        if team is None or team.organization_id != organization_id or member is None:
            raise ValueError("Assigned member must be active in the selected organization team.")
    if assigned_by_user_id is not None:
        assigner = db.get(User, assigned_by_user_id)
        if assigner is None or assigner.organization_id != organization_id:
            raise ValueError("Assigning user must belong to the organization.")

    now = _now()
    current = db.scalars(select(LeadAssignment).where(
        LeadAssignment.lead_id == lead_id,
        LeadAssignment.is_current.is_(True),
    )).all()
    for item in current:
        item.is_current = False
        item.ended_at = now

    assignment = db.scalar(select(LeadAssignment).where(
        LeadAssignment.lead_id == lead_id,
        LeadAssignment.user_id == user_id,
    ))
    if assignment is None:
        assignment = LeadAssignment(
            lead_id=lead_id,
            user_id=user_id,
            team_id=team_id,
            assigned_by_user_id=assigned_by_user_id,
            assigned_at=now,
            is_current=True,
        )
        db.add(assignment)
    else:
        assignment.team_id = team_id
        assignment.assigned_by_user_id = assigned_by_user_id
        assignment.assigned_at = now
        assignment.ended_at = None
        assignment.is_current = True
    lead.assigned_to_user_id = user_id
    db.flush()
    return assignment


def record_email_validation(
    db: Session,
    *,
    lead_contact_id: int,
    status: str,
    validation_method: str = "manual",
    result_details: str | None = None,
) -> EmailVerification:
    contact = db.get(LeadContact, lead_contact_id)
    if contact is None or contact.contact_type.casefold() != "email":
        raise ValueError("Email validation history requires an email contact.")
    normalized_status = status.strip().casefold()
    if normalized_status not in {"valid", "invalid", "risky", "unknown", "unverified"}:
        raise ValueError("Unsupported email validation status.")
    method = validation_method.strip().casefold()
    if method not in {"manual", "syntax", "imported"}:
        raise ValueError("Validation method must be manual, syntax, or imported.")
    result = EmailVerification(
        lead_contact_id=lead_contact_id,
        status=normalized_status,
        validation_method=method,
        result_details=result_details,
        verified_at=_now(),
    )
    db.add(result)
    if contact.is_primary or normalize_contact_value("email", contact.value) == normalize_contact_value("email", contact.lead.public_email):
        contact.lead.email_validation_status = normalized_status
    db.flush()
    return result


def record_do_not_contact(
    db: Session,
    *,
    organization_id: int,
    value: str,
    reason: str,
    contact_type: str = "email",
    lead_id: int | None = None,
    lead_contact_id: int | None = None,
    created_by_user_id: int | None = None,
) -> DoNotContact:
    _require_org(db, organization_id)
    lead = db.get(Lead, lead_id) if lead_id is not None else None
    if lead_id is not None and (lead is None or lead.organization_id != organization_id):
        raise ValueError("Lead must belong to the selected organization.")
    contact = db.get(LeadContact, lead_contact_id) if lead_contact_id is not None else None
    if lead_contact_id is not None and contact is None:
        raise ValueError("Contact does not exist.")
    if contact is not None:
        if contact.lead.organization_id != organization_id:
            raise ValueError("Contact must belong to the selected organization.")
        if lead_id is not None and contact.lead_id != lead_id:
            raise ValueError("Contact must belong to the selected lead.")
        lead_id = contact.lead_id
    if created_by_user_id is not None:
        actor = db.get(User, created_by_user_id)
        if actor is None or actor.organization_id != organization_id:
            raise ValueError("Creating user must belong to the selected organization.")
    normalized = normalize_contact_value(contact_type, value)
    if not normalized:
        raise ValueError("A value to suppress is required.")
    existing = db.scalar(select(DoNotContact).where(
        DoNotContact.organization_id == organization_id,
        DoNotContact.normalized_value == normalized,
    ))
    if existing:
        return existing
    row = DoNotContact(
        organization_id=organization_id,
        lead_id=lead_id,
        lead_contact_id=lead_contact_id,
        value=value.strip(),
        normalized_value=normalized,
        reason=reason.strip(),
        created_by_user_id=created_by_user_id,
    )
    db.add(row)
    db.flush()
    return row
