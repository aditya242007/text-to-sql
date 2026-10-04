VENV := .venv
PY   := $(VENV)/bin/python
PIP  := PIP_CACHE_DIR=/Volumes/KRISH/.pip-cache $(VENV)/bin/pip
RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest
UVICORN := $(VENV)/bin/uvicorn
STREAMLIT := $(VENV)/bin/streamlit

.DEFAULT_GOAL := help

.PHONY: help install lint test run-api run-ui db-up

help:
	@echo ""
	@echo "  make install   Install all dependencies (including dev extras)"
	@echo "  make lint      Run ruff check + format check"
	@echo "  make test      Run unit tests (no network, no DB)"
	@echo "  make run-api   Start the FastAPI dev server"
	@echo "  make run-ui    Start the Streamlit UI"
	@echo "  make db-up     Start PostgreSQL via Docker Compose"
	@echo ""

install:
	$(PIP) install -e ".[dev]"

lint:
	$(RUFF) check .
	$(RUFF) format --check .

test:
	$(PYTEST) -m "not integration and not live_llm" --cov=app --cov-report=term-missing

run-api:
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	$(STREAMLIT) run ui/streamlit_app.py

db-up:
	docker compose up -d db
