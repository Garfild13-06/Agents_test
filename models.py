"""Pydantic models for request/response validation."""

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, EmailStr, Field, PositiveFloat, field_validator


class WeatherResponse(BaseModel):
    """Weather information response model."""

    city: str
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Weather condition")
    humidity: int = Field(ge=0, le=100, description="Humidity percentage")
    timestamp: datetime


class CurrencyRateResponse(BaseModel):
    """Currency exchange rate response model."""

    base_currency: str
    target_currency: str
    rate: float = Field(gt=0, description="Exchange rate")
    timestamp: datetime


class JokeResponse(BaseModel):
    """Joke response model."""

    joke: str
    category: str
    id: int


class SystemInfoResponse(BaseModel):
    """System information response model."""

    python_version: str
    server_time: datetime
    uptime_seconds: float
    status: str


class RandomQuoteResponse(BaseModel):
    """Random quote response model."""

    quote: str
    author: str
    category: str


class ValidationRequest(BaseModel):
    """Request model for validation endpoint."""

    name: Annotated[str, Field(min_length=1, max_length=100)]
    age: Annotated[int, Field(ge=0, le=150)]
    email: EmailStr
    tags: Annotated[list[str], Field(default_factory=list, max_length=10)]

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[str]) -> list[str]:
        """Strip whitespace and enforce the max-length constraint after cleanup."""
        cleaned = [tag.strip() for tag in tags if tag.strip()]
        if len(cleaned) > 10:
            raise ValueError("No more than 10 non-empty tags allowed.")
        return cleaned


class ValidationResponse(BaseModel):
    """Response model for validation endpoint."""

    success: bool
    message: str
    processed_data: dict[str, Any]


class ProcessDataRequest(BaseModel):
    """Request model for data processing endpoint."""

    numbers: Annotated[list[float], Field(min_length=1, max_length=100)]
    operation: Literal["sum", "average", "max", "min"]
    multiplier: PositiveFloat = Field(
        default=1.0, description="Multiplier applied to the calculated value."
    )


class ProcessDataResponse(BaseModel):
    """Response model for data processing endpoint."""

    operation: str
    result: float
    input_count: int
    processed_at: datetime


class CacheResponse(BaseModel):
    """Cache entry response model."""

    key: str
    value: Any
    created_at: datetime
    exists: bool


class StatsResponse(BaseModel):
    """Statistics response model."""

    total_requests: int
    endpoint_counts: dict[str, int]
    average_response_time_ms: float
    cache_size: int
