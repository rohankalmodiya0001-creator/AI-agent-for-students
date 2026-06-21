"""Skill gap detection and readiness scoring utilities."""

from __future__ import annotations

from ..app_logging import logger
from ..models.schema import JobDescriptionProfile, ResumeProfile, SkillGapReport


class SkillGapService:
    """Compare resume and job description profiles to produce an action plan."""

    def compare_profiles(
        self,
        resume: ResumeProfile,
        job_description: JobDescriptionProfile,
    ) -> SkillGapReport:
        if not resume.skills and not resume.technologies:
            raise ValueError("Resume profile must contain at least one skill or technology")
        if not job_description.required_skills and not job_description.technologies:
            raise ValueError("Job description profile must contain at least one skill or technology")

        resume_skills = {skill.lower() for skill in resume.skills}
        jd_skills = {skill.lower() for skill in job_description.required_skills}
        resume_tech = {tech.lower() for tech in resume.technologies}
        jd_tech = {tech.lower() for tech in job_description.technologies}

        matched_skills = sorted(resume_skills.intersection(jd_skills))
        missing_skills = sorted(jd_skills.difference(resume_skills))
        missing_tech = sorted(jd_tech.difference(resume_tech))
        strengths = sorted(resume_skills.intersection(jd_skills) | resume_tech.intersection(jd_tech))
        weak_skills = sorted(skill for skill in matched_skills if skill not in resume_tech)

        total_required = len(jd_skills | jd_tech)
        matched = len((resume_skills & jd_skills) | (resume_tech & jd_tech))
        match_score = self._calculate_match_score(total_required=total_required, matched=matched)
        readiness_score = self._calculate_readiness_score(
            match_score=match_score,
            weak_count=len(weak_skills),
            missing_count=len(missing_skills) + len(missing_tech),
        )

        logger.info(
            "Computed skill gap report: match=%.1f readiness=%.1f missing=%d weak=%d",
            match_score,
            readiness_score,
            len(missing_skills) + len(missing_tech),
            len(weak_skills),
        )

        summary = (
            f"The candidate matched {len(strengths)} areas, has {len(missing_skills) + len(missing_tech)} gaps, "
            f"and {len(weak_skills)} weak skills. Readiness score: {readiness_score:.1f}."
        )

        return SkillGapReport(
            missing_skills=missing_skills + missing_tech,
            weak_skills=weak_skills,
            strengths=strengths,
            match_score=match_score,
            readiness_score=readiness_score,
            summary=summary,
        )

    def _calculate_match_score(self, total_required: int, matched: int) -> float:
        if total_required <= 0:
            return 0.0
        return min(100.0, round((matched / total_required) * 100, 1))

    def _calculate_readiness_score(self, match_score: float, weak_count: int, missing_count: int) -> float:
        penalty = weak_count * 3.0 + missing_count * 5.0
        return max(0.0, round(match_score - penalty, 1))
