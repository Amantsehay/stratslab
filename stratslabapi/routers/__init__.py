"""
API routers module.

This module organizes all API routers for the StratslabAPI application.
Routers are organized by feature/domain to maintain scalability for future microservices.
"""

from fastapi import APIRouter

# Root router for health and basic endpoints
root_router = APIRouter(tags=["root"])


# API v1 router - main API endpoints (to be implemented)
api_router = APIRouter(prefix="/api/v1", tags=["api"])


# GraphQL router - GraphQL endpoint (to be implemented)
graphql_router = APIRouter(prefix="/graphql", tags=["graphql"])


__all__ = [
    "root_router",
    "api_router",
    "graphql_router",
]
