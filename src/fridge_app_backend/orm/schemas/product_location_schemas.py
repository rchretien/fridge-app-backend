"""Data models for product location."""

from pydantic import BaseModel, Field

from fridge_app_backend.orm.enums.base_enums import ProductLocationEnum


class ProductLocationBase(BaseModel):
    """Base class for product location."""

    name: ProductLocationEnum = Field(
        ..., title="Product location name", min_length=1, max_length=50
    )


class ProductLocationCreate(ProductLocationBase):
    """Create product location."""


class ProductLocationUpdate(ProductLocationBase):
    """Update product location."""


class ProductLocationRead(ProductLocationBase):
    """Read product location model."""

    id: int = Field(..., title="Product location ID", ge=1)

    class Config:
        """Pydantic configuration."""

        orm_mode = True
