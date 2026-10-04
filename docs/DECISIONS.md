# Design Decisions

## Phase 0 — Foundation

### D0-01: Python runtime — use `.venv` (Python 3.12) over system Python
- **Decision:** All commands use `.venv/bin/python` and `.venv/bin/pip` explicitly.
- **Reason:** The machine has Apple's Python 3.9 as the default `python` alias. The existing `.venv` is Python 3.12, which satisfies the `>=3.11` requirement.
- **Alternative considered:** Creating a fresh venv at 3.11 — rejected to avoid unnecessary disk usage (internal disk at 95%).

### D0-02: `PIP_CACHE_DIR=/Volumes/KRISH/.pip-cache`
- **Decision:** All `pip install` calls set `PIP_CACHE_DIR` to the external KRISH volume.
- **Reason:** Internal disk (`/System/Volumes/Data`) is at 95% capacity (189 GiB / 228 GiB used). Installing large LLM SDK dependency trees without redirecting the cache risks running out of space.
- **Alternative considered:** `--no-cache-dir` — rejected because caching speeds up repeated installs across phases.

### D0-03: `app/core/logging.py` extracted from `app/config.py`
- **Decision:** Structlog configuration lives in its own module (`app/core/logging.py`), called once from `app/main.py`.
- **Reason:** Keeps `app/config.py` focused on settings; avoids import-time side effects when `settings` is imported by other modules.

### D0-04: `mypy.strict = false` in `pyproject.toml`
- **Decision:** mypy is configured but `strict = false` for Phase 0.
- **Reason:** Strict mode would require type stubs for all third-party libraries (many LLM SDKs lack them). `ignore_missing_imports = true` is set. Will revisit per-phase.
- **TODO (tracked):** Incrementally tighten mypy config as stubs become available; add per-module overrides.

### D0-05: Duplicate `.gitignore` entries cleaned
- **Decision:** `.gitignore` was rewritten with no duplicates. No new entries beyond what was there before.
- **Reason:** The file had `.DS_Store` three times and `.env` / `.venv/` twice each. Keeping the file tidy avoids confusion.

### D0-06: `ui/streamlit_app.py` placeholder created
- **Decision:** Created a minimal placeholder that just shows an info message.
- **Reason:** `make run-ui` is defined in the Makefile; having no file would cause an immediate error. Phase 9 will replace this entirely.
