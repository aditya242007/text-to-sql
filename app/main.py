"""FastAPI application entry point.

This module creates the FastAPI app instance, configures logging,
and mounts all routers. No business logic lives here.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import settings
from app.core.logging import configure_logging

# Configure structlog before anything else uses a logger.
configure_logging(log_level=settings.log_level, log_format=settings.log_format)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: runs startup logic, then yields, then shutdown logic."""
    logger.info(
        "app_started",
        version="0.1.0",
        llm_provider=settings.llm_provider,
        llm_model=settings.llm_model,
        timezone=settings.app_timezone,
    )
    yield
    logger.info("app_stopped")


app = FastAPI(
    title="Ambiguity-Aware AI SQL Analytics",
    description=(
        "Conversational analytics: ask business questions in natural language, "
        "get safe, schema-aware, read-only PostgreSQL answers."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(health_router)
