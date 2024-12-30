"""Dependencies for product routes."""

from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from fridge_app_backend.orm.crud.product_crud import product_crud
from fridge_app_backend.orm.database import get_session
from fridge_app_backend.orm.models.db_models import Product

SessionDependency = Annotated[Session, Depends(get_session)]


def get_db_product(product_id: int, session: SessionDependency) -> Product:
    """Get a product from the database."""
    product = product_crud.get(session=session, row_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Product not found in the database."
        )
    return product


ProductDependency = Annotated[Product, Depends(get_db_product)]
