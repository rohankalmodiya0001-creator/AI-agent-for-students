"""Evaluation and trend aggregation utilities for interview history."""

from __future__ import annotations

from ..app_logging import logger
from ..models.schema import InterviewHistoryRecord, PerformanceTrend


class EvaluationService:
    """Aggregate interview performance into a stable readiness trend."""

    def evaluate_history(self, history: list[InterviewHistoryRecord]) -> PerformanceTrend:
        if not history:
            return PerformanceTrend(
                technical_score=0.0,
                communication_score=0.0,
                problem_solving_score=0.0,
                confidence_score=0.0,
                readiness_score=0.0,
                weak_topics=[],
                strong_topics=[],
            )

        total = len(history)
        technical_score = sum(record.evaluation.correctness for record in history) / total
        communication_score = sum(record.evaluation.communication for record in history) / total
        problem_solving_score = sum(record.evaluation.problem_solving for record in history) / total
        confidence_score = sum(record.evaluation.confidence for record in history) / total
        depth_score = sum(record.evaluation.depth for record in history) / total

        readiness_score = round(
            technical_score * 0.35 + problem_solving_score * 0.25 + confidence_score * 0.2 + depth_score * 0.2,
            1,
        )

        weak_topics = sorted({record.topic for record in history if record.evaluation.correctness < 65 or record.evaluation.depth < 65})
        strong_topics = sorted({record.topic for record in history if record.evaluation.correctness >= 80 and record.evaluation.depth >= 80})

        logger.info(
            "Aggregated interview history: records=%d technical=%.1f communication=%.1f readiness=%.1f",
            total,
            technical_score,
            communication_score,
            readiness_score,
        )

        return PerformanceTrend(
            technical_score=round(technical_score, 1),
            communication_score=round(communication_score, 1),
            problem_solving_score=round(problem_solving_score, 1),
            confidence_score=round(confidence_score, 1),
            readiness_score=readiness_score,
            weak_topics=weak_topics,
            strong_topics=strong_topics,
        )
