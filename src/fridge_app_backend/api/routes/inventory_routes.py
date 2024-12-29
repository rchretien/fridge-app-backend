"""Endpoints for interacting with the fridge inventory."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from fridge_app_backend.orm.crud.product_crud import product_crud
from fridge_app_backend.orm.database import get_session
from fridge_app_backend.orm.schemas.product_schemas import (
    CreatedProduct,
    ProductCreate,
    ProductReadList,
)

inventory_router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@inventory_router.post(
    "/create",
    response_model=CreatedProduct,
    responses={HTTP_201_CREATED: {"model": CreatedProduct}},
    status_code=HTTP_201_CREATED,
)
async def create_product(
    create_product_in: ProductCreate,
    session: Session = Depends(get_session),  # noqa: B008
) -> CreatedProduct:
    """Create a new product."""
    return CreatedProduct.from_model(product_crud.create(session, obj_in=create_product_in))


@inventory_router.get("/list", response_model=ProductReadList)
async def get_product_list() -> ProductReadList:
    """Get all products."""
    return ...


@inventory_router.patch("/update")
async def update_product() -> dict[str, str]:
    """Update a product."""
    return {"message": "Update a product"}


@inventory_router.delete("/delete")
async def delete_product() -> dict[str, str]:
    """Delete a product."""
    return {"message": "Delete a product"}
