"""Instantiate the necessary SQLAlchemy singleton objects for communicating with the database."""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from fridge_app_backend.api.config import DB_CONN, DB_CONNECTION_ARGS, DB_TYPE
from fridge_app_backend.orm.models.db_models import Base

logger = logging.getLogger(__name__)


# Singleton engine object (connection pooling is applied for performance only in deployed mode)
if DB_TYPE == "deployed":
    logger.info("Database connection established for deployed environment.")
    engine = create_engine(
        DB_CONN,
        future=True,
        connect_args=DB_CONNECTION_ARGS,
        pool_size=20,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )
else:
    engine = create_engine(
        DB_CONN,
        future=True,
        connect_args=DB_CONNECTION_ARGS,
        poolclass=NullPool,
    )


# We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
SessionLocal = sessionmaker(bind=engine)


def initialise_db() -> None:
    """Recreate the database based on structure defined by models."""
    # Emit DDL to the DB - create DB
    # emit CREATE statements given ORM registry
    Base.metadata.create_all(engine)

    # Fill all default tables with initial/default data
    # with SessionLocal.begin() as session:
    #     if not session.query(EnumBase).count():
    #         init_all_enum_tables(session=session)
    #     if not session.query(UTR).count():
    #         init_utr_table(session=session)
    #     init_excluded_restriction_sites_table(session=session)


def reset_db() -> None:
    """Recreate the database based on structure defined by models."""
    # Emit DDL to the DB - create DB
    # emit CREATE statements given ORM registry
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Fill all default tables with initial/default data
    # with SessionLocal.begin() as session:
    #     init_all_enum_tables(session=session)
    #     init_utr_table(session=session)
    #     init_excluded_restriction_sites_table(session=session)


def get_session() -> Generator[Session, None, None]:
    """Get a DB Session.

    Yields
    ------
    DB session object.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    reset_db()
