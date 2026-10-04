"""Smoke tests for the health endpoint — Phase 0 acceptance check."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    """GET /api/v1/health must return HTTP 200 with status 'ok'."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_body(client: TestClient) -> None:
    """GET /api/v1/health body must be {\"status\": \"ok\"}."""
    response = client.get("/api/v1/health")
    assert response.json() == {"status": "ok"}
