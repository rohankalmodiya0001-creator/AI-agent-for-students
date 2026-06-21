"""Knowledge base ingestion service for the RAG layer."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Generator, List

from ..config import config
from ..app_logging import logger
from ..services.rag_service import RAGService


class IngestionService:
    def __init__(self) -> None:
        self.rag_service = RAGService()
        self.docs_path = Path(config.docs_path)
        self.docs_path.mkdir(parents=True, exist_ok=True)

    def _read_documents(self) -> Generator[Dict[str, Any], None, None]:
        for path in sorted(self.docs_path.rglob("*.txt")):
            yield {
                "id": f"{path.stem}-{path.stat().st_mtime_ns}",
                "title": path.stem,
                "topic": path.parent.name or "general",
                "source": str(path.relative_to(self.docs_path)),
                "content": path.read_text(encoding="utf-8"),
                "difficulty": "medium",
            }
        for path in sorted(self.docs_path.rglob("*.md")):
            yield {
                "id": f"{path.stem}-{path.stat().st_mtime_ns}",
                "title": path.stem,
                "topic": path.parent.name or "general",
                "source": str(path.relative_to(self.docs_path)),
                "content": path.read_text(encoding="utf-8"),
                "difficulty": "medium",
            }

    def _chunk_text(self, content: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        tokens = content.split()
        if len(tokens) <= chunk_size:
            return [content]

        chunks: List[str] = []
        start = 0
        while start < len(tokens):
            end = min(start + chunk_size, len(tokens))
            chunks.append(" ".join(tokens[start:end]))
            start = max(end - overlap, start + 1)
        return chunks

    def ingest_knowledge_base(self) -> Dict[str, Any]:
        documents = list(self._read_documents())
        if not documents:
            logger.info("No knowledge base documents found under %s", self.docs_path)
            return {"status": "empty", "message": "No documents were found in the knowledge base path."}

        chunks: List[Dict[str, Any]] = []
        for doc in documents:
            for chunk_index, chunk in enumerate(self._chunk_text(doc["content"])):
                chunks.append(
                    {
                        "id": f"{doc['id']}-{chunk_index}",
                        "title": doc["title"],
                        "topic": doc["topic"],
                        "source": doc["source"],
                        "content": chunk,
                        "difficulty": doc.get("difficulty", "medium"),
                    }
                )

        self.rag_service.ingest_documents(chunks)
        logger.info("Ingested %d documents into the knowledge base", len(chunks))
        return {
            "status": "success",
            "ingested_document_count": len(documents),
            "ingested_chunk_count": len(chunks),
        }

    def list_documents(self) -> List[Dict[str, Any]]:
        return [
            {
                "title": path.stem,
                "path": str(path.relative_to(self.docs_path)),
                "size": path.stat().st_size,
                "topic": path.parent.name or "general",
            }
            for path in sorted(self.docs_path.rglob("*.txt")) + sorted(self.docs_path.rglob("*.md"))
        ]
