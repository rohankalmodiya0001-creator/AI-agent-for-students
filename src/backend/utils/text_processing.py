"""Lightweight rule-based extraction helpers for resume and JD text."""

from __future__ import annotations

import re
from typing import Dict, List


SKILL_PATTERNS = [
    r"machine learning",
    r"deep learning",
    r"natural language processing",
    r"python",
    r"sql",
    r"docker",
    r"kubernetes",
    r"pytorch",
    r"tensorflow",
    r"langchain",
    r"chromadb",
    r"prompt engineering",
    r"vector database",
    r"mlops",
]

PROJECT_PATTERNS = [
    r"project[s]?",
    r"built",
    r"developed",
    r"designed",
    r"implemented",
]

RESPONSIBILITY_PATTERNS = [
    r"responsible for",
    r"experience with",
    r"lead",
    r"collaborated",
    r"owned",
]

SENIORITY_PATTERNS = [
    r"senior",
    r"lead",
    r"staff",
    r"principal",
    r"junior",
    r"associate",
]


def _clean_text(value: str) -> str:
    return (value or "").lower().strip().replace("\n", " ")


def _extract_matches(patterns: List[str], text: str) -> List[str]:
    found = set()
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            found.add(match.group(0).lower())
    return sorted(list(found))


def extract_entities_from_text(text: str) -> Dict[str, List[str]]:
    normalized = _clean_text(text)
    skills = _extract_matches(SKILL_PATTERNS, normalized)
    technologies = [skill for skill in skills if skill not in {"project", "responsible for"}]
    responsibilities = _extract_matches(RESPONSIBILITY_PATTERNS, normalized)
    seniority = _extract_matches(SENIORITY_PATTERNS, normalized)
    projects = []
    certifications = []
    keywords = []

    project_matches = re.findall(r"(?:project|projects)[^\n\.]{0,120}", normalized)
    for match in project_matches:
        if match not in projects:
            projects.append(match.strip())

    certification_matches = re.findall(r"(?:certified|certification|certificate)[^\n\.]{0,80}", normalized)
    for match in certification_matches:
        if match not in certifications:
            certifications.append(match.strip())

    keyword_matches = re.findall(r"\b(machine learning|deep learning|llm|rag|prompt engineering|mlo?ps|system design|data science|python|sql)\b", normalized)
    for match in keyword_matches:
        if match not in keywords:
            keywords.append(match)

    experience_sentences = [sentence.strip() for sentence in re.split(r"[\n\.]+", normalized) if len(sentence.strip()) > 40]
    if not experience_sentences and normalized:
        experience_sentences = [normalized[:200]]

    return {
        "skills": skills,
        "projects": projects,
        "experience": experience_sentences[:5],
        "certifications": certifications,
        "technologies": technologies,
        "responsibilities": responsibilities,
        "seniority_level": seniority[0] if seniority else "Mid",
        "keywords": keywords,
    }
