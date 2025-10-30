"""Instantiate the necessary SQLAlchemy singleton objects for communicating with the database."""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, StaticPool

from fridge_app_backend.config import config
from fridge_app_backend.orm.models.db_models import (
    Base,
    ProductLocation,
    ProductType,
    init_product_location_table,
    init_product_type_table,
)

logger = logging.getLogger(__name__)


# Singleton engine object (connection pooling is applied for performance only in deployed mode)
if config.db_type == "deployed":
    logger.info("Database connection established for deployed environment.")
    engine = create_engine(
        url=config.db_url,
        future=True,
        connect_args=config.db_conn_args,
        pool_size=20,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )
elif config.db_type == "in_memory":
    engine = create_engine(
        url=config.db_url, future=True, connect_args=config.db_conn_args, poolclass=StaticPool
    )
else:
    engine = create_engine(
        url=config.db_url, future=True, connect_args=config.db_conn_args, poolclass=NullPool
    )


# We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.
SessionLocal = sessionmaker(bind=engine)


def initialise_db() -> None:
    """Recreate the database based on structure defined by models."""
    logger.info(f"Database URL: {engine.url}")
    logger.info("Creating database tables...")
    # Emit DDL to the DB - create DB
    # emit CREATE statements given ORM registry
    Base.metadata.create_all(engine)
    logger.info("Database tables created successfully")

    # Fill all default tables with initial/default data if they are empty
    with SessionLocal.begin() as session:
        if not session.query(ProductType).count():
            init_product_type_table(session=session)
        if not session.query(ProductLocation).count():
            init_product_location_table(session=session)


def reset_db() -> None:
    """Recreate the database based on structure defined by models."""
    # Emit DDL to the DB - create DB
    # emit CREATE statements given ORM registry
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Fill all default tables with initial/default data if they are empty
    with SessionLocal.begin() as session:
        init_product_location_table(session=session)
        init_product_type_table(session=session)


def get_session() -> Generator[Session]:
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
