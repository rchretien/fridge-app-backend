"""Data models for product."""

from datetime import datetime

from pydantic import BaseModel, Field

from fridge_app_backend.config import BRUSSELS_TZ
from fridge_app_backend.orm.enums.base_enums import (
    ProductLocationEnum,
    ProductTypeEnum,
    ProductUnitEnum,
)


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
    added_date: datetime = Field(
        default=datetime.now(tz=BRUSSELS_TZ),
        title="Product added date",
        min_length=1,
        max_length=64,
        description="Product added date",
    )
    expiration_date: datetime = Field(
        ...,
        title="Product expiration date",
        min_length=1,
        max_length=64,
        description="Product expiration date",
    )
    product_location: ProductLocationEnum = Field(
        ...,
        title="Product location",
        min_length=1,
        max_length=256,
        description="Product location",
    )
    product_type: ProductTypeEnum = Field(
        ...,
        title="Product type",
        min_length=1,
        max_length=256,
        description="Product type",
    )
    image_location: str = Field(
        ...,
        title="Product image location",
        min_length=1,
        max_length=256,
        description="Product image location on the server",
    )


class ProductCreate(ProductBase):
    """Create product."""


class ProductUpdate(ProductBase):
    """Update product."""


class ProductRead(ProductBase):
    """Read product model."""

    id: int = Field(..., title="Product ID", ge=1)

    class Config:
        """Pydantic configuration."""

        orm_mode = True
