"""Application settings loaded from environment variables / .env file.

All configuration lives here. No other module reads ``os.environ`` directly.
Keys are documented in ``.env.example``.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed, validated application settings via pydantic-settings.

    Values are read from environment variables (case-insensitive) and,
    in development, from a ``.env`` file in the project root.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Database ---
    database_url_admin: str = "postgresql+psycopg://postgres:postgres@localhost:5432/analytics"
    database_url_ro: str = "postgresql+psycopg://analytics_ro:analytics_ro@localhost:5432/analytics"

    # --- LLM provider ---
    llm_provider: str = "gemini"
    llm_model: str = "gemini-2.0-flash"
    llm_fallback_providers: str = ""  # comma-separated, e.g. "openai,groq"

    # --- LLM API keys ---
    gemini_api_key: str = ""
    openai_api_key: str = ""
    groq_api_key: str = ""

    # --- Application ---
    app_timezone: str = "Asia/Kolkata"

    # DB query timeout (milliseconds → used as statement_timeout via psycopg options)
    sql_timeout_ms: int = 10_000

    # Maximum rows returned per query
    sql_max_rows: int = 1_000

    # Schema introspection cache TTL (seconds)
    schema_cache_ttl_s: int = 300

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # "json" | "console"

    @property
    def llm_fallback_list(self) -> list[str]:
        """Return the fallback provider chain as a list (empty if not configured)."""
        return [p.strip() for p in self.llm_fallback_providers.split(",") if p.strip()]


# Module-level singleton — import this everywhere instead of instantiating Settings().
settings = Settings()
