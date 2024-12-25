"""Data models for product category."""

from pydantic import BaseModel, Field


class ProductCategoryBase(BaseModel):
    """Base class for product category."""

    name: str = Field(..., title="Product category name", min_length=1, max_length=50)


class ProductCategoryCreate(ProductCategoryBase):
    """Create product category."""


class ProductCategoryUpdate(ProductCategoryBase):
    """Update product category."""


class ProductCategoryRead(ProductCategoryBase):
    """Read product category model."""

    id: int = Field(..., title="Product category ID", ge=1)

    class Config:
        """Pydantic configuration."""

        orm_mode = True
