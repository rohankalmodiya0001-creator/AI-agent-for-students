"""Adaptive interview question generation utilities."""

from __future__ import annotations

from typing import List

from ..agents.research_agent import ResearchAgent
from ..app_logging import logger
from ..models.schema import InterviewQuestion, SkillGapReport


class InterviewService:
    CORE_TOPICS = [
        "machine learning",
        "data science",
        "deep learning",
        "llm",
        "rag",
        "mlops",
        "python",
        "system design",
    ]

    def __init__(self) -> None:
        self.research_agent = ResearchAgent()

    def generate_questions(self, skill_gap: SkillGapReport, interview_type: str) -> List[InterviewQuestion]:
        topics = self._build_topic_set(skill_gap, interview_type)
        query = self._build_query(skill_gap, interview_type)
        context = self.research_agent.retrieve_learning_context(query, topics)
        logger.info("Generating %s interview questions for topics: %s", interview_type, ", ".join(topics))
        return self._build_questions(topics, context)

    def _build_query(self, skill_gap: SkillGapReport, interview_type: str) -> str:
        weak_focus = ", ".join(skill_gap.weak_skills[:3]) if skill_gap.weak_skills else ""
        base_query = f"Generate interview questions for {interview_type}"
        return f"{base_query} focusing on weak skills: {weak_focus}".strip()

    def _build_topic_set(self, skill_gap: SkillGapReport, interview_type: str) -> List[str]:
        selected: List[str] = []
        interview_topic = interview_type.strip().lower()
        if interview_topic:
            selected.append(interview_topic)

        for skill in skill_gap.weak_skills:
            normalized = skill.strip().lower()
            if normalized and normalized not in selected:
                selected.append(normalized)

        for topic in self.CORE_TOPICS:
            if len(selected) >= 6:
                break
            if topic not in selected and (topic == interview_topic or topic in skill_gap.weak_skills or not skill_gap.weak_skills):
                selected.append(topic)

        if not selected:
            selected.append("machine learning")
        return selected[:6]

    def _build_questions(self, topics: List[str], context: str) -> List[InterviewQuestion]:
        questions: List[InterviewQuestion] = []
        context_preview = context.strip().splitlines()[0] if context.strip() else ""

        for index, topic in enumerate(topics):
            question_text = f"Describe a practical design or implementation pattern for {topic}."
            if context_preview:
                question_text += f" Use this context as a starting point: {context_preview[:180]}"

            questions.append(
                InterviewQuestion(
                    question=question_text,
                    topic=topic,
                    difficulty="medium" if index < 3 else "hard",
                    follow_up=(
                        "How would you extend this approach for a large-scale production system?"
                        if index % 2 == 0
                        else "What are the main failure modes and how would you mitigate them?"
                    ),
                )
            )

        if not questions:
            questions.append(
                InterviewQuestion(
                    question="Describe your approach to designing a production-ready machine learning system.",
                    topic="machine learning",
                    difficulty="medium",
                )
            )
        return questions
