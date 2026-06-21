"""Job description parsing and structured extraction utilities."""

from __future__ import annotations

from ..app_logging import logger
from ..models.schema import JobDescriptionProfile
from ..utils.text_processing import extract_entities_from_text


class JobDescriptionService:
    """Parse a job description and extract structured hiring requirements."""

    def parse_job_description(self, text: str) -> JobDescriptionProfile:
        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("Job description text cannot be empty")

        logger.info("Parsing job description text (%d characters)", len(normalized_text))
        entities = extract_entities_from_text(normalized_text)

        return JobDescriptionProfile(
            required_skills=entities.get("skills", []),
            technologies=entities.get("technologies", []),
            responsibilities=entities.get("responsibilities", []),
            seniority_level=entities.get("seniority_level", "Mid"),
            keywords=entities.get("keywords", []),
            raw_text=normalized_text,
        )
