# Project Progress

## Phase 0 — Foundation
- **Status:** ✅ Complete
- **Branch:** `phase/0-foundation`
- **Date:** 2026-10-04

### What was built
- Full package layout matching PRD §11: `app/{api,core,llm,db,semantics,timeutil,pipeline,sql,conversation,prompts}`, `ui/`, `db/`, `tests/{unit,integration,golden}`.
- `pyproject.toml` with all runtime + dev dependencies, ruff config (target py311, line-length 100), pytest markers (`integration`, `live_llm`).
- `.env.example` with every required key documented.
- `Makefile` with `install`, `lint`, `test`, `run-api`, `run-ui`, `db-up` — all using `.venv/bin/` explicitly; `PIP_CACHE_DIR` set to external drive.
- `app/config.py` — pydantic-settings `Settings` singleton.
- `app/core/errors.py` — typed exception hierarchy: `UnsafeSQLError`, `LLMOutputError`, `SchemaNotFoundError`, `AmbiguityError`, `PipelineError`, `ConfigurationError`.
- `app/core/logging.py` — structlog setup (JSON / console).
- `app/main.py` — FastAPI app with `GET /api/v1/health`.
- `app/api/health.py` — health router.
- `tests/conftest.py` — session-scoped `TestClient` fixture.
- `tests/unit/test_health.py` — 2 smoke tests.
- `ui/streamlit_app.py` — Phase 9 placeholder.

### How to run
```bash
# Install
make install

# Lint
make lint

# Test
make test

# Start API
make run-api
# → http://localhost:8000/api/v1/health
# → http://localhost:8000/docs
```

### Test results (real output — see phase summary)
All tests pass; ruff clean.

### Known gaps / decisions
- See `docs/DECISIONS.md`.
- Docker Compose not yet needed (Phase 1).
- No pipeline logic — intentionally out of scope.

---

## Phase 1 — Database, Read-Only Role & Seed Data
- **Status:** ⬜ Not Started

## Phase 2 — Contracts, Semantics Registry & Business Definitions
- **Status:** ⬜ Not Started

## Phase 3 — LLM Provider Abstraction
- **Status:** ⬜ Not Started

## Phase 4 — Schema Introspection & Deterministic Time Resolver
- **Status:** ⬜ Not Started

## Phase 5 — Intent Parsing & Ambiguity Detection
- **Status:** ⬜ Not Started

## Phase 6 — SQL Planning, Generation, Safety Validation, Execution & Repair
- **Status:** ⬜ Not Started

## Phase 7 — Orchestrator & Conversation Context
- **Status:** ⬜ Not Started

## Phase 8 — FastAPI Layer
- **Status:** ⬜ Not Started

## Phase 9 — Streamlit Chat UI
- **Status:** ⬜ Not Started

## Phase 10 — Evaluation, Security Review & Hardening
- **Status:** ⬜ Not Started

## Phase 11 — Documentation, Packaging & Release
- **Status:** ⬜ Not Started
