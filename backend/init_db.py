"""Backward-compatible entry point; schema changes are managed by Alembic."""
from run_migrations import upgrade


def init_database() -> None:
    upgrade()


if __name__ == "__main__":
    init_database()
