# Rule 02 — Architecture & Layering (Always On)

## Layout (follow PRD §11 exactly)
`app/{api,core,llm,db,semantics,timeutil,pipeline,sql,conversation,prompts}`, `ui/`, `db/`, `tests/{unit,integration,golden}`.

## Layering (dependencies point downward only)
api → pipeline → (llm, sql, db, semantics, timeutil, conversation) → core
- `core` (Pydantic schemas, enums, errors) imports nothing from the app.
- `api` contains no business logic — only validation, calling the orchestrator, serialization.
- `pipeline/orchestrator.py` is the ONLY place that sequences pipeline steps.
- Each pipeline step is a small class/function with one responsibility and explicit typed input/output.

## Provider independence
- All LLM calls go through `app/llm/base.py::LLMProvider`. Never import `google.generativeai`, `openai`, or `groq` outside `app/llm/`.
- Provider chosen via config (`LLM_PROVIDER`, `LLM_MODEL`); fallback chain optional.

## Config & secrets
- All settings via `app/config.py` (pydantic-settings) from env. Provide `.env.example`. Never commit `.env`.
- No hard-coded table or column names in Python logic. Schema comes from introspection; business meaning from `app/semantics/*.yaml`.

## Prompts
- Prompts live in `app/prompts/*.md`, loaded by a loader, with placeholders. No large inline prompt strings in code.

## Determinism
- Date/time resolution is done in Python (`app/timeutil`), never by the LLM.
- LLM temperature 0 for intent, ambiguity, planning, SQL.
