"""JSON-backed persistent memory for interview session history."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from ..database import DATABASE_PATH


BASE_DIR = (DATABASE_PATH.parent if DATABASE_PATH is not None else Path("src/data")).resolve()
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_FILE = MEMORY_DIR / "memory.json"


def _load_memory() -> Dict[str, Any]:
    if not MEMORY_FILE.exists():
        return {}

    with MEMORY_FILE.open("r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return {}

    if isinstance(data, dict):
        return data
    return {}


def _save_memory(data: Dict[str, Any]) -> None:
    with MEMORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def save_session_memory(session_id: str, record: Dict[str, Any]) -> None:
    memory = _load_memory()
    memory[session_id] = memory.get(session_id, [])
    memory[session_id].append(record)
    _save_memory(memory)


def get_session_memory(session_id: str) -> List[Dict[str, Any]]:
    memory = _load_memory()
    return memory.get(session_id, [])
