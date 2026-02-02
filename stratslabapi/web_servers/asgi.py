"""
ASGI application entry point for StratslabAPI.

This module provides the ASGI application instance that is used by
ASGI servers like Uvicorn. It initializes the FastAPI application
with all necessary configuration, middleware, and routers.

Usage:
    uvicorn stratslabapi.web_servers.asgi:app --host 0.0.0.0 --port 8000
"""

from stratslabapi.apps.fastapi import StratslabAPI
from stratslabapi.repositories.session import session_manager

# Create the FastAPI application instance
app = StratslabAPI(
    title="StratslabAPI",
    description="AI-powered trading strategy backtesting platform",
)


@app.on_event("startup")
def startup_event() -> None:
    """Initialize database connection pool on application startup."""
    session_manager.initialize()


@app.get("/health", tags=["health"], include_in_schema=False)
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Status indication of the API and its dependencies
    """
    return {"status": "ok"}
