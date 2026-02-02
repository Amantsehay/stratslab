from datetime import datetime
from uuid import UUID
from pydantic import EmailStr, Field, SecretStr

from stratslabapi.helpers.pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    username: str = Field(min_length=3, max_length=100, pattern=r'^[A-Za-z0-9_.-]+$')
    password: SecretStr = Field(min_length=8)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: SecretStr


class UserResponse(BaseModel):
    """Schema for user response"""
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"
