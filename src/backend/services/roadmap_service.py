"""Learning roadmap generation for interview preparation."""

from __future__ import annotations

from typing import List, Optional

from ..app_logging import logger
from ..models.schema import PerformanceTrend, SkillGapReport


class RoadmapService:
    """Convert skill gaps and interview trends into an ordered study plan."""

    def generate_roadmap(
        self,
        skill_gap: SkillGapReport,
        trends: Optional[PerformanceTrend] = None,
        interview_type: str | None = None,
    ) -> List[str]:
        if not skill_gap.missing_skills and not skill_gap.weak_skills and not (trends and trends.weak_topics):
            return [
                "Review your strongest topics to keep interview confidence high.",
                "Run a short mock interview to confirm your current readiness level.",
            ]

        roadmap: List[str] = []
        focus_topics = self._ordered_focus_topics(skill_gap, trends)
        interview_label = interview_type or "technical"

        roadmap.append(f"Start with {interview_label} interview questions that target {focus_topics[0]}.")
        roadmap.append("Review matched strengths to reinforce domain confidence and sharpen explanations.")

        if skill_gap.missing_skills:
            roadmap.append(
                "Study missing skills in priority order: " + ", ".join(skill_gap.missing_skills[:5])
            )

        if skill_gap.weak_skills:
            roadmap.append(
                "Practice weak skills through short drills and follow-up questions: "
                + ", ".join(skill_gap.weak_skills[:5])
            )

        if trends and trends.weak_topics:
            roadmap.append(
                "Revisit weak interview topics after each mock session: " + ", ".join(trends.weak_topics[:5])
            )

        roadmap.append(
            "Use RAG-backed learning material for each topic to ground explanations in examples, trade-offs, and best practices."
        )
        roadmap.append(
            "Schedule another mock interview after the study block and compare your new scores to previous performance."
        )

        logger.info("Generated roadmap with %d steps", len(roadmap))
        return roadmap

    def _ordered_focus_topics(
        self,
        skill_gap: SkillGapReport,
        trends: Optional[PerformanceTrend] = None,
    ) -> List[str]:
        topics: List[str] = []
        for candidate in list(skill_gap.weak_skills) + list(skill_gap.missing_skills):
            normalized = candidate.strip().lower()
            if normalized and normalized not in topics:
                topics.append(normalized)

        if trends:
            for candidate in trends.weak_topics:
                normalized = candidate.strip().lower()
                if normalized and normalized not in topics:
                    topics.append(normalized)

        if skill_gap.strengths:
            for candidate in skill_gap.strengths:
                normalized = candidate.strip().lower()
                if normalized and normalized not in topics:
                    topics.append(normalized)

        return topics or ["machine learning"]
