# Rule 04 — Ambiguity Handling (Always On)

This is the product differentiator. Treat it as the most important behavior.

## Detection
- Maintain `app/semantics/ambiguity_registry.yaml` (terms: best, worst, top, popular, active, valuable, successful, loyal, engaged, high-performing, …) with candidate interpretations.
- Filter candidate options by what the schema can actually support (no "Most visits" if there is no visits table).
- Ambiguity exists ONLY if interpretations would materially change the SQL/result. Do not over-ask:
  - "Top 5 products by revenue" → NOT ambiguous.
  - "Best customer" / "most active customer" / "most valuable customer" → ambiguous.
- The LLM may flag unregistered ambiguity but must give a `reason`.

## Behavior
- Status `clarification_required` ⇒ `sql` MUST be `None`. Enforce with a Pydantic model validator AND an orchestrator guard. SQL generation must be unreachable in that state.
- Ask exactly one short, plain-language question with 2–5 options (+ optional free text). No technical jargon.
- Max 2 clarification rounds per query; after that, ask the user to rephrase.
- Store the user's choice in session context and reuse it for follow-ups.
- Disclose safe defaults (e.g. "revenue counts completed orders only") in `assumptions`.

## Tests required
Golden tests in BOTH directions: ambiguous set → must clarify (100%); clear set → must NOT clarify (≤5% false positives).
