"""
ASGI application entry point for StratslabAPI.

This module provides the ASGI application instance that is used by
ASGI servers like Uvicorn. It initializes the FastAPI application
with all necessary configuration, middleware, and routers.

Usage:
    uvicorn stratslabapi.web_servers.asgi:app --host 0.0.0.0 --port 8000
"""

from stratslabapi.apps.fastapi import StratslabAPI

# Create the FastAPI application instance
app = StratslabAPI(
    title="StratslabAPI",
    description="AI-powered trading strategy backtesting platform",
)

