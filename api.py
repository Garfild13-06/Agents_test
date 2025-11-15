"""API routes and endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Body, Header, HTTPException, Query, status
from fastapi.responses import HTMLResponse

from config import settings
from models import (
    CacheResponse,
    CurrencyRateResponse,
    JokeResponse,
    ProcessDataRequest,
    ProcessDataResponse,
    RandomQuoteResponse,
    StatsResponse,
    SystemInfoResponse,
    ValidationRequest,
    ValidationResponse,
    WeatherResponse,
)
from services import (
    fetch_external_data_mock,
    generate_uuid,
    get_cache_value,
    get_currency_rate,
    get_random_joke,
    get_random_quote,
    get_statistics,
    get_system_info,
    process_numbers,
    set_cache_value,
    update_request_stats,
)
from services import get_weather_async

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root() -> str:
    """
    Root endpoint returning HTML interface.

    Returns:
        HTML page with web interface
    """
    update_request_stats("root")
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Demo Server</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin: 5px;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 10px;
                padding: 10px;
                background-color: #f9f9f9;
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
            }
            pre {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 4px;
                overflow-x: auto;
            }
            input {
                padding: 8px;
                margin: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>🚀 FastAPI Demo Server</h1>
        
        <div class="container">
            <h2>Системная информация</h2>
            <button onclick="loadSystemInfo()">Загрузить информацию о системе</button>
            <div id="systemInfo" class="result"></div>
        </div>

        <div class="container">
            <h2>Погода</h2>
            <input type="text" id="cityInput" placeholder="Введите город (например: moscow)" value="moscow">
            <button onclick="loadWeather()">Получить погоду</button>
            <div id="weatherResult" class="result"></div>
        </div>

        <div class="container">
            <h2>Случайная шутка</h2>
            <button onclick="loadJoke()">Получить шутку</button>
            <div id="jokeResult" class="result"></div>
        </div>

        <div class="container">
            <h2>Случайная цитата</h2>
            <button onclick="loadQuote()">Получить цитату</button>
            <div id="quoteResult" class="result"></div>
        </div>

        <div class="container">
            <h2>Статистика</h2>
            <button onclick="loadStats()">Загрузить статистику</button>
            <div id="statsResult" class="result"></div>
        </div>

        <div class="container">
            <h2>UUID генератор</h2>
            <button onclick="generateUUID()">Сгенерировать UUID</button>
            <div id="uuidResult" class="result"></div>
        </div>

        <script>
            async function loadSystemInfo() {
                try {
                    const response = await fetch('/api/system/info');
                    const data = await response.json();
                    document.getElementById('systemInfo').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('systemInfo').innerHTML = 
                        '<p style="color: red;">Ошибка: ' + error.message + '</p>';
                }
            }

            async function loadWeather() {
                const city = document.getElementById('cityInput').value || 'moscow';
                try {
                    const response = await fetch(`/api/weather/${city}`);
                    const data = await response.json();
                    document.getElementById('weatherResult').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('weatherResult').innerHTML = 
                        '<p style="color: red;">Ошибка: ' + error.message + '</p>';
                }
            }

            async function loadJoke() {
                try {
                    const response = await fetch('/api/joke');
                    const data = await response.json();
                    document.getElementById('jokeResult').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('jokeResult').innerHTML = 
                        '<p style="color: red;">Ошибка: ' + error.message + '</p>';
                }
            }

            async function loadQuote() {
                try {
                    const response = await fetch('/api/random/quote');
                    const data = await response.json();
                    document.getElementById('quoteResult').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('quoteResult').innerHTML = 
                        '<p style="color: red;">Ошибка: ' + error.message + '</p>';
                }
            }

            async function loadStats() {
                try {
                    const response = await fetch('/api/stats');
                    const data = await response.json();
                    document.getElementById('statsResult').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('statsResult').innerHTML = 
                        '<p style="color: red;">Ошибка: ' + error.message + '</p>';
                }
            }

            async function generateUUID() {
                try {
                    const response = await fetch('/api/random/uuid');
                    const data = await response.json();
                    document.getElementById('uuidResult').innerHTML = 
                        '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (error) {
                    document.getElementById('uuidResult').innerHTML = 
                        '<p style="color: red;">Ошибка: ' + error.message + '</p>';
                }
            }
        </script>
    </body>
    </html>
    """


@router.get("/api/system/info", response_model=SystemInfoResponse)
async def system_info() -> SystemInfoResponse:
    """
    Get system information endpoint.

    Returns:
        System information including Python version, server time, and status
    """
    update_request_stats("system_info")
    info = get_system_info()
    return SystemInfoResponse(**info)


@router.get("/api/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str) -> WeatherResponse:
    """
    Get weather information for a city (async endpoint with mock data).

    Args:
        city: City name

    Returns:
        Weather information

    Raises:
        HTTPException: If weather data cannot be retrieved
    """
    update_request_stats("weather")
    try:
        weather_data = await get_weather_async(city, settings.weather_api_timeout)
        return WeatherResponse(
            city=city,
            temperature=weather_data["temperature"],
            condition=weather_data["condition"],
            humidity=weather_data["humidity"],
            timestamp=datetime.now(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weather data: {str(e)}",
        )


@router.get("/api/currency/{base}/{target}", response_model=CurrencyRateResponse)
def get_currency(base: str, target: str) -> CurrencyRateResponse:
    """
    Get currency exchange rate.

    Args:
        base: Base currency code (e.g., USD, EUR)
        target: Target currency code (e.g., EUR, GBP)

    Returns:
        Currency exchange rate information

    Raises:
        HTTPException: If currency rate cannot be retrieved
    """
    update_request_stats("currency")
    try:
        rate = get_currency_rate(base, target)
        return CurrencyRateResponse(
            base_currency=base.upper(),
            target_currency=target.upper(),
            rate=rate,
            timestamp=datetime.now(),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get currency rate: {str(e)}",
        )


@router.get("/api/joke", response_model=JokeResponse)
def get_joke() -> JokeResponse:
    """
    Get a random joke.

    Returns:
        Random joke with category and ID
    """
    update_request_stats("joke")
    joke_data = get_random_joke()
    return JokeResponse(**joke_data)


@router.get("/api/stats", response_model=StatsResponse)
def get_stats() -> StatsResponse:
    """
    Get request statistics based on in-memory data.

    Returns:
        Statistics including total requests, endpoint counts, and cache size
    """
    update_request_stats("stats")
    stats_data = get_statistics()
    return StatsResponse(**stats_data)


@router.get("/api/random/uuid")
def get_random_uuid() -> dict[str, str]:
    """
    Generate a random UUID.

    Returns:
        Dictionary with generated UUID
    """
    update_request_stats("random_uuid")
    return {"uuid": generate_uuid()}


@router.get("/api/random/quote", response_model=RandomQuoteResponse)
def get_quote() -> RandomQuoteResponse:
    """
    Get a random quote.

    Returns:
        Random quote with author and category
    """
    update_request_stats("random_quote")
    quote_data = get_random_quote()
    return RandomQuoteResponse(**quote_data)


@router.post("/api/validate", response_model=ValidationResponse)
def validate_data(
    request: ValidationRequest,
    strict: bool = Query(default=False, description="Enable strict validation mode"),
) -> ValidationResponse:
    """
    Validate JSON data with query parameters.

    Args:
        request: Validation request data
        strict: Optional strict validation mode

    Returns:
        Validation result with processed data
    """
    update_request_stats("validate")
    # Process and validate the data
    processed = {
        "name_length": len(request.name),
        "age_group": "adult" if request.age >= 18 else "minor",
        "email_domain": request.email.split("@")[1] if "@" in request.email else None,
        "tag_count": len(request.tags),
        "strict_mode": strict,
    }

    return ValidationResponse(
        success=True,
        message="Data validated successfully",
        processed_data=processed,
    )


@router.get("/api/protected")
def get_protected_resource(
    x_api_key: str = Header(..., alias="X-API-Key", description="API key for authentication"),
) -> dict[str, Any]:
    """
    Protected resource requiring API key in header.

    Args:
        x_api_key: API key from request header

    Returns:
        Protected resource data

    Raises:
        HTTPException: If API key is invalid
    """
    update_request_stats("protected")
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return {
        "message": "Access granted to protected resource",
        "resource_id": generate_uuid(),
        "access_time": datetime.now().isoformat(),
        "permissions": ["read", "write"],
    }


@router.post("/api/process", response_model=ProcessDataResponse)
def process_data(request: ProcessDataRequest) -> ProcessDataResponse:
    """
    Process JSON body data with validation.

    Args:
        request: Data processing request

    Returns:
        Processed data result

    Raises:
        HTTPException: If processing fails
    """
    update_request_stats("process")
    try:
        result = process_numbers(request.numbers, request.operation, request.multiplier)
        return ProcessDataResponse(
            operation=request.operation,
            result=result,
            input_count=len(request.numbers),
            processed_at=datetime.now(),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing failed: {str(e)}",
        )


@router.get("/api/cache/{key}", response_model=CacheResponse)
def get_cache(key: str) -> CacheResponse:
    """
    Get value from in-memory cache.

    Args:
        key: Cache key

    Returns:
        Cache entry or error if not found
    """
    update_request_stats("get_cache")
    entry = get_cache_value(key)
    if entry is None:
        return CacheResponse(
            key=key,
            value=None,
            created_at=datetime.now(),
            exists=False,
        )

    return CacheResponse(
        key=key,
        value=entry["value"],
        created_at=entry["created_at"],
        exists=True,
    )


@router.post("/api/cache/{key}")
def set_cache(key: str, value: Any = Body(...)) -> CacheResponse:
    """
    Set value in in-memory cache.

    Args:
        key: Cache key
        value: Value to store (from request body)

    Returns:
        Created cache entry
    """
    update_request_stats("set_cache")
    entry = set_cache_value(key, value)
    return CacheResponse(
        key=key,
        value=entry["value"],
        created_at=entry["created_at"],
        exists=True,
    )


@router.get("/api/external")
async def external_data() -> dict[str, Any]:
    """
    Async endpoint that demonstrates external HTTP request using httpx.

    Returns:
        Mock external API response

    Note:
        This endpoint uses httpx for async HTTP requests (mocked for demo)
    """
    update_request_stats("external")
    try:
        # Simulate external API call
        result = await fetch_external_data_mock("https://api.example.com/data", timeout=5.0)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External API request failed: {str(e)}",
        )

