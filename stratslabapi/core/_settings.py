from base64 import urlsafe_b64encode
from functools import cached_property, lru_cache 
import json
import logging
from pathlib import Path
from typing import Any, Literal, get_args, get_origin
from urllib.parse import urlparse

from cryptography.fernet import Fernet
from pydantic import BaseModel, Field, HttpUrl, PostgresDsn, RedisDsn, SecretStr, field_validator
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

def _parse_list(value: str | None) -> list[str]:
    if not value:
        return []
    return [str(x).strip() for x in value.split(",")]

def _parse_json(value: str | None, field_name: str = "unknown") -> Any:
    """Parse JSON string, returning None for empty/invalid input."""
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        # Log the error but return None to allow fallback to default value
        logging.warning(f"Failed to parse JSON for field '{field_name}' from env variable: {e}")
        return None

def _fix_postgres_url(url: str, /, *, scheme: str = "postgresql+asyncpg") -> str:
    return urlparse(url)._replace(scheme=scheme).geturl()

class _EnvSource(EnvSettingsSource):
    def prepare_field_value(
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool
    ) -> Any:
        # Only apply CSV parsing to list[str] fields
        if get_origin(field.annotation) is list:
            args = get_args(field.annotation)
            if args and args[0] is str:
                return _parse_list(value)
            else:
                # For complex list types (e.g., list[dict[str, Any]]), parse as JSON
                parsed = _parse_json(value, field_name)
                if parsed is not None:
                    return parsed
                return super().prepare_field_value(field_name, field, value, value_is_complex)
        if field_name == "database_url" and value:
            return PostgresDsn(_fix_postgres_url(value))
        return super().prepare_field_value(field_name, field, value, value_is_complex)
    
    
class Settings(BaseSettings):
    allows_origins: list[str] = []
    database_url: PostgresDsn | None = None
    project_root: Path = Path(__file__).parent.parent.parent.resolve()
    trusted_host: str = "localhost"
    static: Path = Path("static")
    secret_key: SecretStr = SecretStr("default-secret-key-change-in-production")

    # PostgreSQL connection components for constructing database_url
    postgres_db: str = "stratslab_dev"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    
    pool_max_overflow: int = 10
    pool_size: int = 5
    pool_timeout: int = 30
    pool_recycle: int = -1

    # API Documentation Configuration
    docs_url: str | None = "/api-docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"
    openapi_tags: list[dict[str, Any]] = Field(
        default_factory=lambda: [
            {"name": "root", "description": "Root and health endpoints"},
            {"name": "api", "description": "Main API v1 endpoints"},
            {"name": "graphql", "description": "GraphQL endpoints"},
        ]
    ) 
    
    @field_validator("docs_url", "redoc_url", "openapi_url", mode="before")
    @classmethod
    def normalize_empty_to_none(cls, v: Any) -> str | None:
        """Normalize empty strings to None for API documentation URLs.
        
        This ensures that setting these values to empty strings will disable
        the documentation endpoints, which is the expected FastAPI behavior.
        """
        if v == "":
            return None
        return v
    
    @cached_property
    def fernet(self) -> Fernet:
        return Fernet(urlsafe_b64encode(self.secret_key.get_secret_value().encode().ljust(32)[:32]))
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
        
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (_EnvSource(settings_cls), )
    
    @staticmethod
    def _clean_path(path: str | None, /) -> str:
        if path is None:
            path = ""
        return path[1:] if path.startswith("/") else path
    def build_url(
        self,
        *,
        path: str | None = None,
        is_static : bool = True
    ) -> HttpUrl:
        path = self._clean_path(path)
        if is_static is True:
            path =  f"{self.static}/{path}" if path else f"{self.static}"
        return HttpUrl.build(
            scheme="https",
            host=self.trusted_host,
            path=path
        )
        
settings = Settings()


class FeatureFlags(BaseModel):
    enable_https_redirect: bool = False
    send_emails: bool = False
    activate_users: bool = False
    enable_sentry: bool = False
    count_api_requests: bool = False
    

feature_flags = FeatureFlags()
