"""Endpoints for interacting with the fridge inventory."""

from fastapi import APIRouter

inventory_router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@inventory_router.post("/create")
async def create_product() -> dict[str, str]:
    """Create a new product."""
    return {"message": "Create a new product"}


@inventory_router.get("/list")
async def get_product_list() -> dict[str, str]:
    """Get all products."""
    return {"message": "Get all products"}


@inventory_router.patch("/update")
async def update_product() -> dict[str, str]:
    """Update a product."""
    return {"message": "Update a product"}


@inventory_router.delete("/delete")
async def delete_product() -> dict[str, str]:
    """Delete a product."""
    return {"message": "Delete a product"}
