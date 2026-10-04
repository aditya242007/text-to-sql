# Rule 08 — Agent Workflow & Communication (Always On)

1. **Plan first.** For every phase, produce an Implementation Plan artifact (files to create, approach, risks) and wait for approval before coding if the phase is non-trivial.
2. Work phase by phase in the order defined in `docs/PHASE_PROMPTS.md`. Never skip or merge phases.
3. Keep a running `docs/PROGRESS.md` and `docs/DECISIONS.md` (decision, reason, alternatives).
4. Use the terminal to run tests/linters/docker; show real results in your walkthrough.
5. Never modify the PRD or these rules without explicit user approval. Propose changes instead.
6. Do not run destructive shell commands (`rm -rf`, dropping databases, `docker system prune`) without explicit user confirmation. Only operate inside the project directory.
7. Never put real API keys in code, logs, tests, or artifacts. Use `.env` (git-ignored).
8. End each phase with: Summary → How to run → Test results → Open questions → "Ready for Phase N+1?"
