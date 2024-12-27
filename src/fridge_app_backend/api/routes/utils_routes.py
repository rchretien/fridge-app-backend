"""Endpoints for utility functions."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fridge_app_backend.orm.crud.product_type_crud import product_type_crud
from fridge_app_backend.orm.database import get_session
from fridge_app_backend.orm.schemas.product_type_schemas import ProductTypeReadList

utils_router = APIRouter(
    prefix="/utils",
    tags=["Utilities"],
)


@utils_router.get("/product_type_list")
async def get_product_type_list(
    *,
    session: Session = Depends(get_session),  # noqa: B008
) -> ProductTypeReadList:
    """Get all product types."""
    return ProductTypeReadList.from_db_product_type_list(
        product_type_list=product_type_crud.get_all(session)
    )
