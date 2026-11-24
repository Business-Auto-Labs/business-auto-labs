"""Database configuration shared by the API, migrations, and tests."""
from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime, timezone
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import DateTime, Engine, create_engine, event
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.types import TypeDecorator


BACKEND_DIR = Path(__file__).resolve().parent
ENV_FILE = BACKEND_DIR / ".env"
load_dotenv(ENV_FILE)


def _database_url() -> URL:
    raw_url = os.getenv("DATABASE_URL")
    if not raw_url:
        raw_url = URL.create("sqlite", database=str(BACKEND_DIR / "crm.db"))
    else:
        raw_url = make_url(raw_url)

    if raw_url.drivername.startswith("sqlite"):
        database = raw_url.database
        if database and database != ":memory:":
            path = Path(database)
            if not path.is_absolute():
                path = BACKEND_DIR / path
            raw_url = raw_url.set(database=str(path.resolve()))
    return raw_url


DATABASE_URL = _database_url()


class UTCDateTime(TypeDecorator):
    """Store UTC timestamps and always return timezone-aware UTC values."""
    impl = DateTime
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(DateTime(timezone=True))

    def process_bind_param(self, value: datetime | None, dialect):
        if value is None:
            return None
        value = value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)
        return value.replace(tzinfo=None) if dialect.name == "sqlite" else value

    def process_result_value(self, value: datetime | None, dialect):
        if value is None:
            return None
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = mapped_column(UTCDateTime(), default=utcnow, nullable=False)
    updated_at = mapped_column(UTCDateTime(), default=utcnow, onupdate=utcnow, nullable=False)


def build_engine(url: str | URL | None = None, **options: object) -> Engine:
    """Create an engine with SQLite foreign-key enforcement enabled."""
    resolved_url = make_url(url) if isinstance(url, str) else (url or DATABASE_URL)
    connect_args: dict[str, object] = {}
    if resolved_url.drivername.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(
        resolved_url,
        pool_pre_ping=True,
        connect_args=connect_args,
        **options,
    )

    if resolved_url.drivername.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _enable_sqlite_foreign_keys(dbapi_connection: object, _: object) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
