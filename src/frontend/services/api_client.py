"""Shared API and local storage helpers for the Streamlit frontend."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

import httpx

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")


def post(endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{API_BASE_URL}/{endpoint}"
    with httpx.Client(timeout=30) as client:
        response = client.post(url, json=payload)
        response.raise_for_status()
        return response.json()


def save_json(filename: str, content: Any) -> None:
    path = DATA_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, indent=2), encoding="utf-8")


def load_json(filename: str) -> Any:
    path = DATA_DIR / filename
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
