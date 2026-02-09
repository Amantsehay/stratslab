from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, Literal, Self
import mimetypes
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from starlette.routing import Host, Mount, Route, WebSocketRoute

from stratslabapi.__version__ import __version__
from stratslabapi.core import settings, feature_flags
from stratslabapi.middlewares.cors import CORSMiddleware
from stratslabapi.middlewares.counter import APIRequestCounter
from stratslabapi.middlewares.secure import HTTPSRedirectMiddleware
from stratslabapi.repositories.session import session_manager
from stratslabapi.utils import metadata

if TYPE_CHECKING:
    from pydantic import HttpUrl
    

    
mimetypes.add_type("image/webp", ".webp")



class StratslabAPI(FastAPI):

    @property
    def BOTS_FORBIDDEN_URLS(self) -> tuple[str, ...]:
        """URLs that should be forbidden for bots. Includes the dynamic OpenAPI URL from settings."""
        return (
            "/favicon.ico",
            settings.openapi_url,
            "/robots.txt",
            "/sitemap.xml",
            "/static",
            "/health",
            "/logout",
            "/api/",
            "/s"
        )

    @property
    def _description(self) -> str:
        """API description"""
        return "Stratslab API - Strategy Analysis Platform"

    def __init__(self, **kwargs: Any) -> None:

        kwargs.setdefault("docs_url", settings.docs_url)
        kwargs.setdefault("redoc_url", settings.redoc_url)
        kwargs.setdefault("openapi_url", settings.openapi_url)
        kwargs.setdefault("lifespan", self._lifespan)
        kwargs.setdefault("version", __version__)
        kwargs.setdefault("description", self._description)
        kwargs.setdefault("openapi_tags", settings.openapi_tags)
        super().__init__(**kwargs)
        self._setup_middlewares()
        self._setup_routers()
        add_pagination(self)
        
    @asynccontextmanager
    async def _lifespan(self, _: Self) -> AsyncGenerator[None, Any]:
        # Initialize database connection pool on startup
        session_manager.initialize()
        yield 
        # Close database connections on shutdown
        if session_manager.engine is not None:
            await session_manager.close()
    
    
    def _setup_middlewares(self) -> None:
        if feature_flags.enable_https_redirect:
            self.add_middleware(HTTPSRedirectMiddleware)
        self.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allows_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        if feature_flags.count_api_requests:
            self.add_middleware(APIRequestCounter)
    def _setup_routers(self) -> None:
        from stratslabapi.routers import api_router, graphql_router, root_router

        for router in [api_router, graphql_router, root_router]:
            self.include_router(router)
    