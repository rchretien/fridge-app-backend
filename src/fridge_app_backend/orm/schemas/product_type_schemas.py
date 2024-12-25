"""Data models for product type."""

from pydantic import BaseModel, Field


class ProductTypeBase(BaseModel):
    """Base class for product type."""

    name: str = Field(..., title="Product type name", min_length=1, max_length=50)


class ProductTypeCreate(ProductTypeBase):
    """Create product type."""


class ProductTypeUpdate(ProductTypeBase):
    """Update product type."""


class ProductTypeRead(ProductTypeBase):
    """Read product type model."""

    id: int = Field(..., title="Product type ID", ge=1)

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class ProductTypeReadList(BaseModel):
    """Read product type list."""

    product_types: list[ProductTypeRead] = Field(
        ..., title="Product types", description="Product type list"
    )
    next_skip: int = Field(
        ..., title="Next skip", ge=0, description="Database index of the last item retrieved"
    )
    total_items: int = Field(
        ..., title="Total items", ge=0, description="Total number of items in the database"
    )

    class Config:
        """Pydantic configuration."""

        orm_mode = True
