"""Module containing API configuration variables."""

import logging
from pathlib import Path

from fridge_app_backend.api.utils import get_env_var
from fridge_app_backend.exceptions import BadDBTypeError, BadEnvironmentError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

AVAILABLE_ENVIRONMENTS = {"dev", "prod"}
DEPLOYED_ENVIRONMENTS = {"prod"}
ENVIRONMENT = get_env_var("FRIDGE_APP_ENVIRONMENT", "dev")
AVAILABLE_DB_TYPES = {"in_memory", "sqlite"}
DB_TYPE = get_env_var("DB_TYPE", "in_memory")

# Check that the environment is set correctly
if ENVIRONMENT not in AVAILABLE_ENVIRONMENTS:
    raise BadEnvironmentError(
        current_environment=ENVIRONMENT, allowed_environments=AVAILABLE_ENVIRONMENTS
    )

# Check that the DB_TYPE is set correctly
if DB_TYPE not in AVAILABLE_DB_TYPES:
    raise BadDBTypeError(db_type=DB_TYPE, allowed_types=AVAILABLE_DB_TYPES)

ENV_FILE = Path("~/.env").expanduser()


def get_db_conn() -> str:
    """Get the connection string for the database."""
    if DB_TYPE == "in_memory":
        return "sqlite:///:memory:"

    db_path = Path("database.db")
    if db_path.exists():
        db_path.unlink()

    return f"sqlite+pysqlite:///{db_path.absolute()}"


def get_db_conn_args() -> dict[str, str | bool]:
    """Get the connection arguments for the database."""
    return {"check_same_thread": False}


# Set database connection string, arguments and type
DB_CONN = get_db_conn()
DB_CONNECTION_ARGS = get_db_conn_args()
