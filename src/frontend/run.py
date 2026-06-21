"""Convenience launcher for the Streamlit frontend."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "src" / "frontend" / "app.py"


if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(APP_PATH)], check=True)
