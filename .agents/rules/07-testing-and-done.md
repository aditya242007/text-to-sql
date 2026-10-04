# Rule 07 — Testing & Definition of Done (Always On)

## Per phase, you may declare "done" only when ALL are true
1. Acceptance criteria in the phase prompt are met.
2. `ruff check` and `pytest` pass; new code has tests (unit first; integration where DB is involved).
3. You actually ran the code/tests and report real output — never claim success without running.
4. No scope creep; no files from later phases.
5. `docs/PROGRESS.md` updated: what was built, how to run it, decisions, known gaps.
6. Work is committed on the phase branch, pushed, and a PR is open (Rule 09); CI is green.
7. A short summary is given to the user, then STOP and wait for approval before the next phase.

## Test strategy
- Unit: validator, time resolver, context merge, schema contracts, registry filtering (LLM mocked).
- Integration: Dockerized PostgreSQL; read-only role proof; executor timeout/limit.
- Golden: `tests/golden/questions.yaml` with expected status, key SQL properties, and numeric results checked against hand-written SQL.
- Coverage target ≥85% for validator, time resolver, context merge, schemas.

## Safety net
- If a test fails, fix the cause; never weaken or delete a test to pass.
- If blocked or unsure, state the blocker and ask; do not invent behavior.
