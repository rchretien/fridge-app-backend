"""CRUD operations for the product model."""

from datetime import datetime
from types import SimpleNamespace
from typing import Any

from sqlalchemy.orm import Session

from fridge_app_backend.config import config
from fridge_app_backend.orm.crud.base_crud import CRUDBase
from fridge_app_backend.orm.models.db_models import Product, ProductLocation, ProductType
from fridge_app_backend.orm.schemas.product_schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """CRUD operations for product model."""

    def _collect_scalar_values(self, obj_dict: dict[str, Any], session: Session) -> dict[str, Any]:
        """Resolve foreign keys and map external names to model column names."""
        product_type = (
            session.query(ProductType).filter(ProductType.name == obj_dict["product_type"]).first()
        )
        product_location = (
            session.query(ProductLocation)
            .filter(ProductLocation.name == obj_dict["product_location"])
            .first()
        )

        return {
            "name": obj_dict["product_name"],
            "description": obj_dict["description"],
            "quantity": obj_dict["quantity"],
            "unit": obj_dict["unit"],
            "expiry_date": obj_dict["expiry_date"],
            "product_type_id": product_type.id if product_type else None,
            "product_location_id": product_location.id if product_location else None,
        }

    def encode_model(self, obj_in: ProductCreate, session: Session) -> Product:
        """Encode a ProductCreate Pydantic model to its SQLAlchemy model counterpart."""
        obj_dict = obj_in.model_dump(exclude_unset=True)
        scalar_values = self._collect_scalar_values(obj_dict, session)
        return Product(
            creation_date=datetime.now(tz=config.brussels_tz),
            image_location="file_path",
            **scalar_values,
        )

    def encode_update_model(self, obj_in: ProductUpdate, session: Session) -> SimpleNamespace:
        """Encode a ProductUpdate Pydantic model to a namespace of scalar columns."""
        obj_dict = obj_in.model_dump(exclude_unset=True)
        scalar_values = self._collect_scalar_values(obj_dict, session)
        return SimpleNamespace(**scalar_values)

    def get_names_starting_with(self, product_name: str, session: Session) -> list[str]:
        """Get product names starting with a specific string."""
        return [
            row.name
            for row in session.query(Product.name)
            .filter(Product.name.ilike(f"{product_name}%"))
            .all()
        ]


product_crud = CRUDProduct(Product)
