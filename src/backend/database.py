"""Database utilities for the Multi-Agent RAG Interview Coach backend."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import config


def _sqlite_path(database_url: str) -> Path | None:
    """Return the filesystem path for a SQLite URL, if applicable."""

    if not database_url.startswith("sqlite:///"):
        return None
    return Path(database_url.replace("sqlite:///", "", 1))


DATABASE_PATH = _sqlite_path(config.database_url)
if DATABASE_PATH is not None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(config.database_url, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def initialize_database() -> None:
    """Create the SQLite tables used by the application if they do not exist."""

    if DATABASE_PATH is None:
        return

    schema_statements = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            created_at TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            resume_id TEXT,
            job_description_id TEXT,
            skill_gap_report TEXT,
            roadmap TEXT,
            final_report TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS resume_profiles (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            parsed_skills TEXT,
            projects TEXT,
            experience_summary TEXT,
            certifications TEXT,
            technologies TEXT,
            raw_text TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            required_skills TEXT,
            technologies TEXT,
            responsibilities TEXT,
            seniority_level TEXT,
            keywords TEXT,
            raw_text TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS interview_history (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            question TEXT,
            topic TEXT,
            answer TEXT,
            evaluation TEXT,
            feedback TEXT,
            created_at TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS performance_trends (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            technical_score REAL,
            communication_score REAL,
            problem_solving_score REAL,
            confidence_score REAL,
            readiness_score REAL,
            weak_topics TEXT,
            strong_topics TEXT,
            created_at TEXT
        )
        """,
    ]

    assert DATABASE_PATH is not None
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        for statement in schema_statements:
            cursor.execute(statement)
        connection.commit()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional SQLAlchemy session scope."""

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db_session() -> Generator[Session, None, None]:
    """Yield a database session for FastAPI dependencies."""

    with session_scope() as session:
        yield session

engine = create_engine(config.database_url, future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db_session():
    with SessionLocal() as session:
        yield session
