"""SQLAlchemy ORM model definitions for the fridge app backend."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class BaseWithID(Base):
    """Base class for all ORM with an ID field."""

    __abstract__ = True

    # ID field used as primary key
    id = Column(Integer, primary_key=True, index=True)


class ProductCategory(BaseWithID):
    """Product category model."""

    __tablename__ = "product_category"

    name = Column(String, unique=True)


class Product(BaseWithID):
    """Product model."""

    __tablename__ = "product"

    name = Column(String, unique=True)
    category_id = Column(Integer)
    description = Column(String)
    quantity = Column(Integer)
    unit = Column(String, default="g")
    added_date = Column(String)
    expiration_date = Column(String)
    location = Column(String)
