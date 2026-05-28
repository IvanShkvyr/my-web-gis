from pathlib import Path
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL as SAUrl

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FRONTEND_DIR: Path = (_PROJECT_ROOT / "frontend").resolve()


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables / .env file
    All required fields raise a clear error at startup if missing.
    """

    # --- DataBase parts ---
    DB_USER: str = Field(..., description="Database username")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(..., description="Database port")
    DB_NAME: str = Field(..., description="Database name")

    # --- JWT ---
    SECRET_KEY: str = Field(
        ...,
        min_length=32,
        description="Secret key for JWT signing. Generate: python -c \"import secrets; print(secrets.token_hex(32))\"",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        gt=0,
        description="JWT token lifetime in minutes",
    )

    # --- App ---
    APP_ENV: Literal["development", "production"] = Field(default="development")
    CORS_ORIGINS: str = Field(
        default="",
        description="Comma-separated list of allowed CORS origins",
    )


    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        """
        Parses CORS_ORIGINS string into a list for use in middleware.
        """
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


    @computed_field
    @property
    def DATABASE_URL(self) -> SAUrl:
        """
        Builds a SQLAlchemy-compatible connection string from individual parts.
        Credentials are URL-encoded to handle special characters safely.
        """
        return SAUrl.create(
                drivername="postgresql+psycopg2",
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                database=self.DB_NAME,
            )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

settings = Settings()
