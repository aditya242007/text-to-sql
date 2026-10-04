# Rule 09 — Git & GitHub Tracking (Always On)

The whole project is tracked in GitHub. Every phase leaves a clean, reviewable history.

## Branching
- `main` is always green and deployable. Never commit directly to `main` after Phase 0.
- One branch per phase: `phase/<N>-<short-name>` (e.g. `phase/1-database`). Hotfixes: `fix/<short-name>`.
- Create the branch from up-to-date `main` before writing any code.

## Commits
- Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`, `ci:`. Imperative mood, subject ≤ 72 chars, body explains *why* when non-obvious.
- Small, logical commits (e.g. schema → seed → tests), not one giant commit per phase.
- Run `ruff check` and `pytest` BEFORE committing. Never commit failing tests or lint errors.
- Before every commit run `git status` and `git diff --staged` and confirm no secrets or junk are staged.

## Never commit
`.env`, API keys, tokens, DB dumps, `__pycache__`, `.venv`, `.pytest_cache`, `.ruff_cache`, large generated data, IDE files. If a secret is ever staged or committed: STOP, tell the user, and do not push; the key must be rotated.

## Pushing & PRs
- Push the phase branch: `git push -u origin phase/<N>-<name>`.
- Open a Pull Request into `main` (use `gh pr create` if the GitHub CLI is available, otherwise give the user the compare URL). Fill the PR template: summary, how tested, checklist, PRD sections covered.
- Merge only after the user approves, and only if CI is green. Prefer squash-merge with a Conventional Commit title.
- After merge: `git checkout main && git pull`, then tag: `git tag -a v0.<N>.0 -m "Phase <N>: <name>"` and `git push origin v0.<N>.0`.

## Forbidden without explicit user confirmation
`git push --force` / `--force-with-lease`, `git reset --hard`, `git rebase` on pushed branches, deleting remote branches, rewriting history, changing the remote URL, editing git config globally.

## Authentication
- Never ask the user to paste tokens/passwords into the chat, and never write them to files.
- Assume the user is already authenticated via `gh auth login` or SSH. If a push fails with an auth error, stop and tell the user how to authenticate; do not work around it.

## Tracking
- Update `docs/PROGRESS.md` in every phase PR (what's done, how to run, test results, link to PR).
- Each phase PR should reference its GitHub Issue (`Closes #N`) if issues exist.
