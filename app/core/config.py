import os
from typing import Any, Dict, List, Optional
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "L&D Enterprise AI SaaS"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Database
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[int] = 5432
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        data = info.data
        user = data.get("POSTGRES_USER")
        password = data.get("POSTGRES_PASSWORD")
        server = data.get("POSTGRES_SERVER")
        port = data.get("POSTGRES_PORT") or 5432
        db = data.get("POSTGRES_DB")
        if not all([user, password, server, db]):
            raise ValueError(
                "Missing database configuration: "
                "POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_SERVER / POSTGRES_DB"
            )
        import urllib.parse
        quoted_user = urllib.parse.quote_plus(user)
        quoted_password = urllib.parse.quote_plus(password)
        # Return asyncpg connection string for async engine
        return f"postgresql+asyncpg://{quoted_user}:{quoted_password}@{server}:{port}/{db}"

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # AI Provider
    LLM_PROVIDER: str = "gemini"  # gemini, ollama, openai, claude
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None

    # Ollama provider settings
    OLLAMA_BINARY_PATH: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = "llama3.2"
    OLLAMA_TEMPERATURE: float = 0.7

    # Embedding provider settings
    EMBEDDING_PROVIDER: str = "gemini"  # gemini, openai, claude, ollama

    # AI Model Settings
    DEFAULT_MODEL: str = "gemini-2.5-flash"
    PREMIUM_MODEL: str = "gemini-2.5-pro"
    EMBEDDING_MODEL: str = "text-embedding-004"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except Exception:
                return [v]
        return v


settings = Settings()
