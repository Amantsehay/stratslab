from contextlib import asynccontextmanager
from typing import AsyncGenerator
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from stratslabapi.core import settings


def _get_database_url() -> str:
    """Get the database URL from settings.
    
    If database_url is not set, constructs URL from postgres_* components.
    Properly encodes credentials to handle special characters.
    """
    if settings.database_url:
        return str(settings.database_url)
    
    # Build URL from components if database_url is not set
    # URL-encode username and password to handle special characters
    encoded_user = quote_plus(settings.postgres_user)
    encoded_password = quote_plus(settings.postgres_password)
    return f"postgresql+asyncpg://{encoded_user}:{encoded_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"


class SessionManager:
    """Manages database connections with async SQLAlchemy engine"""

    def __init__(self):
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker[AsyncSession] | None = None

    def initialize(self) -> None:
        """Initialize async engine with connection pooling from settings"""
        self.engine = create_async_engine(
            _get_database_url(),
            pool_size=settings.pool_size,
            max_overflow=settings.pool_max_overflow,
            pool_timeout=settings.pool_timeout,
            pool_recycle=settings.pool_recycle,
            echo=False
        )
        self.session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide transactional database session"""
        if self.session_maker is None:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")

        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def close(self) -> None:
        """Close engine and all connections"""
        if self.engine is not None:
            await self.engine.dispose()


# Global singleton instance
session_manager = SessionManager()
