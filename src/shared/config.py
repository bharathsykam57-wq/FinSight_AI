"""
Configuration Management Module.

Loads and validates all environment variables from the .env file
using Pydantic Settings. Import 'settings' anywhere in the app.

Usage:
    from src.shared.config import settings
    print(settings.gemini_api_key)
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # --- AI Configuration ---
    openai_model_name: str = Field(
        "gemini/gemini-2.0-flash",
        description="The LLM model to use for agents."
    )

    # --- Gemini ---
    gemini_api_key: Optional[str] = Field(
        None,
        description="Google Gemini API Key."
    )

    # --- Firecrawl ---
    firecrawl_api_key: Optional[str] = Field(
        None,
        description="API Key for Firecrawl scraping service."
    )

    # --- LangSmith Observability (optional) ---
    langchain_tracing_v2: bool = Field(
        False,
        description="Enable LangSmith tracing."
    )
    langchain_api_key: Optional[str] = Field(
        None,
        description="LangSmith API Key (required if tracing is True)."
    )

    # --- Azure Infrastructure ---
    azure_blob_storage_connection_string: Optional[str] = Field(
        None,
        description="Connection string for Azure Blob Storage."
    )
    azure_postgres_connection_string: Optional[str] = Field(
        None,
        description="Connection string for Azure PostgreSQL."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """Creates and caches the Settings object. Reads .env only once on startup."""
    return Settings()


settings = get_settings()