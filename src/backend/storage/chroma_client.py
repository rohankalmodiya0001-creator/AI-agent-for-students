"""ChromaDB client wrapper for persistent vector storage."""

from __future__ import annotations

from pathlib import Path

from chromadb import PersistentClient

from ..config import config


class ChromaClient:
    """Create and manage a persistent ChromaDB client."""

    def __init__(self) -> None:
        db_dir = Path(config.chroma_db_dir)
        db_dir.mkdir(parents=True, exist_ok=True)
        self.persist_directory = db_dir
        self.client = PersistentClient(path=str(db_dir))

    def get_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)

    def persist(self) -> None:
        """Persist the current client state to disk."""

        # PersistentClient writes to disk automatically; this is kept for API compatibility.
        return None
