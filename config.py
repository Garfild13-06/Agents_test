"""Configuration module for handling environment variables and settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API configuration
    api_key: str = "demo-key-12345"
    api_key_header: str = "X-API-Key"

    # Server configuration
    app_name: str = "FastAPI Demo Server"
    app_version: str = "1.0.0"
    debug: bool = False

    # External API settings (with defaults for demo)
    weather_api_timeout: float = 5.0
    currency_api_timeout: float = 5.0

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


# Global settings instance
settings = Settings()

