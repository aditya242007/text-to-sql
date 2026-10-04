# 01 — Project Context (Always On)

Source of truth: `docs/PRD.md`. Read it before any task and re-read the relevant section before each phase.

## Mission
Build a reliable **ambiguity-aware natural-language-to-SQL system** that lets non-technical users query a PostgreSQL analytics database in plain English:
Natural Language → Intent → Ambiguity Resolution → SQL → Validation → Execution → Natural-Language Insight.
The system must be **safe** (read-only, validated SQL), **accurate** (deterministic where possible) and **honest** (clarify rather than guess).

## Core Principles
| # | Principle | Meaning |
|---|-----------|---------|
| 1 | **Safety first** | No query may mutate data. Every generated SQL is validated before execution. |
| 2 | **Clarify, don't guess** | When multiple reasonable interpretations produce different answers, ask the user. Never guess. Correctness over answering every question. |
| 3 | **Provider independence** | The LLM is a swappable component behind an abstraction. No vendor lock-in. |
| 4 | **Determinism over creativity** | `temperature=0` for intent/SQL; Pydantic contracts on every LLM response. |
| 5 | **Phased delivery** | 12 phases (0–11) per `docs/PHASE_PROMPTS.md`. Build ONLY the current phase. After it, summarize and STOP; wait for user approval before the next phase. |

## Fixed Technology Stack
> [!CAUTION]
> Do **not** introduce any dependency outside this list without stating why and getting explicit user approval.

| Layer | Technology | Note |
|-------|-----------|------|
| Language | Python 3.11+ | |
| API | FastAPI + uvicorn | sync endpoints by default |
| DB toolkit | SQLAlchemy 2 | sync by default; used for introspection and executing validated SQL only |
| DB driver | psycopg 3 (`psycopg[binary]`) | |
| Database | PostgreSQL 16 | Docker Compose |
| Contracts | Pydantic v2 + pydantic-settings | every LLM response is a Pydantic model |
| SQL parsing | sqlglot | AST-based validation |
| Config | pydantic-settings + PyYAML + `.env` | |
| Logging / retry | structlog, tenacity | |
| LLM SDKs | google-genai, openai, groq | imported only inside `app/llm/` |
| HTTP client | httpx | API tests and UI→API calls |
| UI (MVP) | Streamlit (+ pandas) | chat UI calling the FastAPI API only |
| Testing / quality | pytest, pytest-cov, ruff, mypy | see `07-testing-and-done` |
| Packaging | pyproject.toml, Docker Compose | |

## Seed Data Requirements
Realistic, deterministic (seeded RNG): ≥ 5,000 customers, ≥ 50,000 orders (all statuses), Indian cities and states, ~24 months of history including the previous full calendar month.

## Scope Limits
- The LLM produces raw SQL, validated by sqlglot; do not build a query-builder/ORM layer for analytics.
- No direct database writes; the app executes through a read-only role.
- No frontend beyond Streamlit for the MVP.
- No extra structured-output libraries (e.g. `instructor`); the provider-agnostic layer is our own code.
- No provider SDK imports outside `app/llm/`.
- Out of scope for the MVP: agent frameworks, vector DBs, RAG, fine-tuning, multiple databases, write access, data pipelines, enterprise auth/SSO, BI features.
- If the PRD is ambiguous or conflicts with a prompt, STOP and ask the user instead of choosing silently.
