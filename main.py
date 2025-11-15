"""Main entry point for FastAPI application."""

import uvicorn
from fastapi import FastAPI

from api import router
from config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Demo FastAPI server for testing AI agents' capabilities",
    debug=settings.debug,
)

# Include API routes
app.include_router(router)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize application on startup."""
    print(f"Starting {settings.app_name} v{settings.app_version}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Cleanup on application shutdown."""
    print(f"Shutting down {settings.app_name}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )

