"""Phase 2 database tests. All generated test records stay in temporary SQLite files."""
from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from sqlalchemy import URL, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from database import BACKEND_DIR, Base, build_engine
from models import (
    Campaign, CampaignContact, CampaignNiche, City, Country, DataSource,
    DoNotContact, EmailDraft, EmailVerification, FollowUpReminder, Lead,
    LeadAssignment, LeadContact, LeadNiche, LeadScore, LeadSource,
    LeadStatusHistory, Niche, Organization, OrganizationNiche, Region,
    SuppressionRecord, ScrapingJob, SearchConfiguration, Team, TeamMember, User,
)
from crm_services import (
    assign_lead, change_lead_status, discover_or_merge_lead,
    record_do_not_contact, record_email_validation,
)
from run_migrations import upgrade


class PhaseTwoDatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="bal-crm-test-")
        self.db_path = Path(self.temp_dir.name) / "phase2.sqlite3"
        self.url = URL.create("sqlite", database=str(self.db_path))
        upgrade(self.url)
        self.engine = build_engine(self.url)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def tearDown(self) -> None:
        self.engine.dispose()
        self.temp_dir.cleanup()

    def _base_records(self, db: Session):
        organization = Organization(name="Test Organization", slug="test-organization")
        niche_a = Niche(name="Dental Test", slug="dental-test")
        niche_b = Niche(name="Clinic Test", slug="clinic-test")
        country = Country(name="Testland", code="TT")
        db.add_all([organization, niche_a, niche_b, country])
        db.flush()
        region = Region(country_id=country.id, name="Test State")
        db.add(region)
        db.flush()
        city = City(region_id=region.id, name="Test City")
        user = User(
            organization_id=organization.id,
            email="rep@businessautolabs.test",
            hashed_password="test-only-not-a-real-password",
            role="sales_rep",
        )
        db.add_all([city, user])
        db.flush()
        team = Team(organization_id=organization.id, name="Test Sales")
        db.add(team)
        db.flush()
        membership = TeamMember(team_id=team.id, user_id=user.id, role="sales_rep")
        db.add(membership)
        db.commit()
        return organization, niche_a, niche_b, country, region, city, user, team

    def test_local_lead_merge_and_history_relationships(self) -> None:
        with self.Session() as db:
            org, niche_a, niche_b, country, region, city, user, team = self._base_records(db)
            source = DataSource(name="Manual Test Directory", source_kind="manual")
            db.add(source)
            db.commit()
            search = SearchConfiguration(
                organization_id=org.id,
                name="Local test search",
                niche_id=niche_a.id,
                country_id=country.id,
                options={"mode": "manual-test-only"},
            )
            db.add(search)
            db.flush()
            job = ScrapingJob(
                organization_id=org.id,
                search_configuration_id=search.id,
                data_source_id=source.id,
                status="pending",
            )
            db.add(job)
            db.commit()
            self.assertEqual(job.search_configuration_id, search.id)
            self.assertEqual(job.data_source.name, source.name)

            lead = discover_or_merge_lead(
                db,
                organization_id=org.id,
                niche_id=niche_a.id,
                country_id=country.id,
                region_id=region.id,
                city_id=city.id,
                business_name="Riverside Dental",
                business_category="Dental clinic",
                address="1 Test Road",
                website="https://www.riverside.example/",
                public_phone="+1 (555) 010-0100",
                public_email="Info@Riverside.example",
                source_name="Test Directory",
                source_url="https://directory.example.test/riverside",
                data_source_id=source.id,
                score=71.0,
            )
            db.commit()
            first_id = lead.id
            original_source = lead.original_source_url

            merged = discover_or_merge_lead(
                db,
                organization_id=org.id,
                niche_id=niche_b.id,
                country_id=country.id,
                region_id=region.id,
                city_id=city.id,
                business_name="  riverside   dental  ",
                website="https://riverside.example",
                public_email="INFO@RIVERSIDE.EXAMPLE",
                source_name="Second Test Directory",
                source_url="https://another.example.test/business/riverside",
                score=84.0,
            )
            db.commit()

            self.assertEqual(merged.id, first_id)
            self.assertEqual(merged.original_source_url, original_source)
            self.assertEqual(db.scalar(select(func.count()).select_from(Lead)), 1)
            self.assertEqual(db.scalar(select(func.count()).select_from(LeadNiche)), 2)
            self.assertEqual(db.scalar(select(func.count()).select_from(LeadSource)), 2)
            self.assertEqual(db.scalar(select(func.count()).select_from(LeadContact)), 3)
            self.assertEqual(db.scalar(select(func.count()).select_from(LeadScore)), 2)
            self.assertEqual({item.id for item in merged.niches}, {niche_a.id, niche_b.id})
            self.assertEqual(db.scalar(select(func.count()).select_from(OrganizationNiche)), 2)
            self.assertIsNotNone(merged.discovered_at)
            self.assertIsNotNone(merged.discovered_at.tzinfo)

            email = db.scalar(select(LeadContact).where(
                LeadContact.lead_id == lead.id,
                LeadContact.contact_type == "email",
            ))
            first_check = record_email_validation(
                db, lead_contact_id=email.id, status="valid", validation_method="syntax"
            )
            second_check = record_email_validation(
                db, lead_contact_id=email.id, status="risky", validation_method="manual",
                result_details="Test-only review note.",
            )
            self.assertIsInstance(first_check, EmailVerification)
            self.assertEqual(second_check.status, "risky")
            self.assertEqual(lead.email_validation_status, "risky")
            self.assertEqual(db.scalar(select(func.count()).select_from(EmailVerification)), 2)

            lead = change_lead_status(
                db, organization_id=org.id, lead_id=lead.id, to_status="qualified",
                actor_user_id=user.id, note="Test-only qualification.",
            )
            self.assertEqual(lead.crm_status, "qualified")
            self.assertEqual(db.scalar(select(func.count()).select_from(LeadStatusHistory)), 1)
            lead.crm_status = "contacted"
            db.flush()
            self.assertEqual(db.scalar(select(func.count()).select_from(LeadStatusHistory)), 2)
            self.assertIsNone(lead.status_history[-1].actor_user_id)

            assignment = assign_lead(
                db, organization_id=org.id, lead_id=lead.id, user_id=user.id, team_id=team.id
            )
            self.assertTrue(assignment.is_current)
            self.assertEqual(lead.assigned_to_user_id, user.id)

            reminder = FollowUpReminder(
                lead_id=lead.id, user_id=user.id, due_date=lead.created_at, notes="Test-only reminder."
            )
            campaign = Campaign(organization_id=org.id, name="Test Draft Campaign", status="draft")
            db.add_all([reminder, campaign])
            db.flush()
            db.add(CampaignNiche(campaign_id=campaign.id, niche_id=niche_b.id))
            db.add(CampaignContact(campaign_id=campaign.id, lead_id=lead.id, status="queued"))
            draft = EmailDraft(
                campaign_id=campaign.id, lead_id=lead.id, created_by_user_id=user.id,
                subject="Test-only draft", body="Not sent.", status="draft",
            )
            db.add(draft)
            dnc = record_do_not_contact(
                db, organization_id=org.id, value="info@riverside.example",
                reason="Test-only request", lead_id=lead.id, lead_contact_id=email.id,
            )
            db.add(SuppressionRecord(
                organization_id=org.id, value="block@businessautolabs.test",
                normalized_value="block@businessautolabs.test", reason="test-only",
            ))
            db.commit()

            self.assertEqual(draft.status, "draft")
            self.assertEqual(draft.body, "Not sent.")
            self.assertEqual(dnc.normalized_value, "info@riverside.example")
            self.assertEqual(db.scalar(select(func.count()).select_from(CampaignContact)), 1)
            self.assertEqual(db.scalar(select(func.count()).select_from(DoNotContact)), 1)
            self.assertEqual(db.scalar(select(func.count()).select_from(SuppressionRecord)), 1)

    def test_matching_is_organization_scoped_and_geography_is_validated(self) -> None:
        with self.Session() as db:
            org, niche_a, _, country, region, city, _, _ = self._base_records(db)
            lead_a = discover_or_merge_lead(
                db, organization_id=org.id, niche_id=niche_a.id, country_id=country.id,
                region_id=region.id, city_id=city.id, business_name="Same Name Test",
            )
            second_org = Organization(name="Other Test Organization", slug="other-test-organization")
            db.add(second_org)
            db.flush()
            lead_b = discover_or_merge_lead(
                db, organization_id=second_org.id, niche_id=niche_a.id, country_id=country.id,
                region_id=region.id, city_id=city.id, business_name="Same Name Test",
            )
            self.assertNotEqual(lead_a.id, lead_b.id)
            self.assertEqual(db.scalar(select(func.count()).select_from(Lead)), 2)

            with self.assertRaisesRegex(ValueError, "requires its state or region"):
                discover_or_merge_lead(
                    db, organization_id=org.id, niche_id=niche_a.id, country_id=country.id,
                    city_id=city.id, business_name="Invalid Geography Test",
                )
            db.rollback()

    def test_sqlite_foreign_keys_and_migration_idempotency(self) -> None:
        with self.engine.connect() as connection:
            self.assertEqual(connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one(), 1)
        with self.Session() as db:
            with self.assertRaises(IntegrityError):
                db.execute(insert(Team).values(organization_id=987654, name="Invalid Test Team"))
                db.commit()
            db.rollback()
        upgrade(self.url)
        upgrade(self.url)
        with self.engine.connect() as connection:
            self.assertEqual(connection.exec_driver_sql("PRAGMA foreign_key_check").all(), [])
            self.assertEqual(connection.exec_driver_sql("SELECT version_num FROM alembic_version").scalar_one(), "20261124_0002")

    def test_legacy_database_copy_migrates_without_changing_row_counts(self) -> None:
        legacy_path = BACKEND_DIR / "crm.db"
        if not legacy_path.exists():
            self.skipTest("No local legacy crm.db is available; fresh-schema migration tests still run.")
        copy_path = Path(self.temp_dir.name) / "legacy-copy.sqlite3"
        source = sqlite3.connect(legacy_path)
        target = sqlite3.connect(copy_path)
        try:
            before_tables = [
                row[0] for row in source.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'alembic_version'"
                )
            ]
            before_counts = {
                table: source.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]
                for table in before_tables
            }
            source.backup(target)
        finally:
            source.close()
            target.close()

        url = URL.create("sqlite", database=str(copy_path))
        upgrade(url)
        upgrade(url)
        migrated = sqlite3.connect(copy_path)
        try:
            for table, count in before_counts.items():
                self.assertEqual(
                    migrated.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0],
                    count,
                    f"Migration changed row count in {table}",
                )
            self.assertEqual(
                migrated.execute("SELECT COUNT(*) FROM lead_niches").fetchone()[0],
                before_counts.get("leads", 0),
            )
            self.assertEqual(migrated.execute("PRAGMA foreign_key_check").fetchall(), [])
        finally:
            migrated.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
