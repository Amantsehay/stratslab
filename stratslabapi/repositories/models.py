from pydantic import BaseModel
from datetime import UTC, datetime, timedelta
from enum import Enum
from functools import partial
from typing import Final

from aiocache import cached
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import (
    VARCHAR,
    BIGINT,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Table,
    Text,
    TIMESTAMP,
    func,
    Select,
    select,
    Update,
    SmallInteger,
    Result
)
from sqlalchemy.dialects.postgresql import ENUM, Insert, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy.orm.strategy_options import Load
from sqlalchemy.sql.elements import BinaryExpression

from ._base import Base
from .session import session_manager



_REQUESTS_TTL: Final[int] = 60 * 60 * 1

def _cache_requests_since_builder(func_, *args, **_) -> str:
    truncated = args[1].replace(minute=0, second=0, microsecond=0)
    return f"{func_.__name__}:{truncated.isoformat()}"

class RequestCounterModel(Base):
    __tablename__ = "request_counter"
    
    url: Mapped[str] = mapped_column(
        VARCHAR(
            length=64
        ),
        nullable=False,
        unique=True
    )
    counter: Mapped[int] = mapped_column(
        BIGINT,
        nullable=False,
        default=1
    )
    
    @classmethod
    async def count_url(cls, session: AsyncSession, url: str, /) -> None:
        statement: Insert = (
            insert(cls)
            .values({"url": url})
            .on_conflict_do_update(
                constraint="request_counter_url_key",
                set_={"counter": cls.counter + 1}
            )
        )    

        session: AsyncSession 
        async with session_manager.session() as session:
            await session.execute(statement)
            await session.commit()
    
    @classmethod
    @cached(ttl=_REQUESTS_TTL)
    async def get_total_requests(cls) -> int:
        statement: Select = select(
            func.coalesce(
                func.sum(
                    RequestCounterModel.counter), 0))
        session: AsyncSession
        async with session_manager.session() as session:
            result; Result = await session.execute(statement)
            
        return result.scalar()
    @classmethod
    @cached(ttl=_REQUESTS_TTL, key_builder=_cache_requests_since_builder)
    async def get_requests_since(cls, since: datetime) -> int:
        statement: Select = select(
            func.sum(RequestCounterModel.counter)
        ).where(RequestCounterModel.created_at >= since)