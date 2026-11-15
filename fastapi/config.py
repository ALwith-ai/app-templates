"""Typed settings loaded from the environment and the service's .env file."""

from functools import cache
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated configuration. Add one field for each value the service reads."""

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env", env_file_encoding="utf-8", extra="ignore", hide_input_in_errors=True
    )

    database_url: PostgresDsn


@cache
def get_settings() -> Settings:
    return Settings()
