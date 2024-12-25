"""Endpoints for utility functions."""

from fastapi import APIRouter

from fridge_app_backend.orm.crud.product_type_crud import product_type_crud

utils_router = APIRouter(
    prefix="/utils",
    tags=["Utilities"],
)


@utils_router.get("/product_type_list")
async def get_product_type_list() -> dict[str, list[str]]:
    """Get all product types."""
    return {"product_types": product_type_crud.get_all()}
