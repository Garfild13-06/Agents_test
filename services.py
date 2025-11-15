"""Business logic and external data fetching services."""

import asyncio
import random
import sys
import time
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

import httpx


# In-memory storage for demo purposes
_in_memory_cache: Dict[str, Dict[str, Any]] = {}
_request_stats: Dict[str, int] = {}
_start_time = time.time()


# Mock data
WEATHER_DATA = {
    "moscow": {"temperature": 15.5, "condition": "Cloudy", "humidity": 65},
    "london": {"temperature": 12.0, "condition": "Rainy", "humidity": 80},
    "tokyo": {"temperature": 22.0, "condition": "Sunny", "humidity": 55},
    "newyork": {"temperature": 18.0, "condition": "Partly Cloudy", "humidity": 70},
}

CURRENCY_RATES = {
    ("USD", "EUR"): 0.85,
    ("USD", "GBP"): 0.79,
    ("EUR", "USD"): 1.18,
    ("EUR", "GBP"): 0.93,
    ("GBP", "USD"): 1.27,
    ("GBP", "EUR"): 1.08,
}

JOKES = [
    {"joke": "Why don't scientists trust atoms? Because they make up everything!", "category": "science", "id": 1},
    {"joke": "Why did the scarecrow win an award? He was outstanding in his field!", "category": "general", "id": 2},
    {"joke": "Why don't eggs tell jokes? They'd crack each other up!", "category": "food", "id": 3},
    {"joke": "What do you call a fake noodle? An impasta!", "category": "food", "id": 4},
    {"joke": "Why did the math book look so sad? Because it had too many problems!", "category": "education", "id": 5},
]

QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivation"},
    {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs", "category": "business"},
    {"quote": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon", "category": "life"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt", "category": "inspiration"},
    {"quote": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle", "category": "philosophy"},
]


async def get_weather_async(city: str, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Fetch weather data for a city (async mock implementation).

    Args:
        city: City name (lowercase)
        timeout: Request timeout in seconds

    Returns:
        Dictionary with weather data

    Raises:
        ValueError: If city not found
    """
    # Simulate async external API call
    await asyncio.sleep(0.1)

    city_lower = city.lower()
    if city_lower not in WEATHER_DATA:
        # Generate random weather for unknown cities
        return {
            "temperature": round(random.uniform(-10, 35), 1),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
            "humidity": random.randint(30, 90),
        }

    return WEATHER_DATA[city_lower]


def get_currency_rate(base: str, target: str) -> float:
    """
    Get currency exchange rate (mock implementation).

    Args:
        base: Base currency code
        target: Target currency code

    Returns:
        Exchange rate

    Raises:
        ValueError: If rate not found
    """
    base_upper = base.upper()
    target_upper = target.upper()

    if base_upper == target_upper:
        return 1.0

    key = (base_upper, target_upper)
    if key in CURRENCY_RATES:
        return CURRENCY_RATES[key]

    # Generate mock rate for unknown pairs
    return round(random.uniform(0.5, 2.0), 4)


def get_random_joke() -> Dict[str, Any]:
    """
    Get a random joke.

    Returns:
        Dictionary with joke data
    """
    return random.choice(JOKES)


def get_system_info() -> Dict[str, Any]:
    """
    Get system information.

    Returns:
        Dictionary with system information
    """
    return {
        "python_version": sys.version.split()[0],
        "server_time": datetime.now(),
        "uptime_seconds": round(time.time() - _start_time, 2),
        "status": "operational",
    }


def get_random_quote() -> Dict[str, Any]:
    """
    Get a random quote.

    Returns:
        Dictionary with quote data
    """
    return random.choice(QUOTES)


def generate_uuid() -> str:
    """
    Generate a random UUID.

    Returns:
        UUID string
    """
    return str(uuid4())


def update_request_stats(endpoint: str) -> None:
    """
    Update request statistics for an endpoint.

    Args:
        endpoint: Endpoint name
    """
    _request_stats[endpoint] = _request_stats.get(endpoint, 0) + 1


def get_statistics() -> Dict[str, Any]:
    """
    Get request statistics.

    Returns:
        Dictionary with statistics
    """
    total = sum(_request_stats.values())
    avg_time = 0.0  # Simplified for demo
    return {
        "total_requests": total,
        "endpoint_counts": _request_stats.copy(),
        "average_response_time_ms": avg_time,
        "cache_size": len(_in_memory_cache),
    }


def get_cache_value(key: str) -> Optional[Dict[str, Any]]:
    """
    Get value from in-memory cache.

    Args:
        key: Cache key

    Returns:
        Cache entry or None if not found
    """
    return _in_memory_cache.get(key)


def set_cache_value(key: str, value: Any) -> Dict[str, Any]:
    """
    Set value in in-memory cache.

    Args:
        key: Cache key
        value: Value to store

    Returns:
        Created cache entry
    """
    entry = {
        "value": value,
        "created_at": datetime.now(),
        "exists": True,
    }
    _in_memory_cache[key] = entry
    return entry


def process_numbers(numbers: list[float], operation: str, multiplier: float = 1.0) -> float:
    """
    Process a list of numbers with specified operation.

    Args:
        numbers: List of numbers to process
        operation: Operation to perform (sum, average, max, min)
        multiplier: Optional multiplier to apply

    Returns:
        Processed result

    Raises:
        ValueError: If operation is invalid
    """
    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers)
    elif operation == "max":
        result = max(numbers)
    elif operation == "min":
        result = min(numbers)
    else:
        raise ValueError(f"Unknown operation: {operation}")

    return round(result * multiplier, 2)


async def fetch_external_data_mock(url: str, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Mock external HTTP request using httpx (for demo purposes).

    Args:
        url: URL to fetch
        timeout: Request timeout

    Returns:
        Mock response data

    Note:
        In real implementation, this would make actual HTTP request
    """
    # Simulate network delay
    await asyncio.sleep(0.2)

    # Return mock data instead of making real request
    return {
        "status": "success",
        "data": {"message": "This is a mock response", "timestamp": datetime.now().isoformat()},
        "url": url,
    }

