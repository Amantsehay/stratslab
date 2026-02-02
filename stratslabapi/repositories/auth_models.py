from uuid import UUID
from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Self

from ._base import Base


class Role(Base):
    """User role model for role-based access control"""
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    users: Mapped[list["User"]] = relationship("User", back_populates="role")


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), nullable=False)

    role: Mapped[Role] = relationship("Role", back_populates="users")

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Self | None:
        """Get user by email address"""
        return await cls.get_or_none(session, email, field=cls.email)

    @classmethod
    async def get_by_username(cls, session: AsyncSession, username: str) -> Self | None:
        """Get user by username"""
        return await cls.get_or_none(session, username, field=cls.username)
