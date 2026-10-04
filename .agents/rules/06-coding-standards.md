# Rule 06 — Coding Standards (Always On)

- Python 3.11+, full type hints, `mypy --strict`-friendly where practical. Pydantic v2 for all boundary data.
- Format/lint: `ruff` (lint + format). Zero warnings before declaring a phase done.
- Small functions, single responsibility, no global mutable state; inject dependencies (engine, provider, config).
- Typed custom exceptions in `app/core/errors.py`; convert to user-safe messages only in the API layer.
- Use `structlog` JSON logging with a request/session id; no `print`.
- Docstrings on public classes/functions; comments explain *why*, not *what*.
- SQL via SQLAlchemy `text()` only for validated generated SQL; any app-authored SQL must be parameterized.
- Keep files < ~300 lines; split when larger.
- No dead code, no TODOs left without a tracked note in `docs/DECISIONS.md`.
- Never hard-code secrets, hosts, model names, or table/column names.
