"""CRM history, assignment, campaign draft, and contact-suppression models."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean, ForeignKey, Index, JSON, String, Text,
    UniqueConstraint, text, event, inspect,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from database import Base, TimestampMixin, UTCDateTime, utcnow


class LeadAssignment(Base):
    __tablename__ = "lead_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), index=True)
    assigned_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    assigned_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(UTCDateTime())
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="assignments")
    user: Mapped["User"] = relationship(back_populates="assignments", foreign_keys=[user_id])
    team: Mapped["Team | None"] = relationship(back_populates="assignments")
    assigned_by: Mapped["User | None"] = relationship(foreign_keys=[assigned_by_user_id])

    __table_args__ = (
        UniqueConstraint("lead_id", "user_id", name="uq_lead_user_assignment"),
        Index("ix_lead_assignments_current", "lead_id", "is_current"),
        Index(
            "uq_lead_assignment_current",
            "lead_id",
            unique=True,
            sqlite_where=text("is_current = 1"),
            postgresql_where=text("is_current IS TRUE"),
        ),
    )


class CRMActivity(Base):
    __tablename__ = "crm_activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    activity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    details: Mapped[str | None] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="activities")
    user: Mapped["User"] = relationship(back_populates="activities")
    __table_args__ = (Index("ix_crm_activities_lead_time", "lead_id", "timestamp"),)


class LeadStatusHistory(Base):
    __tablename__ = "lead_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    from_status: Mapped[str | None] = mapped_column(String(50))
    to_status: Mapped[str] = mapped_column(String(50), nullable=False)
    note: Mapped[str | None] = mapped_column(Text)
    changed_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)

    lead: Mapped["Lead"] = relationship(back_populates="status_history")
    actor: Mapped["User | None"] = relationship()
    __table_args__ = (Index("ix_lead_status_history_lead_time", "lead_id", "changed_at"),)


class FollowUpReminder(TimestampMixin, Base):
    __tablename__ = "follow_up_reminders"

    id: Mapped[int] = mapped_column(primary_key=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    due_date: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(UTCDateTime())

    lead: Mapped["Lead"] = relationship(back_populates="reminders")
    user: Mapped["User"] = relationship(back_populates="reminders")
    __table_args__ = (Index("ix_follow_up_open_due", "is_completed", "due_date"),)


class Campaign(TimestampMixin, Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    niche_filter: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="draft", server_default="draft", nullable=False)

    organization: Mapped["Organization | None"] = relationship(back_populates="campaigns")
    campaign_contacts: Mapped[list["CampaignContact"]] = relationship(back_populates="campaign", cascade="all, delete-orphan")
    niche_links: Mapped[list["CampaignNiche"]] = relationship(back_populates="campaign", cascade="all, delete-orphan")
    niches: Mapped[list["Niche"]] = relationship(secondary="campaign_niches", viewonly=True)
    email_drafts: Mapped[list["EmailDraft"]] = relationship(back_populates="campaign", cascade="all, delete-orphan")


class CampaignNiche(Base):
    __tablename__ = "campaign_niches"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    niche_id: Mapped[int] = mapped_column(ForeignKey("niches.id", ondelete="RESTRICT"), nullable=False, index=True)

    campaign: Mapped["Campaign"] = relationship(back_populates="niche_links")
    niche: Mapped["Niche"] = relationship(back_populates="campaign_links")
    __table_args__ = (UniqueConstraint("campaign_id", "niche_id", name="uq_campaign_niche"),)


class CampaignContact(TimestampMixin, Base):
    __tablename__ = "campaign_contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False, index=True)
    lead_id: Mapped[int] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="queued", nullable=False)
    sent_at: Mapped[datetime | None] = mapped_column(UTCDateTime())

    campaign: Mapped["Campaign"] = relationship(back_populates="campaign_contacts")
    lead: Mapped["Lead"] = relationship(back_populates="campaign_contacts")
    __table_args__ = (UniqueConstraint("campaign_id", "lead_id", name="uq_campaign_lead"),)


class EmailDraft(TimestampMixin, Base):
    __tablename__ = "email_drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    campaign_id: Mapped[int | None] = mapped_column(ForeignKey("campaigns.id", ondelete="CASCADE"), index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), index=True)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    subject: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    body: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="draft", nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    campaign: Mapped["Campaign | None"] = relationship(back_populates="email_drafts")
    lead: Mapped["Lead | None"] = relationship()
    created_by: Mapped["User | None"] = relationship(back_populates="authored_drafts")
    __table_args__ = (Index("ix_email_drafts_status_updated", "status", "updated_at"),)


class SuppressionRecord(TimestampMixin, Base):
    """Organization-wide email/domain suppression; never sends or calls external services."""
    __tablename__ = "suppression_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    value: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    normalized_value: Mapped[str | None] = mapped_column(String(255))
    suppression_type: Mapped[str] = mapped_column(String(30), default="email", nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)

    organization: Mapped["Organization | None"] = relationship()
    __table_args__ = (Index("uq_suppression_normalized", "normalized_value", unique=True),)


class DoNotContact(TimestampMixin, Base):
    __tablename__ = "do_not_contact"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id", ondelete="SET NULL"), index=True)
    lead_id: Mapped[int | None] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), index=True)
    lead_contact_id: Mapped[int | None] = mapped_column(ForeignKey("lead_contacts.id", ondelete="CASCADE"), index=True)
    value: Mapped[str] = mapped_column(String(512), nullable=False)
    normalized_value: Mapped[str] = mapped_column(String(512), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(80), default="manual", nullable=False)
    created_by_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utcnow, nullable=False)

    lead: Mapped["Lead | None"] = relationship(back_populates="do_not_contact_records")
    contact: Mapped["LeadContact | None"] = relationship(back_populates="do_not_contact_records")
    __table_args__ = (
        UniqueConstraint("organization_id", "normalized_value", name="uq_dnc_org_normalized"),
        Index("ix_dnc_org_created", "organization_id", "created_at"),
    )


@event.listens_for(Session, "before_flush")
def _record_direct_orm_status_changes(session, flush_context, instances) -> None:
    """Record status edits that bypass the richer application service."""
    from models import Lead

    for lead in session.dirty:
        if not isinstance(lead, Lead) or not session.is_modified(lead, include_collections=False):
            continue
        history = inspect(lead).attrs.crm_status.history
        if not history.has_changes() or not history.deleted or not history.added:
            continue
        already_recorded = any(
            isinstance(item, LeadStatusHistory) and item.lead is lead
            for item in session.new
        )
        if already_recorded:
            continue
        session.add(LeadStatusHistory(
            lead=lead,
            from_status=history.deleted[0],
            to_status=history.added[0],
            note="Status changed directly through the SQLAlchemy ORM.",
        ))
