"""Data models for product."""

import re
from datetime import datetime, timedelta
from typing import Self

from pydantic import BaseModel, Field, field_validator

from fridge_app_backend.config import BRUSSELS_TZ
from fridge_app_backend.orm.enums.base_enums import (
    ProductLocationEnum,
    ProductTypeEnum,
    ProductUnitEnum,
)
from fridge_app_backend.orm.models.db_models import Product


class ProductBase(BaseModel):
    """Base class for product."""

    name: str = Field(
        ..., title="Product name", min_length=1, max_length=50, description="Product name"
    )
    description: str = Field(
        ...,
        title="Product description",
        min_length=1,
        max_length=256,
        description="Product description",
    )
    quantity: int = Field(..., title="Product quantity", ge=1, description="Product quantity")
    unit: ProductUnitEnum = Field(
        ..., title="Product unit", min_length=1, max_length=50, description="Product unit"
    )
    expiration_date: datetime = Field(
        ...,
        title="Product expiration date",
        description="Product expiration date",
        examples=[datetime.now(tz=BRUSSELS_TZ) + timedelta(hours=1)],
    )
    product_location: ProductLocationEnum = Field(
        ...,
        title="Product location",
        description="Product location",
    )
    product_type: ProductTypeEnum = Field(
        ...,
        title="Product type",
        description="Product type",
    )


class ProductCreate(ProductBase):
    """Create product."""


class ProductUpdate(ProductBase):
    """Update product."""


class ProductRead(ProductBase):
    """Read product model."""

    id: int = Field(..., title="Product ID", ge=1)
    added_date: datetime = Field(
        ...,
        title="Product added date",
        description="Product added date",
    )
    image_location: str = Field(
        ...,
        title="Product image location",
        min_length=1,
        max_length=256,
        description="Product image location on the server",
    )

    class Config:
        """Pydantic configuration."""

        orm_mode = True

    @field_validator("image_location")
    @classmethod
    def validate_image_location(cls, value: str) -> str:
        """Validate if image location is a valid UNIX file path."""

        def is_valid_unix_file_path(file_path: str) -> bool:
            """Check if a string is a valid UNIX file path."""
            pattern = re.compile(r"^(\/)?([^/\0]+(\/)?)+$")
            return bool(pattern.match(file_path))

        if not is_valid_unix_file_path(value):
            raise ValueError("Invalid UNIX file path")  # noqa: EM101, TRY003
        return value


class ProductReadList(BaseModel):
    """List of product models."""

    products: list[ProductRead] = Field(..., title="List of products")
    next_skip: int = Field(
        ...,
        description="Database index of the last product in the list.",
        ge=0,
    )
    total: int = Field(
        ...,
        description="Total number of products the endpoint can return when called with a given sequence of filters.",
        ge=0,
    )

    class Config:
        """Pydantic configuration."""

        orm_mode = True

    @classmethod
    def from_db_products(
        cls, product_list: list[Product], skip: int, limit: int, total: int
    ) -> Self:
        """Create a ProductReadList instance from a list of Product model instances."""
        return cls(
            products=[ProductRead.from_model(product) for product in product_list],
            next_skip=skip + min(limit, len(product_list)),
            total=total,
        )


class CreatedProduct(BaseModel):
    """Data model for a created product."""

    product_id: int = Field(..., description="ID of the created product.")
    message: str = Field(..., description="Message about the created product")

    @classmethod
    def from_model(cls, model: Product) -> Self:
        """Create a CreatedProduct instance from a Product model instance."""
        return cls(product_id=model.id, message="Product created successfully")
