# Ambiguity-Aware AI SQL Analytics — Antigravity Build Pack

## Contents
- `docs/PRD.md` — final PRD (source of truth)
- `docs/PHASE_PROMPTS.md` — Phase 0–11 prompts, paste one at a time
- `.agents/rules/01..08-*.md` — individual project rules the agent must obey
- `.agents/workflows/next-phase.md` — optional `/next-phase` workflow
- `docs/GITHUB_SETUP.md` — one-time repo setup + per-phase git loop
- `.github/workflows/ci.yml`, `.github/pull_request_template.md` — CI and PR template

## Before anything else
Follow `docs/GITHUB_SETUP.md` to create the repo and push this pack to `main`.

## Setup in Antigravity
1. Copy this folder to your machine and open it as the workspace.
2. Confirm the rules appear in the Rules panel (workspace rules from `.agents/rules/`). Set them to **Always On**.
   (If your build of Antigravity expects a different rules location, paste the rule files into the workspace rules UI instead.)
3. Use Planning mode. Paste Phase 0 from `docs/PHASE_PROMPTS.md`.
4. Review the plan artifact, approve, verify tests, then move to the next phase.

## Rule files
| File | Purpose |
|------|---------|
| 01-project-context | Mission, core principle, fixed stack, scope limits |
| 02-architecture | Layering, provider independence, config, prompts, determinism |
| 03-sql-safety | Read-only enforcement in code and DB |
| 04-ambiguity-handling | When and how to clarify; no SQL while clarifying |
| 05-llm-structured-output | Pydantic-only LLM contracts, retries, fake provider |
| 06-coding-standards | Typing, lint, logging, file size |
| 07-testing-and-done | Definition of Done per phase |
| 08-workflow-and-communication | Plan first, one phase at a time, no destructive commands |
| 09-git-and-github | Branch per phase, conventional commits, PRs, tags, no secrets/force-push |
