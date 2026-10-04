"""Typed custom exceptions for the analytics pipeline.

All exceptions here are domain errors raised by internal services.
The API layer catches them and converts to user-safe HTTP responses.
Never leak raw DB errors or stack traces to the end user.
"""

from __future__ import annotations


class AppError(Exception):
    """Base class for all application-level errors."""

    pass


class UnsafeSQLError(AppError):
    """Raised when generated SQL contains disallowed constructs (writes, DDL, etc.).

    This is a hard-stop: the SQL must never be executed.
    """

    pass


class LLMOutputError(AppError):
    """Raised when the LLM returns output that fails Pydantic validation after one retry.

    The caller (orchestrator / API layer) must handle this gracefully.
    """

    pass


class SchemaNotFoundError(AppError):
    """Raised when a referenced table or column is not found in the introspected schema."""

    pass


class AmbiguityError(AppError):
    """Raised when a question is ambiguous and cannot proceed without clarification.

    This should trigger a ClarificationResponse, not an error message.
    """

    pass


class PipelineError(AppError):
    """Generic pipeline error for unexpected failures that are not covered above."""

    pass


class ConfigurationError(AppError):
    """Raised when the application configuration is invalid or incomplete."""

    pass
