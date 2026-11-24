"""Relational CRM models. Optional organization links preserve unmapped legacy rows."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean, CheckConstraint, Float, ForeignKey, Index, JSON,
    String, Text, UniqueConstraint, text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, TimestampMixin, UTCDateTime, utcnow


class Organization(TimestampMixin, Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    timezone: Mapped[str] = mapped_column(String(80), default="UTC", nullable=False)

    users: Mapped[list["User"]] = relationship(back_populates="organization")
    teams: Mapped[list["Team"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    niche_links: Mapped[list["OrganizationNiche"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
    search_configurations: Mapped[list["SearchConfiguration"]] = relationship(back_populates="organization")
    leads: Mapped[list["Lead"]] = relationship(back_populates="organization")
    campaigns: Mapped[list["Campaign"]] = relationship(back_populates="organization")


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="sales_rep", nullable=False)

    organization: Mapped["Organization | None"] = relationship(back_populates="users")
    team_memberships: Mapped[list["TeamMember"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    assignments: Mapped[list["LeadAssignment"]] = relationship(back_populates="user", foreign_keys="LeadAssignment.user_id")
    assigned_leads: Mapped[list["Lead"]] = relationship(back_populates="assigned_to", foreign_keys="Lead.assigned_to_user_id")
    activities: Mapped[list["CRMActivity"]] = relationship(back_populates="user")
    reminders: Mapped[list["FollowUpReminder"]] = relationship(back_populates="user")
    authored_drafts: Mapped[list["EmailDraft"]] = relationship(back_populates="created_by")


class Team(TimestampMixin, Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    organization: Mapped["Organization"] = relationship(back_populates="teams")
    members: Mapped[list["TeamMember"]] = relationship(back_populates="team", cascade="all, delete-orphan")
    assignments: Mapped[list["LeadAssignment"]] = relationship(back_populates="team")

    __table_args__ = (UniqueConstraint("organization_id", "name", name="uq_teams_org_name"),)


class TeamMember(TimestampMixin, Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(30), default="sales_rep", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)

    team: Mapped["Team"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="team_memberships")

    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_members_team_user"),
        CheckConstraint("role IN ('owner','admin','manager','sales_rep')", name="ck_team_members_role"),
    )


class Niche(TimestampMixin, Base):
    __tablename__ = "niches"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    leads: Mapped[list["Lead"]] = relationship(back_populates="niche", foreign_keys="Lead.niche_id")
    lead_links: Mapped[list["LeadNiche"]] = relationship(back_populates="niche", cascade="all, delete-orphan")
    organization_links: Mapped[list["OrganizationNiche"]] = relationship(back_populates="niche", cascade="all, delete-orphan")
    search_configurations: Mapped[list["SearchConfiguration"]] = relationship(back_populates="niche")
    campaign_links: Mapped[list["CampaignNiche"]] = relationship(back_populates="niche", cascade="all, delete-orphan")


class OrganizationNiche(TimestampMixin, Base):
    __tablename__ = "organization_niches"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    niche_id: Mapped[int] = mapped_column(ForeignKey("niches.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="niche_links")
    niche: Mapped["Niche"] = relationship(back_populates="organization_links")

    __table_args__ = (UniqueConstraint("organization_id", "niche_id", name="uq_organization_niche"),)


class Country(TimestampMixin, Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    regions: Mapped[list["Region"]] = relationship(back_populates="country")
    leads: Mapped[list["Lead"]] = relationship(back_populates="country")

    __table_args__ = (CheckConstraint("length(code) BETWEEN 2 AND 3", name="ck_countries_code_length"),)


class Region(TimestampMixin, Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    region_type: Mapped[str] = mapped_column(String(40), default="state_or_region", nullable=False)

    country: Mapped["Country"] = relationship(back_populates="regions")
    cities: Mapped[list["City"]] = relationship(back_populates="region")
    leads: Mapped[list["Lead"]] = relationship(back_populates="region")


class City(TimestampMixin, Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id", ondelete="RESTRICT"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    region: Mapped["Region"] = relationship(back_populates="cities")
    leads: Mapped[list["Lead"]] = relationship(back_populates="city")
    __table_args__ = (Index("ix_cities_region_name", "region_id", "name"),)


class DataSource(TimestampMixin, Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(512))
    source_kind: Mapped[str] = mapped_column(String(40), default="other", nullable=False)

    scraping_jobs: Mapped[list["ScrapingJob"]] = relationship(back_populates="data_source")
    leads: Mapped[list["Lead"]] = relationship(back_populates="data_source")
    lead_sources: Mapped[list["LeadSource"]] = relationship(back_populates="data_source")


class SearchConfiguration(TimestampMixin, Base):
    __tablename__ = "search_configurations"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(140), nullable=False)
    niche_id: Mapped[int | None] = mapped_column(ForeignKey("niches.id", ondelete="SET NULL"), index=True)
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id", ondelete="SET NULL"), index=True)
    region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id", ondelete="SET NULL"), index=True)
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id", ondelete="SET NULL"), index=True)
    query_text: Mapped[str | None] = mapped_column(Text)
    options: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="search_configurations")
    niche: Mapped["Niche | None"] = relationship(back_populates="search_configurations")
    jobs: Mapped[list["ScrapingJob"]] = relationship(back_populates="search_configuration")


class ScrapingJob(TimestampMixin, Base):
    __tablename__ = "scraping_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    search_configuration_id: Mapped[int | None] = mapped_column(ForeignKey("search_configurations.id", ondelete="SET NULL"), index=True)
    data_source_id: Mapped[int] = mapped_column(ForeignKey("data_sources.id", ondelete="RESTRICT"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    finished_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    result_summary: Mapped[str | None] = mapped_column(Text)

    data_source: Mapped["DataSource"] = relationship(back_populates="scraping_jobs")
    search_configuration: Mapped["SearchConfiguration | None"] = relationship(back_populates="jobs")
    __table_args__ = (Index("ix_scraping_jobs_status_created", "status", "created_at"),)


class Lead(TimestampMixin, Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True)
    business_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    business_category: Mapped[str | None] = mapped_column(String(160))
    niche_id: Mapped[int] = mapped_column(ForeignKey("niches.id", ondelete="RESTRICT"), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False)
    region_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id", ondelete="SET NULL"), index=True)
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id", ondelete="SET NULL"), index=True)
    address: Mapped[str | None] = mapped_column(Text)
    website: Mapped[str | None] = mapped_column(String(512))
    public_phone: Mapped[str | None] = mapped_column(String(80))
    public_email: Mapped[str | None] = mapped_column(String(320))
    email_validation_status: Mapped[str] = mapped_column(String(30), default="unknown", server_default="unknown", nullable=False)
    original_source: Mapped[str | None] = mapped_column(String(120))
    original_source_url: Mapped[str | None] = mapped_column(Text)
    data_source_id: Mapped[int | None] = mapped_column(ForeignKey("data_sources.id", ondelete="SET NULL"), index=True)
    discovered_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    crm_status: Mapped[str] = mapped_column(String(50), default="discovered", server_default="discovered", nullable=False, index=True)
    qualification_score: Mapped[float] = mapped_column(Float, default=0.0, server_default="0", nullable=False)
    normalized_name: Mapped[str | None] = mapped_column(String(255))
    dedupe_key: Mapped[str | None] = mapped_column(String(64))
    notes: Mapped[str | None] = mapped_column(Text)
    assigned_to_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)

    organization: Mapped["Organization | None"] = relationship(back_populates="leads")
    niche: Mapped["Niche"] = relationship(back_populates="leads", foreign_keys=[niche_id])
    country: Mapped["Country"] = relationship(back_populates="leads")
    region: Mapped["Region | None"] = relationship(back_populates="leads")
    city: Mapped["City | None"] = relationship(back_populates="leads")
    data_source: Mapped["DataSource | None"] = relationship(back_populates="leads")
    assigned_to: Mapped["User | None"] = relationship(back_populates="assigned_leads", foreign_keys=[assigned_to_user_id])
    niche_links: Mapped[list["LeadNiche"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    niches: Mapped[list["Niche"]] = relationship(secondary="lead_niches", viewonly=True)
    contacts: Mapped[list["LeadContact"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    sources: Mapped[list["LeadSource"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    score_history: Mapped[list["LeadScore"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    assignments: Mapped[list["LeadAssignment"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    activities: Mapped[list["CRMActivity"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    status_history: Mapped[list["LeadStatusHistory"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    reminders: Mapped[list["FollowUpReminder"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    campaign_contacts: Mapped[list["CampaignContact"]] = relationship(back_populates="lead", cascade="all, delete-orphan")
    do_not_contact_records: Mapped[list["DoNotContact"]] = relationship(back_populates="lead")

    __table_args__ = (
        Index("ix_leads_org_status", "organization_id", "crm_status"),
        Index("ix_leads_org_niche_country", "organization_id", "niche_id", "country_id"),
        Index("ix_leads_org_discovered", "organization_id", "discovered_at"),
        Index("ix_leads_org_score", "organization_id", "qualification_score"),
        Index("uq_leads_org_dedupe", "organization_id", "dedupe_key", unique=True,
              sqlite_where=text("organization_id IS NOT NULL AND dedupe_key IS NOT NULL"),
              postgresql_where=text("organization_id IS NOT NULL AND dedupe_key IS NOT NULL")),
    )


class LeadNiche(Base):
    __tablename__ = "lead_niches"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    niche_id: Mapped[int] = mapped_column(ForeignKey("niches.id", ondelete="RESTRICT"), nullable=False, index=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    added_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    lead: Mapped["Lead"] = relationship(back_populates="niche_links")
    niche: Mapped["Niche"] = relationship(back_populates="lead_links")
    __table_args__ = (UniqueConstraint("lead_id", "niche_id", name="uq_lead_niche"),)


class LeadContact(TimestampMixin, Base):
    __tablename__ = "lead_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    contact_type: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[str] = mapped_column(String(512), nullable=False)
    normalized_value: Mapped[str | None] = mapped_column(String(512))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("1"), nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="contacts")
    verifications: Mapped[list["EmailVerification"]] = relationship(back_populates="contact", cascade="all, delete-orphan")
    do_not_contact_records: Mapped[list["DoNotContact"]] = relationship(back_populates="contact")
    __table_args__ = (
        Index("uq_lead_contact_normalized", "lead_id", "contact_type", "normalized_value", unique=True),
        Index("ix_lead_contact_type_value", "contact_type", "normalized_value"),
    )


class LeadSource(TimestampMixin, Base):
    __tablename__ = "lead_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    data_source_id: Mapped[int | None] = mapped_column(ForeignKey("data_sources.id", ondelete="SET NULL"), index=True)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_original: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    discovered_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="sources")
    data_source: Mapped["DataSource | None"] = relationship(back_populates="lead_sources")
    __table_args__ = (UniqueConstraint("lead_id", "normalized_url", name="uq_lead_source_url"),)


class EmailVerification(TimestampMixin, Base):
    __tablename__ = "email_verifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_contact_id: Mapped[int] = mapped_column(ForeignKey("lead_contacts.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    validation_method: Mapped[str] = mapped_column(String(40), default="manual", server_default="manual", nullable=False)
    provider_name: Mapped[str | None] = mapped_column(String(120))
    result_details: Mapped[str | None] = mapped_column(Text)
    smtp_response: Mapped[str | None] = mapped_column(Text)
    verified_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    contact: Mapped["LeadContact"] = relationship(back_populates="verifications")


EmailValidationResult = EmailVerification


class LeadScore(Base):
    __tablename__ = "lead_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    score_type: Mapped[str] = mapped_column(String(40), default="qualification", nullable=False)
    factors: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    lead: Mapped["Lead"] = relationship(back_populates="score_history")
    __table_args__ = (Index("ix_lead_scores_lead_created", "lead_id", "created_at"),)


from models_operations import (  # noqa: E402,F401
    Campaign, CampaignContact, CampaignNiche, CRMActivity, DoNotContact,
    EmailDraft, FollowUpReminder, LeadAssignment, LeadStatusHistory,
    SuppressionRecord,
)
