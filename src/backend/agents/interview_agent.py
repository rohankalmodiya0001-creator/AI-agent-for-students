"""Adaptive interview execution and answer evaluation utilities."""

from __future__ import annotations

from typing import List

from ..agents.research_agent import ResearchAgent
from ..app_logging import logger
from ..models.schema import EvaluationMetrics, InterviewHistoryRecord, InterviewQuestion, SkillGapReport
from ..services.interview_service import InterviewService


class InterviewAgent:
    def __init__(self) -> None:
        self.service = InterviewService()
        self.research_agent = ResearchAgent()

    def prepare_questions(self, skill_gap: SkillGapReport, interview_type: str) -> List[InterviewQuestion]:
        return self.service.generate_questions(skill_gap, interview_type)

    def simulate_question_flow(
        self,
        questions: List[InterviewQuestion],
        answers: List[str],
    ) -> List[InterviewHistoryRecord]:
        if not questions:
            return []

        history: List[InterviewHistoryRecord] = []
        for index, question in enumerate(questions):
            answer = answers[index] if index < len(answers) else ""
            feedback = self._generate_feedback(question, answer)
            evaluation = self._evaluate_answer(question, answer)
            history.append(
                InterviewHistoryRecord(
                    question=question.question,
                    topic=question.topic,
                    answer=answer,
                    evaluation=evaluation,
                    feedback=feedback,
                )
            )

        logger.info("Simulated interview flow for %d questions", len(history))
        return history

    def _evaluate_answer(self, question: InterviewQuestion, answer: str) -> EvaluationMetrics:
        tokens = answer.split()
        length = len(tokens)
        lower_answer = answer.lower()
        topic_bonus = 8.0 if question.topic.lower() in lower_answer else 0.0
        example_bonus = 6.0 if any(keyword in lower_answer for keyword in ["example", "for instance", "such as"]) else 0.0
        tradeoff_bonus = 5.0 if any(keyword in lower_answer for keyword in ["trade-off", "tradeoff", "pros", "cons"]) else 0.0
        confidence_bonus = 15.0 if any(keyword in lower_answer for keyword in ["confident", "certain", "sure"]) else 0.0

        correctness = min(100.0, 35.0 + length * 1.8 + topic_bonus)
        depth = min(100.0, 30.0 + length * 1.6 + example_bonus + tradeoff_bonus)
        communication = min(100.0, 40.0 + min(length, 80) * 0.9)
        confidence = min(100.0, 40.0 + confidence_bonus + (3.0 if length > 40 else 0.0))
        problem_solving = min(100.0, 32.0 + length * 1.5 + tradeoff_bonus)

        return EvaluationMetrics(
            correctness=round(correctness, 1),
            depth=round(depth, 1),
            communication=round(communication, 1),
            confidence=round(confidence, 1),
            problem_solving=round(problem_solving, 1),
        )

    def _generate_feedback(self, question: InterviewQuestion, answer: str) -> str:
        if not answer.strip():
            return (
                f"For {question.topic}, provide a concrete answer with an example, the trade-offs, and the production impact."
            )

        feedback_parts = [
            f"For {question.topic}, your response covered the main idea.",
        ]
        if len(answer.split()) < 25:
            feedback_parts.append("Add more implementation detail and a specific example.")
        if "example" not in answer.lower() and "for instance" not in answer.lower():
            feedback_parts.append("Include an example or case study to improve depth.")
        if "trade-off" not in answer.lower() and "tradeoff" not in answer.lower():
            feedback_parts.append("Discuss trade-offs, limitations, and failure modes.")
        return " ".join(feedback_parts)
