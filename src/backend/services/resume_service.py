"""Resume parsing and structured extraction utilities."""

from __future__ import annotations

from pathlib import Path

from ..app_logging import logger
from ..models.schema import ResumeProfile
from ..utils.pdf_parser import extract_text_from_pdf
from ..utils.text_processing import extract_entities_from_text


class ResumeService:
    """Parse a candidate resume and extract structured profile data."""

    def parse_resume(self, file_path: str) -> ResumeProfile:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Resume must be a PDF file: {file_path}")

        logger.info("Parsing resume from %s", path)
        raw_text = extract_text_from_pdf(str(path))
        return self.parse_resume_text(raw_text)

    def parse_resume_text(self, raw_text: str) -> ResumeProfile:
        """Build a structured resume profile from extracted resume text."""

        entities = extract_entities_from_text(raw_text)
        experience = entities.get("experience", [])

        return ResumeProfile(
            skills=entities.get("skills", []),
            projects=entities.get("projects", []),
            experience="\n".join(experience) if isinstance(experience, list) else str(experience),
            certifications=entities.get("certifications", []),
            technologies=entities.get("technologies", []),
            raw_text=raw_text,
        )
