"""Health check router — GET /api/v1/health."""

from __future__ import annotations

import structlog
from fastapi import APIRouter

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["health"])


@router.get("/api/v1/health", summary="Health check")
async def health() -> dict[str, str]:
    """Return a simple liveness signal.

    Returns:
        A JSON object with ``{"status": "ok"}``.
    """
    logger.debug("health_check_called")
    return {"status": "ok"}
