"""Application logging configuration for the interview coach backend."""

from __future__ import annotations

import logging

from rich.logging import RichHandler

from .config import config


LOGGER_NAME = "rag_interview_coach"


def _resolve_level(level_name: str) -> int:
    """Translate the configured log level into a logging module constant."""

    return getattr(logging, level_name.upper(), logging.INFO)


def configure_logging() -> logging.Logger:
    """Configure root logging once and return the application logger.

    The function is safe to call multiple times. Existing handlers are reused so
    re-importing backend modules does not duplicate log lines.
    """

    level = _resolve_level(config.log_level)
    root_logger = logging.getLogger()

    if not any(isinstance(handler, RichHandler) for handler in root_logger.handlers):
        rich_handler = RichHandler(markup=True, show_time=False, rich_tracebacks=True)
        rich_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S")
        )
        root_logger.addHandler(rich_handler)

    root_logger.setLevel(level)

    application_logger = logging.getLogger(LOGGER_NAME)
    application_logger.setLevel(level)
    application_logger.propagate = True
    return application_logger


logger = configure_logging()