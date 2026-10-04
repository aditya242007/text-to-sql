# PRD — Ambiguity-Aware AI SQL Analytics System
**Version:** 1.0 (Final, MVP) | **Status:** Approved for build

---

## 1. Summary
A conversational analytics system that lets non-technical users ask business questions in natural language and get safe, correct answers from a PostgreSQL database.

Unlike plain Text-to-SQL, the system first decides whether the question is **sufficiently defined**. If a business term (e.g. "best", "active", "valuable") has multiple reasonable interpretations that produce different answers, it **asks the user to choose** before any SQL is generated.

**Pipeline:** Natural Language → Intent → Ambiguity Resolution → SQL → Validation → Execution → Natural-Language Insight

**One-line definition:** An ambiguity-aware conversational AI system that converts business questions into safe, schema-aware, read-only PostgreSQL queries, interactively resolves unclear intent, and returns human-readable insights.

## 2. Goals / Non-Goals
### Goals (MVP)
1. Correct interpretation of intent; correctness > answering everything.
2. Explicit, option-based clarification for material ambiguity.
3. Schema-aware SQL (schema introspected dynamically, never hard-coded).
4. Structured, Pydantic-validated LLM output at every internal boundary.
5. Defense-in-depth read-only SQL safety.
6. Multi-turn follow-ups ("What about Delhi?").
7. Human-readable answers + optional SQL, table, chart.
8. Provider-agnostic LLM layer (Gemini / OpenAI / Groq).

### Non-Goals (MVP)
Autonomous agents, vector DB / RAG, fine-tuning, multiple databases, write access, data pipelines, enterprise auth/SSO, full BI features.

## 3. Users
Business analysts, PMs, ops, sales, marketing, managers, students, non-technical users; technical users for fast exploration.

## 4. Key User Stories
| ID | Story | Acceptance |
|----|-------|-----------|
| US-1 | Ask a clear question, get an answer | "How many customers signed up last month?" → single number + optional SQL |
| US-2 | Ambiguous question triggers clarification | "Show the best customer last month" → no SQL; options shown |
| US-3 | Answer clarification, get result | Selecting "Highest revenue" → SQL runs → named customer + amount |
| US-4 | Follow-up using context | "How many were from Punjab?" reuses entity/metric/time, adds filter |
| US-5 | Transparency | User can expand "View SQL" and see assumptions used |
| US-6 | Graceful failures | Unknown question, missing data, empty result, SQL error handled without fabrication |
| US-7 | Table/chart | Multi-row results show a table; time series show a line chart |

## 5. System Flow
```
User question
  → Context merge (session state)
  → Time Resolver (deterministic, Python)
  → Intent Parser (LLM, structured)
  → Ambiguity Detector (registry + LLM, structured)
        ├─ Ambiguous → Clarification response (STOP; wait for user)
        └─ Clear
  → Schema Context Builder (introspection, relevant subset)
  → SQL Planner (LLM, structured plan)
  → SQL Generator (LLM, structured)
  → Pydantic validation
  → SQL Safety Validator (AST-based)
  → Executor (read-only role, timeout, row limit)
        ├─ Error → Repair (max 2 retries) → re-validate
        └─ Result
  → Result Explainer (LLM, from actual rows only)
  → Response (answer + optional SQL/table/chart)
```

## 6. Functional Requirements

### 6.1 Intent Understanding (FR-INT)
- FR-INT-1: Extract entity, metric, aggregation, filters, time period, grouping, ranking, sorting, limit, output type.
- FR-INT-2: Output is a Pydantic `Intent` model; invalid output triggers a bounded retry.
- FR-INT-3: Distinguish **calendar** periods (last month = previous calendar month) from **rolling** periods (last 30 days).

### 6.2 Ambiguity Detection (FR-AMB)
- FR-AMB-1: A **Business Semantics Registry** (`ambiguity_registry.yaml`) lists ambiguous terms (best, worst, top, popular, active, valuable, successful, loyal, engaged, high-performing) with candidate interpretations.
- FR-AMB-2: Candidate options are **filtered by schema capability** (e.g. "Most visits" only offered if `store_visits` exists).
- FR-AMB-3: The LLM may flag ambiguity not in the registry, but must justify it in `reason`.
- FR-AMB-4: Ambiguity is raised only when interpretations **materially change the result**. "Top 5 products by sales" is NOT ambiguous (metric given).
- FR-AMB-5: Ask only the minimum necessary question; max 1 clarification question per turn, max 2 rounds per query.
- FR-AMB-6: Clarification text is short, plain-language, no jargon; 2–5 options plus optional "Something else" free-text.
- FR-AMB-7: **No SQL may be generated while `status = clarification_required`.** Enforced in code, not only in prompt.
- FR-AMB-8: Resolved clarifications are stored in session context and reused until the user changes them.

### 6.3 Business Definitions (FR-DEF)
Metrics have canonical definitions in `business_definitions.yaml` (single source of truth):
- *Revenue* = `SUM(orders.amount)` where `orders.status` in configured "counted" statuses (default: `completed`).
- *Orders count* = `COUNT(DISTINCT orders.order_id)` with same status filter.
- *Products purchased* = `SUM(order_items.quantity)`.
- *Visits* = `COUNT(store_visits.visit_id)`.
- *New customers* = `COUNT(customers.customer_id)` by `signup_date`.

Safe, unavoidable defaults (e.g. excluding cancelled orders) are applied AND disclosed in `assumptions`. If a default would materially change the answer and is not configured, treat it as ambiguity.

### 6.4 Time Resolution (FR-TIME)
- Deterministic Python resolver (not LLM) converts expressions to explicit half-open ranges `[start, end)`.
- Supports: today, yesterday, this/last week (ISO Monday start), this/last month, this/last year, last N days, last N months, last 12 months.
- Resolved dates are injected into the SQL-generation prompt as literals; the LLM must not compute dates.
- Timezone configurable (default `Asia/Kolkata`).

### 6.5 Schema Context (FR-SCH)
- Introspect via SQLAlchemy inspector / `information_schema`: tables, columns, types, PKs, FKs.
- Cache with TTL and manual refresh.
- Prompts receive only relevant tables when the schema is large (FK-graph + keyword pruning).
- Never hard-code table descriptions beyond an optional YAML annotation overlay.

### 6.6 SQL Generation & Planning (FR-SQL)
- PostgreSQL dialect only. Simple, efficient SQL. Explicit JOINs, explicit columns (no `SELECT *`).
- Aggregate at the correct grain to avoid **join fan-out** (never sum `orders.amount` after joining `order_items`).
- Add `LIMIT` for non-aggregate/ranking queries (default 100; "top N" uses N).
- Date filters use half-open ranges on the raw column (no `DATE_TRUNC` on the column in WHERE).
- Deterministic tie-break in rankings (`ORDER BY metric DESC, id ASC`) and mention ties in the answer.

### 6.7 SQL Safety & Validation (FR-SAFE) — see §9

### 6.8 Result Explanation (FR-EXP)
- Explanation generated **only from returned rows**; the LLM never invents numbers.
- Currency formatted as ₹ with Indian digit grouping.
- Empty result → entity-aware "No customers matched these conditions."; never fabricate.

### 6.9 Conversation (FR-CTX)
- Session-scoped `AnalyticalContext`: entity, metric, time period, filters, grouping, ranking, resolved clarifications, last SQL, last result summary.
- Follow-ups classified as `new_query | refinement | clarification_answer`.
- Refinements merge delta into prior context; the merged intent re-runs the full pipeline (ambiguity + validation still apply).
- Context window limited to last N turns (default 6).

### 6.10 Presentation (FR-UI)
Primary answer; collapsible SQL + assumptions; data table for multi-row; line/bar chart when result has a time/category dimension and a numeric metric; clarification rendered as buttons.

### 6.11 Error Handling (FR-ERR)
| Case | Behaviour |
|------|-----------|
| Non-data question | Explain a data question is needed; give 3 examples |
| Missing data | "I can't answer this because the database does not contain …" |
| Ambiguous | Clarification |
| Invalid SQL | Controlled repair, max 2 retries, then safe apology |
| Unsafe SQL | Block, log, generic safe message |
| Timeout | Explain query was too heavy; suggest narrowing range |
| Empty result | Say so plainly |
| LLM/provider failure | Retry with backoff, optional fallback provider, then friendly error |

## 7. Data Model (initial)
- `customers(customer_id, name, email, signup_date, city, state, country)`
- `orders(order_id, customer_id, order_date, amount, status)`
- `products(product_id, product_name, category, price)`
- `order_items(order_id, product_id, quantity, unit_price)`
- `store_visits(visit_id, customer_id, store_id, visit_date)`

Relationships: customers 1—N orders; customers 1—N store_visits; orders 1—N order_items; products 1—N order_items. Schema may evolve; code must not assume it.

## 8. Structured Output Contracts (Pydantic v2)
```python
class IntentStatus(str, Enum):
    ready; clarification_required; unsupported; missing_data; not_data_question; blocked; error

class TimePeriod(BaseModel):
    expression: str | None
    kind: Literal["calendar", "rolling", "absolute"] | None
    start: date | None   # inclusive
    end: date | None     # exclusive

class Filter(BaseModel):
    field: str
    op: Literal["=", "!=", ">", "<", ">=", "<=", "in", "between", "like"]
    value: Any

class Intent(BaseModel):
    entity: str | None
    metric: str | None
    aggregation: Literal["count", "sum", "avg", "min", "max"] | None
    filters: list[Filter] = []
    time_period: TimePeriod | None
    group_by: list[str] = []
    ranking: Literal["highest", "lowest"] | None
    ranking_term: str | None          # e.g. "best"
    sort: list[SortSpec] = []
    limit: int | None
    output: Literal["scalar", "table", "chart"] | None

class ClarificationOption(BaseModel):
    id: str; label: str; description: str | None

class AmbiguityResult(BaseModel):
    is_ambiguous: bool
    ambiguous_term: str | None
    reason: str | None
    question: str | None
    options: list[ClarificationOption] = []

class SQLPlan(BaseModel):
    tables: list[str]; columns: list[str]; joins: list[str]
    filters: list[str]; aggregation: str | None
    ordering: str | None; grain_notes: str | None

class SQLGeneration(BaseModel):
    sql: str
    assumptions: list[str] = []

class PipelineResponse(BaseModel):
    status: IntentStatus
    session_id: str
    intent: Intent | None
    clarification: AmbiguityResult | None
    sql: str | None
    assumptions: list[str]
    answer: str | None
    columns: list[str] | None
    rows: list[list[Any]] | None
    chart: ChartSpec | None
    error: ErrorInfo | None
```
**Invariant (model validator):** `status == clarification_required ⇒ sql is None`; `status == ready ⇒ sql is not None`.

## 9. SQL Safety (Defense in Depth)
1. **DB layer:** dedicated `analytics_ro` role: `SELECT` only on allow-listed tables/views; `default_transaction_read_only = on`; `statement_timeout` (default 10 s); connection limit.
2. **App layer (AST via `sqlglot`, Postgres dialect):**
   - Exactly one statement; must be `SELECT` (or `WITH … SELECT`).
   - Reject DML/DDL/DCL, `COPY`, `SET`, `CALL`, `DO`, stacked statements, `SELECT … INTO`, `FOR UPDATE`, `pg_*` / `information_schema` access, dangerous functions (`pg_sleep`, `pg_read_file`, `lo_*`, `dblink`, …).
   - Table/column allow-list check against the live schema; join validity against FK graph (flag cross joins / missing join predicates).
   - Enforce/append `LIMIT` (max 1000).
   - Cost guard: `EXPLAIN (FORMAT JSON)`; reject above configurable cost/row estimate.
3. **Execution:** read-only transaction, row cap, timeout; raw DB errors never shown to the user.
4. **Credentials:** the LLM never sees credentials; only the app holds them.
5. **Prompt injection:** user text and DB values are data; SQL is validated regardless of what the LLM says.
6. **Audit log:** question, intent, SQL, validation verdict, duration, row count.

## 10. LLM Layer
- `LLMProvider` abstract interface: `generate_structured(prompt, response_model, temperature, ...) -> BaseModel`.
- Adapters: Gemini, OpenAI, Groq; selected by config; optional fallback chain.
- Native JSON-schema output where supported; else JSON mode + Pydantic validation + 1 repair retry.
- Temperature 0 for intent/SQL; slightly higher allowed only for explanation wording.
- Prompts live in `app/prompts/*.md` (versioned), not inline strings.

## 11. Architecture & Stack
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2 + psycopg 3, Pydantic v2, sqlglot, PyYAML, structlog, tenacity.
- **DB:** PostgreSQL 16 (Docker Compose), seeded with realistic data (≥5k customers, ≥50k orders, Indian cities/states).
- **UI (MVP):** Streamlit chat UI calling the FastAPI API (chat, clarification buttons, SQL expander, table, chart).
- **Testing:** pytest, golden question set, mocked LLM for unit tests, optional live-LLM eval.
- **Packaging:** `pyproject.toml`, `.env.example`, Docker Compose, README.

```
app/main.py, app/config.py
app/api/          routes, dependencies
app/core/         schemas.py, enums.py, errors.py
app/llm/          base.py, gemini.py, openai_provider.py, groq.py, factory.py
app/db/           engine.py, introspection.py, schema_context.py
app/semantics/    business_definitions.yaml, ambiguity_registry.yaml, loader.py
app/timeutil/     resolver.py
app/pipeline/     context_merge.py, intent.py, ambiguity.py, planner.py, sqlgen.py, explain.py, orchestrator.py
app/sql/          validator.py, executor.py, repair.py
app/conversation/ store.py, context.py
app/prompts/      *.md
ui/streamlit_app.py
db/               init.sql, roles.sql, seed.py
tests/            unit/, integration/, golden/
```

## 12. API
- `POST /api/v1/chat` `{session_id?, message}` → `PipelineResponse`
- `POST /api/v1/clarify` `{session_id, option_id | free_text}` → `PipelineResponse`
- `GET /api/v1/schema` → introspected schema summary
- `GET /api/v1/health`
- `POST /api/v1/sessions/{id}/reset`

## 13. Non-Functional Requirements
- p50 end-to-end latency < 6 s, p95 < 15 s (LLM-dependent); DB query timeout 10 s.
- Zero successful write operations (verified by tests and DB role).
- Structured logging with request IDs; secrets only via env.
- ≥85% unit test coverage on validator, time resolver, context merge, schema contracts.
- No hard dependency on one LLM provider.

## 14. Success Criteria & Evaluation
Golden set (`tests/golden/questions.yaml`):

| # | Question | Expected |
|---|----------|----------|
| 1 | How many customers signed up last month? | ready, correct count |
| 2 | What was the total revenue last month? | ready, status assumption disclosed |
| 3 | Show the top 5 customers by revenue. | ready, 5 rows |
| 4 | Which city generated the most revenue? | ready, 1 row |
| 5 | How many orders were placed last week? | ready, ISO week |
| 6 | Monthly sales for the last 12 months | ready, 12 rows, line chart |
| 7 | Show customers with more than 5 orders | ready, HAVING-based |
| 8 | Show the best customer last month | **clarification**, no SQL |
| 9 | Show the most active customer | **clarification**, no SQL |
| 10 | "How many signed up last month?" → "How many from Punjab?" | refinement, filter added |
| 11 | "Delete all customers" | blocked / not a read query |
| 12 | "Tell me something interesting" | not_data_question |
| 13 | "Average customer age" (no such column) | missing_data |
| 14 | Prompt-injection attempt in question | no unsafe SQL executed |

Targets: ≥90% execution accuracy on clear questions; **100%** clarification on the ambiguous set; **0** unsafe SQL executions; ≤5% unnecessary clarifications on clear questions.

## 15. Milestones
M0 Foundation → M1 DB & data → M2 Contracts & config → M3 LLM layer → M4 Schema/time/semantics → M5 Intent & ambiguity → M6 SQL gen/validate/execute/repair → M7 Orchestrator & conversation → M8 API → M9 UI → M10 Evaluation & hardening → M11 Docs & release.

## 16. Risks & Mitigations
| Risk | Mitigation |
|------|-----------|
| LLM over-asks or under-asks | Registry + golden tests in both directions; prompt tuning |
| Join fan-out gives wrong totals | Grain rule in prompt + validator warning + numeric golden checks against hand-written SQL |
| Prompt injection | AST validator + RO role + allow-lists |
| Provider structured-output differences | Adapter layer + Pydantic validation + repair retry |
| Revenue definition disputes | Central `business_definitions.yaml` + disclosed assumptions |
| Schema drift | Dynamic introspection with TTL refresh |

## 17. Defaults Chosen (changeable in config)
- Counted order statuses for revenue: `completed`.
- Week start: Monday (ISO).
- Timezone: Asia/Kolkata.
- Session store: in-memory for MVP; interface ready for Redis/Postgres.
