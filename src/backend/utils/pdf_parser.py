"""PDF extraction helpers used by the resume analysis service."""

from __future__ import annotations

from pathlib import Path
from typing import List

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file: {file_path}")

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        raise ValueError(f"Unable to read PDF file: {file_path}") from exc

    content_parts: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            content_parts.append(text)
    return "\n".join(content_parts).strip()
