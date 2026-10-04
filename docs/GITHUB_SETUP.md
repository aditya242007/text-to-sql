# GitHub Setup (do this once, yourself — not the agent)

## 1. Create the repo
Option A — GitHub CLI:
```bash
cd ambiguity-sql-analytics
git init -b main
gh auth login                       # one-time, browser-based; don't paste tokens anywhere else
gh repo create ambiguity-sql-analytics --private --source=. --remote=origin
```
Option B — website: create an empty repo (no README/.gitignore), then:
```bash
git init -b main
git remote add origin git@github.com:<you>/ambiguity-sql-analytics.git
```

## 2. First commit (the build pack)
```bash
cat > .gitignore << 'EOT'
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/
*.dump
.idea/
.vscode/
EOT
git add .
git commit -m "docs: add PRD, agent rules, phase prompts and CI scaffolding"
git push -u origin main
```

## 3. Protect `main` (GitHub → Settings → Branches → Add rule for `main`)
- Require a pull request before merging
- Require status checks: `lint-and-unit` (and `integration` after Phase 1)
- Block force pushes

## 4. Track phases with Issues & Milestones (optional but recommended)
```bash
for i in 0 1 2 3 4 5 6 7 8 9 10 11; do gh issue create --title "Phase $i" --body "See docs/PHASE_PROMPTS.md — Phase $i" ; done
```
Add a GitHub Project board (Todo / In progress / Review / Done) and put the issues on it.

## 5. Secrets
Put API keys only in a local `.env`. For CI live-LLM evals later, add them as **Settings → Secrets and variables → Actions**; never in code.

## 6. Per-phase loop
```
git checkout main && git pull
git checkout -b phase/N-name
# agent builds, committing in small steps
git push -u origin phase/N-name
gh pr create --fill                 # CI runs
# you review → squash-merge → then:
git checkout main && git pull
git tag -a v0.N.0 -m "Phase N" && git push origin v0.N.0
```
