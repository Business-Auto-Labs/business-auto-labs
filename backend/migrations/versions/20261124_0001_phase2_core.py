"""Initial Phase 2 schema and additive adoption of the Phase 1 prototype."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect, text

import models
from database import Base
from normalization import make_dedupe_key, normalize_business_name, normalize_contact_value, normalize_url


revision = "20261124_0001"
down_revision = None
branch_labels = None
depends_on = None


def _additive_columns() -> dict[str, list[sa.Column]]:
    def fk(target, name, ondelete=None):
        return sa.ForeignKey(target, name=name, ondelete=ondelete)
    return {
        "users": [
            sa.Column("organization_id", sa.Integer(), fk("organizations.id", "fk_users_organization", ondelete="SET NULL"), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "niches": [
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "countries": [
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "regions": [
            sa.Column("region_type", sa.String(40), server_default="state_or_region", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "cities": [
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "data_sources": [
            sa.Column("source_kind", sa.String(40), server_default="other", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "scraping_jobs": [
            sa.Column("organization_id", sa.Integer(), fk("organizations.id", "fk_scraping_jobs_organization", ondelete="SET NULL"), nullable=True),
            sa.Column("search_configuration_id", sa.Integer(), fk("search_configurations.id", "fk_scraping_jobs_search_configuration", ondelete="SET NULL"), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("result_summary", sa.Text(), nullable=True),
        ],
        "leads": [
            sa.Column("organization_id", sa.Integer(), fk("organizations.id", "fk_leads_organization", ondelete="SET NULL"), nullable=True),
            sa.Column("business_category", sa.String(160), nullable=True),
            sa.Column("address", sa.Text(), nullable=True),
            sa.Column("website", sa.String(512), nullable=True),
            sa.Column("public_phone", sa.String(80), nullable=True),
            sa.Column("public_email", sa.String(320), nullable=True),
            sa.Column("email_validation_status", sa.String(30), server_default="unknown", nullable=False),
            sa.Column("original_source", sa.String(120), nullable=True),
            sa.Column("discovered_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("normalized_name", sa.String(255), nullable=True),
            sa.Column("dedupe_key", sa.String(64), nullable=True),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("assigned_to_user_id", sa.Integer(), fk("users.id", "fk_leads_assigned_user", ondelete="SET NULL"), nullable=True),
        ],
        "lead_contacts": [
            sa.Column("normalized_value", sa.String(512), nullable=True),
            sa.Column("is_public", sa.Boolean(), server_default=sa.text("1"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "email_verifications": [
            sa.Column("validation_method", sa.String(40), server_default="manual", nullable=False),
            sa.Column("result_details", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "lead_assignments": [
            sa.Column("team_id", sa.Integer(), fk("teams.id", "fk_lead_assignments_team", ondelete="SET NULL"), nullable=True),
            sa.Column("assigned_by_user_id", sa.Integer(), fk("users.id", "fk_lead_assignments_assigned_by", ondelete="SET NULL"), nullable=True),
            sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("is_current", sa.Boolean(), server_default=sa.text("1"), nullable=False),
        ],
        "follow_up_reminders": [
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "campaigns": [
            sa.Column("organization_id", sa.Integer(), fk("organizations.id", "fk_campaigns_organization", ondelete="SET NULL"), nullable=True),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
        "suppression_records": [
            sa.Column("organization_id", sa.Integer(), fk("organizations.id", "fk_suppression_records_organization", ondelete="SET NULL"), nullable=True),
            sa.Column("normalized_value", sa.String(255), nullable=True),
            sa.Column("suppression_type", sa.String(30), server_default="email", nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        ],
    }


def _add_missing_columns(bind) -> None:
    existing_tables = set(inspect(bind).get_table_names())
    for table_name, definitions in _additive_columns().items():
        if table_name not in existing_tables:
            continue
        present = {column["name"] for column in inspect(bind).get_columns(table_name)}
        missing = [column for column in definitions if column.name not in present]
        if missing:
            with op.batch_alter_table(table_name) as batch:
                for column in missing:
                    batch.add_column(column)


def _as_datetime(value):
    if isinstance(value, datetime):
        return value
    if not value:
        return datetime.now(timezone.utc).replace(tzinfo=None)
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return parsed.astimezone(timezone.utc).replace(tzinfo=None) if parsed.tzinfo else parsed


def _backfill_legacy_data(bind) -> None:
    tables = set(inspect(bind).get_table_names())
    if "leads" not in tables:
        return
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat(sep=" ")

    leads = bind.execute(text(
        "SELECT id, business_name, niche_id, country_id, region_id, city_id, "
        "original_source_url, data_source_id, created_at, qualification_score, "
        "organization_id FROM leads ORDER BY id"
    )).mappings().all()

    # Keep each original lead and its primary niche/source while introducing
    # additive multi-niche and multi-source links.
    lead_niches = Base.metadata.tables["lead_niches"]
    lead_sources = Base.metadata.tables["lead_sources"]
    lead_scores = Base.metadata.tables["lead_scores"]
    for row in leads:
        exists = bind.execute(text(
            "SELECT 1 FROM lead_niches WHERE lead_id=:lead AND niche_id=:niche"
        ), {"lead": row["id"], "niche": row["niche_id"]}).first()
        if not exists:
            bind.execute(lead_niches.insert().values(
                lead_id=row["id"], niche_id=row["niche_id"], is_primary=True, added_at=_as_datetime(row["created_at"]),
            ))

        source_url = row["original_source_url"]
        normalized_url = normalize_url(source_url)
        if source_url and normalized_url:
            exists = bind.execute(text(
                "SELECT 1 FROM lead_sources WHERE lead_id=:lead AND normalized_url=:url"
            ), {"lead": row["id"], "url": normalized_url}).first()
            if not exists:
                bind.execute(lead_sources.insert().values(
                    lead_id=row["id"], data_source_id=row["data_source_id"],
                    source_url=source_url, normalized_url=normalized_url,
                    is_original=True, discovered_at=_as_datetime(row["created_at"]),
                    created_at=_as_datetime(row["created_at"]), updated_at=_as_datetime(row["created_at"]),
                ))

        # Avoid inventing historical events when the old schema has no score history.
        score = row["qualification_score"]
        if score is not None:
            exists = bind.execute(text(
                "SELECT 1 FROM lead_scores WHERE lead_id=:lead"
            ), {"lead": row["id"]}).first()
            if not exists:
                bind.execute(lead_scores.insert().values(
                    lead_id=row["id"], score=score, score_type="qualification",
                    factors={}, notes="Initial score carried forward during Phase 2 migration.",
                    created_at=_as_datetime(row["created_at"]),
                ))

        bind.execute(text(
            "UPDATE leads SET normalized_name=:name, discovered_at=COALESCE(discovered_at, created_at) "
            "WHERE id=:id"
        ), {"name": normalize_business_name(row["business_name"]), "id": row["id"]})

    if "lead_contacts" in tables:
        contacts = bind.execute(text(
            "SELECT id, lead_id, contact_type, value FROM lead_contacts ORDER BY id"
        )).mappings().all()
        normalized_rows = []
        counts = Counter()
        for row in contacts:
            norm = normalize_contact_value(row["contact_type"], row["value"])
            normalized_rows.append((row["id"], row["lead_id"], row["contact_type"], norm))
            counts[(row["lead_id"], row["contact_type"], norm)] += 1
        for contact_id, lead_id, kind, norm in normalized_rows:
            # Duplicates are retained; a null normalized value avoids making the
            # new uniqueness index discard or alter historical contact records.
            value = norm if counts[(lead_id, kind, norm)] == 1 else None
            bind.execute(text(
                "UPDATE lead_contacts SET normalized_value=:value WHERE id=:id"
            ), {"value": value, "id": contact_id})

        for row in leads:
            lead_id = row["id"]
            for kind, column in (("email", "public_email"), ("phone", "public_phone"), ("website", "website")):
                contact = bind.execute(text(
                    "SELECT value FROM lead_contacts WHERE lead_id=:lead AND lower(contact_type)=:kind "
                    "ORDER BY is_primary DESC, id ASC LIMIT 1"
                ), {"lead": lead_id, "kind": kind}).first()
                if contact and contact[0]:
                    bind.execute(text(
                        f"UPDATE leads SET {column}=COALESCE({column}, :value) WHERE id=:id"
                    ), {"value": contact[0], "id": lead_id})

    # Migrate an existing assignment into the current-owner pointer without
    # deleting or rewriting its assignment history.
    if "lead_assignments" in tables:
        assignments = bind.execute(text(
            "SELECT id, lead_id, user_id, assigned_at FROM lead_assignments ORDER BY lead_id, assigned_at, id"
        )).mappings().all()
        latest = {}
        for row in assignments:
            latest[row["lead_id"]] = row
            bind.execute(text("UPDATE lead_assignments SET is_current=0 WHERE id=:id"), {"id": row["id"]})
        for lead_id, row in latest.items():
            bind.execute(text(
                "UPDATE lead_assignments SET is_current=1 WHERE id=:id"
            ), {"id": row["id"]})
            bind.execute(text(
                "UPDATE leads SET assigned_to_user_id=:user WHERE id=:lead"
            ), {"user": row["user_id"], "lead": lead_id})

    # Backfill normalized suppression values only where they remain unique.
    if "suppression_records" in tables:
        rows = bind.execute(text("SELECT id, value FROM suppression_records ORDER BY id")).mappings().all()
        norms = [(r["id"], normalize_contact_value("email", r["value"])) for r in rows]
        counts = Counter(value for _, value in norms)
        for row_id, value in norms:
            bind.execute(text(
                "UPDATE suppression_records SET normalized_value=:value WHERE id=:id"
            ), {"value": value if counts[value] == 1 else None, "id": row_id})

    # Fingerprints are scoped to organizations. Legacy rows intentionally keep
    # organization_id NULL until a real organization mapping is provided.
    if "organization_id" in {c["name"] for c in inspect(bind).get_columns("leads")}:
        rows = bind.execute(text(
            "SELECT id, organization_id, business_name, country_id, region_id, city_id, website, public_phone, public_email "
            "FROM leads WHERE organization_id IS NOT NULL"
        )).mappings().all()
        generated = []
        counts = Counter()
        for row in rows:
            key = make_dedupe_key(
                row["business_name"], row["country_id"], row["region_id"], row["city_id"],
                row["website"], row["public_phone"], row["public_email"],
            )
            generated.append((row["id"], row["organization_id"], key))
            counts[(row["organization_id"], key)] += 1
        for lead_id, org_id, key in generated:
            bind.execute(text(
                "UPDATE leads SET dedupe_key=:key WHERE id=:id"
            ), {"key": key if counts[(org_id, key)] == 1 else None, "id": lead_id})


def _create_missing_indexes(bind) -> None:
    inspector = inspect(bind)
    tables = set(inspector.get_table_names())
    for table in Base.metadata.sorted_tables:
        if table.name not in tables:
            continue
        columns = {column["name"] for column in inspect(bind).get_columns(table.name)}
        existing_names = {index["name"] for index in inspect(bind).get_indexes(table.name)}
        for index in table.indexes:
            if index.name in existing_names:
                continue
            if all(column.name in columns for column in index.columns):
                index.create(bind=bind, checkfirst=True)


def upgrade() -> None:
    bind = op.get_bind()
    # For an empty DB create the complete Phase 2 schema. For the unversioned
    # Phase 1 prototype, this creates only new tables; existing tables are kept.
    Base.metadata.create_all(bind=bind, checkfirst=True)
    _add_missing_columns(bind)
    _backfill_legacy_data(bind)
    _create_missing_indexes(bind)


def downgrade() -> None:
    raise RuntimeError(
        "Phase 2 migration is intentionally forward-only: downgrading could delete legacy or CRM data. "
        "Restore a verified database backup to reverse it."
    )
