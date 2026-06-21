"""Retrieval and embedding utilities for the knowledge base."""

from __future__ import annotations

import warnings
from typing import Any, Dict, List, Optional

from ..config import config
from ..app_logging import logger
from ..storage.chroma_client import ChromaClient

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    try:
        from google import generativeai as genai
    except Exception:  # pragma: no cover - import availability depends on environment
        genai = None


class RAGService:
    """Store and retrieve interview coaching knowledge using ChromaDB."""

    def __init__(self) -> None:
        self.chroma = ChromaClient()
        self.collection = self.chroma.get_collection("interview_knowledge")
        self._fallback_encoder = None

    def _configure_gemini(self) -> Any:
        if genai is None or not config.google_api_key:
            return None
        genai.configure(api_key=config.google_api_key)
        return genai

    @property
    def fallback_encoder(self):
        if self._fallback_encoder is None:
            from sentence_transformers import SentenceTransformer

            self._fallback_encoder = SentenceTransformer("all-MiniLM-L6-v2")
        return self._fallback_encoder

    def embed_text(self, text: str) -> List[float]:
        client = self._configure_gemini()
        if client is not None:
            try:
                response = client.embed_content(
                    model="models/text-embedding-004",
                    content=text,
                )
                return list(response["embedding"]["values"])
            except Exception as exc:
                logger.warning("Gemini embedding failed, falling back to sentence-transformers: %s", exc)

        return list(self.fallback_encoder.encode(text))

    def ingest_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents:
            return

        ids = [doc["id"] for doc in documents]
        documents_text = [doc["content"] for doc in documents]
        metadatas = [
            {
                "title": doc["title"],
                "topic": doc["topic"],
                "source": doc["source"],
                "difficulty": doc.get("difficulty", "medium"),
            }
            for doc in documents
        ]
        embeddings = [self.embed_text(doc["content"]) for doc in documents]

        self.collection.add(ids=ids, documents=documents_text, metadatas=metadatas, embeddings=embeddings)
        self.chroma.persist()

    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embed_text(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )

        retrieved: List[Dict[str, Any]] = []
        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for index, item_id in enumerate(ids):
            retrieved.append(
                {
                    "id": item_id,
                    "document": documents[index] if index < len(documents) else "",
                    "metadata": metadatas[index] if index < len(metadatas) else {},
                    "distance": distances[index] if index < len(distances) else None,
                }
            )
        return retrieved

    def build_context(self, query: str, topics: Optional[List[str]] = None) -> str:
        retrieved = self.retrieve(query)
        if topics:
            filtered = [item for item in retrieved if item["metadata"].get("topic") in topics]
        else:
            filtered = retrieved

        context_blocks = [
            f"[{item['metadata'].get('topic', 'general')}] {item['metadata'].get('title', '')}: {item['document']}"
            for item in filtered
        ]
        return "\n\n".join(context_blocks)
