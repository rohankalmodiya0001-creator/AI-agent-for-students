"""Final report synthesis for interview readiness outcomes."""

from __future__ import annotations

from ..app_logging import logger
from ..models.schema import PerformanceTrend, SkillGapReport


class ReportService:
    """Generate a structured final readiness summary from gap and trend data."""

    def generate_report(self, skill_gap: SkillGapReport, trends: PerformanceTrend) -> str:
        logger.info(
            "Generating final report with readiness=%.1f and technical score=%.1f",
            skill_gap.readiness_score,
            trends.technical_score,
        )

        strengths = ", ".join(skill_gap.strengths) if skill_gap.strengths else "None"
        missing_skills = ", ".join(skill_gap.missing_skills) if skill_gap.missing_skills else "None"
        weak_skills = ", ".join(skill_gap.weak_skills) if skill_gap.weak_skills else "None"
        weak_topics = ", ".join(trends.weak_topics) if trends.weak_topics else "None"
        strong_topics = ", ".join(trends.strong_topics) if trends.strong_topics else "None"

        readiness_label = self._readiness_label(trends.readiness_score)
        action_plan = self._build_action_plan(skill_gap, trends)

        report_lines = [
            "Final Interview Readiness Report",
            "",
            f"Overall readiness: {readiness_label} ({trends.readiness_score:.1f}/100)",
            f"Match score: {skill_gap.match_score:.1f}/100",
            f"Technical score: {trends.technical_score:.1f}/100",
            f"Communication score: {trends.communication_score:.1f}/100",
            f"Problem solving score: {trends.problem_solving_score:.1f}/100",
            f"Confidence score: {trends.confidence_score:.1f}/100",
            "",
            f"Strengths: {strengths}",
            f"Missing skills: {missing_skills}",
            f"Weak skills: {weak_skills}",
            f"Weak topics: {weak_topics}",
            f"Strong topics: {strong_topics}",
            "",
            f"Summary: {skill_gap.summary}",
            "",
            "Action Plan:",
            action_plan,
        ]
        return "\n".join(report_lines)

    def _readiness_label(self, readiness_score: float) -> str:
        if readiness_score >= 85:
            return "Interview ready"
        if readiness_score >= 70:
            return "Nearly ready"
        if readiness_score >= 50:
            return "Needs focused practice"
        return "Needs substantial preparation"

    def _build_action_plan(self, skill_gap: SkillGapReport, trends: PerformanceTrend) -> str:
        focus_topics = skill_gap.weak_skills or trends.weak_topics or skill_gap.missing_skills
        if focus_topics:
            topic_text = ", ".join(focus_topics[:5])
        else:
            topic_text = "review the core interview domains"

        return (
            f"1. Prioritize: {topic_text}.\n"
            f"2. Reinforce strengths in {', '.join(trends.strong_topics) if trends.strong_topics else 'your strongest interview areas'}.\n"
            "3. Run repeat mock interviews until readiness improves by at least 10 points.\n"
            "4. Collect follow-up notes after each interview and update the roadmap weekly."
        )
