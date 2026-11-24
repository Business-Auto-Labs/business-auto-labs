from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ENV_FILE = Path(__file__).resolve().with_name(".env")
load_dotenv(ENV_FILE)


def _read_port() -> int:
    raw_port = os.getenv("API_PORT", "8000")
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ValueError("API_PORT must be an integer between 1 and 65535.") from exc

    if not 1 <= port <= 65535:
        raise ValueError("API_PORT must be an integer between 1 and 65535.")
    return port


@dataclass(frozen=True)
class Settings:
    api_host: str
    api_port: int
    frontend_origins: tuple[str, ...]

    @classmethod
    def from_environment(cls) -> "Settings":
        raw_origins = os.getenv(
            "FRONTEND_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        )
        frontend_origins = tuple(
            origin.strip().rstrip("/")
            for origin in raw_origins.split(",")
            if origin.strip()
        )

        return cls(
            api_host=os.getenv("API_HOST", "127.0.0.1").strip() or "127.0.0.1",
            api_port=_read_port(),
            frontend_origins=frontend_origins,
        )


settings = Settings.from_environment()
