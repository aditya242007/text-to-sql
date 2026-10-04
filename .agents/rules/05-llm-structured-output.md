# Rule 05 — LLM Interaction & Structured Output (Always On)

- Every LLM call returns a **Pydantic model** via `LLMProvider.generate_structured(...)`. No parsing free text for internal logic.
- Use native JSON-schema/structured output when the provider supports it; otherwise JSON mode + Pydantic validation + ONE repair retry; then raise a typed `LLMOutputError`.
- Prompts must state: never invent tables/columns; use only the provided schema; never assume an undefined business metric; PostgreSQL only; no destructive SQL; return only the schema'd JSON.
- Prompts receive: schema context, business definitions, resolved date ranges (literals), resolved clarifications, and conversation context. They never receive credentials or raw rows beyond what the explainer needs.
- Result explanation uses ONLY the rows returned; never invent or round numbers silently.
- Retry transient provider errors with exponential backoff (tenacity); optionally fall back to the next provider.
- Unit tests use a `FakeLLMProvider` returning canned Pydantic objects — no network in unit tests.
- Log provider, model, latency, token counts; never log API keys.
