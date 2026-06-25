"""Top-level FastAPI entrypoint.

Some deployment platforms auto-detect FastAPI apps only from default locations.
This module re-exports the actual application from `backend.api.app`.

Deployment tools can import `app` from `src/app.py`.
"""

from backend.api.app import app, create_app  # noqa: F401

