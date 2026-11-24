"""Phase 2 integrity follow-up: contact timestamps, assignment invariant, and email cache."""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect, text


revision = "20261124_0002"
down_revision = "20261124_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = {item["name"] for item in inspector.get_columns("campaign_contacts")}
    missing = [
        column for column in (
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )
        if column.name not in columns
    ]
    if missing:
        with op.batch_alter_table("campaign_contacts") as batch:
            for column in missing:
                batch.add_column(column)

    # Keep the lead's quick filter field in sync with the newest stored result.
    bind.execute(text("""
        UPDATE leads
        SET email_validation_status = (
            SELECT lower(ev.status)
            FROM email_verifications ev
            JOIN lead_contacts lc ON lc.id = ev.lead_contact_id
            WHERE lc.lead_id = leads.id AND lower(lc.contact_type) = 'email'
            ORDER BY ev.verified_at DESC, ev.id DESC
            LIMIT 1
        )
        WHERE EXISTS (
            SELECT 1
            FROM email_verifications ev
            JOIN lead_contacts lc ON lc.id = ev.lead_contact_id
            WHERE lc.lead_id = leads.id AND lower(lc.contact_type) = 'email'
        )
    """))

    existing_indexes = {index["name"] for index in inspect(bind).get_indexes("lead_assignments")}
    if "uq_lead_assignment_current" not in existing_indexes:
        op.create_index(
            "uq_lead_assignment_current",
            "lead_assignments",
            ["lead_id"],
            unique=True,
            sqlite_where=sa.text("is_current = 1"),
            postgresql_where=sa.text("is_current IS TRUE"),
        )


def downgrade() -> None:
    raise RuntimeError(
        "Phase 2 integrity migration is forward-only to avoid deleting CRM history. "
        "Restore a verified database backup to reverse it."
    )
