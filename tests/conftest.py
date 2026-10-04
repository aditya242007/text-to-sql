"""Shared pytest fixtures for the test suite.

Conventions:
- Unit tests live in tests/unit/ and must never make network or DB calls.
- Integration tests (marker: integration) require a live Dockerized PostgreSQL.
- Live-LLM tests (marker: live_llm) require a real API key; skipped otherwise.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Return a FastAPI TestClient for the whole test session.

    No network calls are made; TestClient drives the ASGI app in-process.
    """
    return TestClient(app)
