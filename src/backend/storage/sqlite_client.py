"""Compatibility wrapper for SQLite initialization used by the API startup."""

from __future__ import annotations

from pathlib import Path

from ..config import config
from ..database import DATABASE_PATH, initialize_database as _initialize_database


DB_PATH = DATABASE_PATH or Path(config.database_url.replace("sqlite:///", "", 1))


def initialize_database() -> None:
    """Initialize the application database schema."""

    _initialize_database()
