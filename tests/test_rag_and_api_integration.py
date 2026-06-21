from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

from backend.api.app import create_app
from backend.api import routes as routes_module
from backend.services.rag_service import RAGService


class DummyCollection:
    def __init__(self, query_results: dict | None = None) -> None:
        self.records: list[dict] = []
        self._query_results = query_results or {
            "ids": [["doc-1", "doc-2"]],
            "documents": [["RAG context", "Python context"]],
            "metadatas": [[
                {"topic": "rag", "title": "RAG 101"},
                {"topic": "python", "title": "Python 101"},
            ]],
            "distances": [[0.12, 0.34]],
        }

    def add(self, ids, documents, metadatas, embeddings) -> None:  # noqa: ANN001
        self.records.append(
            {
                "ids": ids,
                "documents": documents,
                "metadatas": metadatas,
                "embeddings": embeddings,
            }
        )

    def query(self, **kwargs):  # noqa: ANN003
        return self._query_results


class FakeWorkflow:
    def roadmap_generation(self, input_data: dict) -> dict:
        return {"roadmap": ["study rag", "practice prompt engineering"]}

    def mock_interview(self, input_data: dict) -> dict:
        return {
            "questions": [
                {"question": "Explain RAG", "topic": "rag", "difficulty": "medium", "follow_up": None}
            ]
        }

    def evaluate(self, input_data: dict) -> dict:
        return {
            "interview_history": [
                {
                    "question": "Explain RAG",
                    "topic": "rag",
                    "answer": "RAG combines retrieval and generation.",
                    "evaluation": {
                        "correctness": 75,
                        "depth": 70,
                        "communication": 72,
                        "confidence": 65,
                        "problem_solving": 74,
                    },
                    "feedback": "Add more depth.",
                }
            ],
            "performance_trends": {
                "technical_score": 75,
                "communication_score": 72,
                "problem_solving_score": 74,
                "confidence_score": 65,
                "readiness_score": 71,
                "weak_topics": ["rag"],
                "strong_topics": ["python"],
            },
            "adaptive_roadmap": ["study rag"],
        }

    def final_report(self, input_data: dict) -> dict:
        return {"final_report": "Final Interview Readiness Report\nGreat progress."}


class FakeMemoryService:
    def __init__(self) -> None:
        self.records: list[tuple[str, dict]] = []

    def store_interview_record(self, session_id: str, record: dict) -> None:
        self.records.append((session_id, record))

    def build_progress_summary(self, session_id: str) -> dict:
        if not self.records:
            return {"session_id": session_id, "history_length": 0, "latest_feedback": None, "adaptive_roadmap": []}
        _, latest = self.records[-1]
        return {
            "session_id": session_id,
            "history_length": len(self.records),
            "latest_feedback": latest.get("feedback"),
            "weak_topics": latest.get("weak_topics", []),
            "strong_topics": latest.get("strong_topics", []),
            "adaptive_roadmap": latest.get("adaptive_roadmap", []),
            "question_count": latest.get("question_count", 0),
        }


def test_rag_service_ingest_and_retrieve(monkeypatch) -> None:
    service = RAGService.__new__(RAGService)
    service.collection = DummyCollection()
    service.chroma = SimpleNamespace(persist=lambda: None)
    monkeypatch.setattr(service, "embed_text", lambda text: [0.1, 0.2, 0.3])

    documents = [
        {
            "id": "doc-1",
            "title": "RAG 101",
            "topic": "rag",
            "source": "rag.md",
            "content": "Retrieval augmented generation basics.",
            "difficulty": "medium",
        }
    ]
    service.ingest_documents(documents)

    assert service.collection.records
    results = service.retrieve("Explain RAG", limit=2)
    assert results[0]["metadata"]["topic"] == "rag"


def test_rag_service_build_context_filters_topics(monkeypatch) -> None:
    service = RAGService.__new__(RAGService)
    service.collection = DummyCollection()
    service.chroma = SimpleNamespace(persist=lambda: None)
    monkeypatch.setattr(service, "embed_text", lambda text: [0.1, 0.2, 0.3])

    context = service.build_context("rag", topics=["rag"])

    assert "RAG context" in context
    assert "Python context" not in context


def test_api_endpoints_use_workflow_and_memory(monkeypatch) -> None:
    fake_workflow = FakeWorkflow()
    fake_memory = FakeMemoryService()
    monkeypatch.setattr(routes_module, "_workflow", fake_workflow)
    monkeypatch.setattr(routes_module, "memory_service", fake_memory)

    client = TestClient(create_app())

    roadmap_response = client.post(
        "/api/roadmap",
        json={"skill_gap_report": {"missing_skills": [], "weak_skills": [], "strengths": [], "match_score": 0, "readiness_score": 0, "summary": ""}},
    )
    assert roadmap_response.status_code == 200
    assert roadmap_response.json()["roadmap"][0] == "study rag"

    interview_response = client.post(
        "/api/mock-interview",
        json={
            "skill_gap_report": {
                "missing_skills": [],
                "weak_skills": [],
                "strengths": [],
                "match_score": 0,
                "readiness_score": 0,
                "summary": "",
            },
            "interview_type": "RAG",
        },
    )
    assert interview_response.status_code == 200
    assert interview_response.json()["questions"][0]["topic"] == "rag"

    evaluate_response = client.post(
        "/api/evaluate",
        json={
            "session_id": "session-1",
            "questions": [{"question": "Explain RAG", "topic": "rag", "difficulty": "medium"}],
            "answers": ["RAG combines retrieval and generation."],
        },
    )
    assert evaluate_response.status_code == 200
    assert fake_memory.records
    assert fake_memory.records[-1][0] == "session-1"

    report_response = client.post(
        "/api/final-report",
        json={
            "session_id": "session-1",
            "skill_gap_report": {
                "missing_skills": [],
                "weak_skills": [],
                "strengths": [],
                "match_score": 0,
                "readiness_score": 0,
                "summary": "",
            },
            "performance_trends": {
                "technical_score": 0,
                "communication_score": 0,
                "problem_solving_score": 0,
                "confidence_score": 0,
                "readiness_score": 0,
                "weak_topics": [],
                "strong_topics": [],
            },
        },
    )
    assert report_response.status_code == 200
    assert "Final Interview Readiness Report" in report_response.json()["final_report"]

    memory_response = client.get("/api/session/session-1/memory")
    assert memory_response.status_code == 200
    assert memory_response.json()["session_id"] == "session-1"
