"""
API routers module.

This module organizes all API routers for the StratslabAPI application.
Routers are organized by feature/domain to maintain scalability for future microservices.
"""

from fastapi import APIRouter

# Root router for health and basic endpoints
root_router = APIRouter(tags=["root"])


@root_router.get(
    "/health",
    summary="Health Check",
    description="Returns the health status of the API",
    tags=["root"],
    response_description="Health status of the API",
)
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring API availability.

    Returns:
        dict: A dictionary with status "healthy" if the API is running correctly
    """
    return {"status": "healthy"}


# API v1 router - main API endpoints (to be implemented)
api_router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


# GraphQL router - GraphQL endpoint (to be implemented)
graphql_router = APIRouter(
    prefix="/graphql",
    tags=["graphql"],
    responses={
        400: {"description": "Bad request"},
        500: {"description": "Internal server error"},
    },
)
# API v1 router - main API endpoints (to be implemented)
api_router = APIRouter(prefix="/api/v1", tags=["api"])


# GraphQL router - GraphQL endpoint (to be implemented)
graphql_router = APIRouter(prefix="/graphql", tags=["graphql"])


__all__ = [
    "root_router",
    "api_router",
    "graphql_router",
]
