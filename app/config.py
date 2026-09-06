import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Required field
    groq_api_key: str

    # Optional fields with default values
    port: int = 8080
    telegram_chat_id: Optional[str] = None

    # Settings configuration (reads from .env file if available)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra env variables not defined here
    )


# Instantiate the settings object
settings = Settings()
