from typing import List

from ..models.schema import InterviewHistoryRecord, PerformanceTrend
from ..services.evaluation_service import EvaluationService


class EvaluationAgent:
    def __init__(self) -> None:
        self.service = EvaluationService()

    def evaluate(self, history: List[InterviewHistoryRecord]) -> PerformanceTrend:
        return self.service.evaluate_history(history)
