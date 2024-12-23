"""SQLAlchemy ORM model definitions for the fridge app backend."""

import json
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from fridge_app_backend.orm.config import LOCATION_LIST_FILE_PATH, PRODUCT_TYPE_LIST_FILE_PATH


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class BaseWithID(Base):
    """Base class for all ORM with an ID field."""

    __abstract__ = True

    # ID field used as primary key
    id = mapped_column(Integer, primary_key=True, index=True)


class ProductType(BaseWithID):
    """Product type model."""

    __tablename__ = "product_type"

    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Relationship with the Product model (one-to-many)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="product_type")


class ProductLocation(BaseWithID):
    """Location model."""

    __tablename__ = "product_location"

    name: Mapped[str] = mapped_column(String, unique=True)

    # Relationship with the Product model (one-to-many)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="product_location")


class Product(BaseWithID):
    """Product model."""

    __tablename__ = "product"

    # Define columns
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer, CheckConstraint("quantity >= 1"))
    unit: Mapped[str] = mapped_column(
        String,
        CheckConstraint(sqltext="unit IN ('g', 'boxes', 'bottles')", name="unit_check"),
        default="g",
        nullable=False,
    )
    added_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationship with the ProductType model (many-to-one)
    product_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_type.id"), nullable=False
    )
    product_type: Mapped[ProductType] = relationship(
        ProductType, back_populates="products", single_parent=True, cascade="all, delete-orphan"
    )

    # Relationship with the ProductLocation model (many-to-one)
    product_location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_location.id"), nullable=False
    )
    product_location: Mapped[ProductLocation] = relationship(
        ProductLocation, back_populates="products", single_parent=True, cascade="all, delete-orphan"
    )

    # Adding check constraints spanning several columns to the table
    __table_args__ = (
        CheckConstraint(sqltext="expiration_date > added_date", name="expiration_date_check"),
    )


def init_product_type_table(session: Session) -> None:
    """Initialise the product type table with default data."""
    with PRODUCT_TYPE_LIST_FILE_PATH.open("r") as file:
        product_type_list = json.load(file)

    # Insert default data into the table
    session.add_all(
        [
            ProductType(name=product_type["name"])
            for product_type in product_type_list["product_type_list"]
        ]
    )


def init_product_location_table(session: Session) -> None:
    """Initialise the location table with default data."""
    with LOCATION_LIST_FILE_PATH.open("r") as file:
        product_location_list = json.load(file)

    # Insert default data into the table
    session.add_all(
        [
            ProductLocation(name=product_location["name"])
            for product_location in product_location_list["product_location_list"]
        ]
    )
