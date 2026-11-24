"""Run Alembic migrations using backend/.env or a supplied local database URL."""
from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import URL, make_url

from database import BACKEND_DIR, DATABASE_URL


def upgrade(database_url: str | URL | None = None) -> None:
    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_DIR / "migrations"))
    url = make_url(database_url) if isinstance(database_url, str) else (database_url or DATABASE_URL)
    config.set_main_option(
        "sqlalchemy.url",
        url.render_as_string(hide_password=False).replace("%", "%%"),
    )
    command.upgrade(config, "head")


if __name__ == "__main__":
    upgrade()
