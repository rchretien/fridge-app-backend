"""Module containing API configuration variables."""

import logging
from functools import lru_cache
from os import getenv
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pytz import timezone

from fridge_app_backend.exceptions import BadDBTypeError, BadEnvironmentError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

AVAILABLE_ENVIRONMENTS = {"local", "test", "dev", "prod"}
DEPLOYED_ENVIRONMENTS = {"prod"}
AVAILABLE_DB_TYPES = {"in_memory", "sqlite", "postgres"}
ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Config(BaseSettings):
    """Configuration class for the API."""

    model_config = SettingsConfigDict(
        env_file=Path(f"{ROOT_DIR}/.env-{getenv('ENVIRONMENT', 'local')}"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API specic variables
    api_name: str = "Fridge Inventory App Backend"
    api_description: str = "CRUD API for managing a fridge inventory."
    api_version: str = "0.1.0"
    brussels_tz_name: str = "Europe/Brussels"
    commit_sha: str | None = None

    # Environment specific variables
    environment: str = "local"
    db_type: str = "in_memory"

    # Postgres configuration (used only if db_type == "postgres")
    db_user: str | None = None
    db_password: str = ""
    db_name: str | None = None
    db_host: str | None = None
    db_port: str | None = None

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Validate the environment."""
        if value not in AVAILABLE_ENVIRONMENTS:
            raise BadEnvironmentError(
                current_environment=value, allowed_environments=AVAILABLE_ENVIRONMENTS
            )
        return value

    @field_validator("db_type")
    @classmethod
    def validate_db_type(cls, value: str) -> str:
        """Validate db type."""
        if value not in AVAILABLE_DB_TYPES:
            raise BadDBTypeError(db_type=value, allowed_types=AVAILABLE_DB_TYPES)
        return value

    @property
    def brussels_tz(self):
        return timezone(self.brussels_tz_name)

    # ---------------------------------------------
    # 🔗 Database connection logic
    # ---------------------------------------------
    @property
    def db_url(self) -> str:
        """Return the correct database URL based on the db_type."""
        if self.db_type == "in_memory":
            return "sqlite:///:memory:"

        if self.db_type == "sqlite":
            db_path = Path("database.db")
            if db_path.exists():
                db_path.unlink()
            return f"sqlite+pysqlite:///{db_path.absolute()}"

        if self.db_type == "postgres":
            password_part = f":{self.db_password}" if self.db_password else ""
            return (
                f"postgresql+psycopg2://{self.db_user}{password_part}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )

        raise BadDBTypeError(db_type=self.db_type, allowed_types=AVAILABLE_DB_TYPES)

    @property
    def db_conn_args(self) -> dict[str, str | bool]:
        """Return the connection arguments for SQLAlchemy."""
        if self.db_type.startswith("sqlite"):
            return {"check_same_thread": False}
        return {}


@lru_cache
def get_settings() -> Config:
    """Return the settings."""
    return Config()


config = get_settings()
