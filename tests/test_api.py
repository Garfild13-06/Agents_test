"""Tests for API endpoints."""

import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Test root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "FastAPI Demo Server" in response.text


def test_system_info() -> None:
    """Test system info endpoint returns valid data."""
    response = client.get("/api/system/info")
    assert response.status_code == 200
    data = response.json()
    assert "python_version" in data
    assert "server_time" in data
    assert "uptime_seconds" in data
    assert "status" in data
    assert data["status"] == "operational"


def test_weather_endpoint_success() -> None:
    """Test weather endpoint with valid city."""
    response = client.get("/api/weather/moscow")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "moscow"
    assert "temperature" in data
    assert "condition" in data
    assert "humidity" in data
    assert "timestamp" in data
    assert isinstance(data["temperature"], (int, float))
    assert 0 <= data["humidity"] <= 100


def test_weather_endpoint_unknown_city() -> None:
    """Test weather endpoint with unknown city (should still work with mock)."""
    response = client.get("/api/weather/unknowncity123")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "unknowncity123"
    assert "temperature" in data


def test_currency_endpoint_success() -> None:
    """Test currency endpoint with valid currencies."""
    response = client.get("/api/currency/USD/EUR")
    assert response.status_code == 200
    data = response.json()
    assert data["base_currency"] == "USD"
    assert data["target_currency"] == "EUR"
    assert "rate" in data
    assert data["rate"] > 0
    assert "timestamp" in data


def test_currency_endpoint_same_currency() -> None:
    """Test currency endpoint with same base and target."""
    response = client.get("/api/currency/USD/USD")
    assert response.status_code == 200
    data = response.json()
    assert data["rate"] == 1.0


def test_joke_endpoint() -> None:
    """Test joke endpoint returns valid joke."""
    response = client.get("/api/joke")
    assert response.status_code == 200
    data = response.json()
    assert "joke" in data
    assert "category" in data
    assert "id" in data
    assert isinstance(data["joke"], str)
    assert len(data["joke"]) > 0


def test_random_uuid_endpoint() -> None:
    """Test UUID generation endpoint."""
    response = client.get("/api/random/uuid")
    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert isinstance(data["uuid"], str)
    assert len(data["uuid"]) > 0


def test_random_quote_endpoint() -> None:
    """Test random quote endpoint."""
    response = client.get("/api/random/quote")
    assert response.status_code == 200
    data = response.json()
    assert "quote" in data
    assert "author" in data
    assert "category" in data
    assert isinstance(data["quote"], str)
    assert len(data["quote"]) > 0


def test_validate_endpoint_success() -> None:
    """Test validation endpoint with valid data."""
    request_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "tags": ["developer", "python"],
    }
    response = client.post("/api/validate?strict=false", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "processed_data" in data
    assert data["processed_data"]["name_length"] == 8
    assert data["processed_data"]["age_group"] == "adult"


def test_validate_endpoint_invalid_email() -> None:
    """Test validation endpoint with invalid email."""
    request_data = {
        "name": "John Doe",
        "age": 30,
        "email": "invalid-email",
        "tags": [],
    }
    response = client.post("/api/validate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_validate_endpoint_invalid_age() -> None:
    """Test validation endpoint with invalid age."""
    request_data = {
        "name": "John Doe",
        "age": 200,  # Invalid age
        "email": "john@example.com",
        "tags": [],
    }
    response = client.post("/api/validate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_protected_endpoint_success() -> None:
    """Test protected endpoint with valid API key."""
    response = client.get(
        "/api/protected",
        headers={"X-API-Key": "demo-key-12345"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "resource_id" in data
    assert "access_time" in data
    assert "permissions" in data


def test_protected_endpoint_invalid_key() -> None:
    """Test protected endpoint with invalid API key."""
    response = client.get(
        "/api/protected",
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]


def test_protected_endpoint_missing_key() -> None:
    """Test protected endpoint without API key."""
    response = client.get("/api/protected")
    assert response.status_code == 422  # Missing header


def test_process_endpoint_success() -> None:
    """Test process endpoint with valid data."""
    request_data = {
        "numbers": [1, 2, 3, 4, 5],
        "operation": "sum",
        "multiplier": 2.0,
    }
    response = client.post("/api/process", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "sum"
    assert data["result"] == 30.0  # (1+2+3+4+5) * 2
    assert data["input_count"] == 5
    assert "processed_at" in data


def test_process_endpoint_average() -> None:
    """Test process endpoint with average operation."""
    request_data = {
        "numbers": [10, 20, 30],
        "operation": "average",
    }
    response = client.post("/api/process", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["operation"] == "average"
    assert data["result"] == 20.0


def test_process_endpoint_invalid_operation() -> None:
    """Test process endpoint with invalid operation."""
    request_data = {
        "numbers": [1, 2, 3],
        "operation": "invalid_op",
    }
    response = client.post("/api/process", json=request_data)
    assert response.status_code == 400


def test_cache_get_missing() -> None:
    """Test cache get with non-existent key."""
    response = client.get("/api/cache/nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] is False
    assert data["key"] == "nonexistent"


def test_cache_set_and_get() -> None:
    """Test cache set and get operations."""
    # Set cache value
    key = "test_key_123"
    value = {"test": "data", "number": 42}
    response = client.post(f"/api/cache/{key}", json=value)
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] is True
    assert data["key"] == key

    # Get cache value
    response = client.get(f"/api/cache/{key}")
    assert response.status_code == 200
    data = response.json()
    assert data["exists"] is True
    assert data["value"] == value


def test_stats_endpoint() -> None:
    """Test stats endpoint returns valid statistics."""
    # Make some requests first
    client.get("/api/joke")
    client.get("/api/random/uuid")

    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
    assert "endpoint_counts" in data
    assert "average_response_time_ms" in data
    assert "cache_size" in data
    assert isinstance(data["total_requests"], int)
    assert isinstance(data["endpoint_counts"], dict)


@pytest.mark.asyncio
async def test_external_endpoint() -> None:
    """Test external endpoint (async)."""
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/external")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "data" in data

