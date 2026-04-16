from typing import Any

from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    # System
    TIMEZONE: str = "Europe/London"
    LOG_LEVEL: str = "WARNING"
    ENCRYPTION_KEY: str

    # Database
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    # Origins
    FRONTEND_HOST: str = "http://localhost:5173"

    # Clerk
    CLERK_SECRET_KEY: str
    CLERK_JWT_KEY: str

    # GoCardless
    GOCARDLESS_API_KEY_ID: str
    GOCARDLESS_API_KEY_SECRET: str

    # OpenFIGI
    OPENFIGI_API_KEY: str


settings = Settings()  # type: ignore
