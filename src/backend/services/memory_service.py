from typing import Any, Dict, List

from ..storage.memory_store import get_session_memory, save_session_memory


class MemoryService:
    def store_interview_record(self, session_id: str, record: Dict[str, Any]) -> None:
        save_session_memory(session_id, record)

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        return get_session_memory(session_id)

    def build_progress_summary(self, session_id: str) -> Dict[str, Any]:
        history = self.get_session_history(session_id)
        if not history:
            return {
                "session_id": session_id,
                "history_length": 0,
                "latest_feedback": None,
                "adaptive_roadmap": [],
            }

        latest_record = history[-1]
        return {
            "session_id": session_id,
            "history_length": len(history),
            "latest_feedback": latest_record.get("feedback"),
            "weak_topics": latest_record.get("weak_topics", []),
            "strong_topics": latest_record.get("strong_topics", []),
            "adaptive_roadmap": latest_record.get("adaptive_roadmap", []),
            "question_count": latest_record.get("question_count", 0),
        }
