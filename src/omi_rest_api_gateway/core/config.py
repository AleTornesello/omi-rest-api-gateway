from enum import StrEnum
from functools import lru_cache

from pydantic import AnyHttpUrl, BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    local = "local"
    test = "test"
    staging = "staging"
    production = "production"


class ApiSettings(BaseModel):
    title: str = "OMI REST API Gateway"
    version: str = "0.1.0"
    prefix: str = "/api/v1"
    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: list[str] = Field(default_factory=lambda: ["*"])


class OmiSettings(BaseModel):
    base_url: AnyHttpUrl = AnyHttpUrl("https://www.agenziaentrate.gov.it")
    timeout_seconds: float = Field(default=30.0, gt=0)
    cache_ttl_seconds: int = Field(default=86_400, ge=0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="OMI_API_",
        extra="ignore",
    )

    environment: Environment = Environment.local
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = Field(default=8080, ge=1, le=65_535)
    reload: bool = False
    log_level: str = "INFO"
    api: ApiSettings = Field(default_factory=ApiSettings)
    omi: OmiSettings = Field(default_factory=OmiSettings)


@lru_cache
def get_settings() -> Settings:
    return Settings()
