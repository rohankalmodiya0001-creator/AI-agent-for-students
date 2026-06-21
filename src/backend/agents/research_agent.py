from typing import List

from ..services.rag_service import RAGService


class ResearchAgent:
    def __init__(self) -> None:
        self.service = RAGService()

    def retrieve_learning_context(self, query: str, topics: List[str]) -> str:
        return self.service.build_context(query, topics)

    def get_top_references(self, query: str, topics: List[str], limit: int = 5):
        return self.service.retrieve(query, limit)
