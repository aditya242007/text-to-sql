"""Structlog configuration for the analytics application.

Call ``configure_logging()`` once at startup (in ``app/main.py``).
All subsequent ``structlog.get_logger()`` calls will use this configuration.

Key decisions:
- JSON renderer in production; pretty ``ConsoleRenderer`` when LOG_FORMAT=console.
- Request/session IDs are injected via context variables (added by middleware).
- Secrets must never appear in log entries — validate this at the call site.
"""

from __future__ import annotations

import logging
import sys

import structlog


def configure_logging(*, log_level: str = "INFO", log_format: str = "json") -> None:
    """Configure structlog with shared processors and the chosen renderer.

    Args:
        log_level: Standard logging level string (e.g. "INFO", "DEBUG").
        log_format: "json" (default, production) or "console" (development).
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    if log_format == "console":
        renderer: structlog.types.Processor = structlog.dev.ConsoleRenderer()
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level.upper())
