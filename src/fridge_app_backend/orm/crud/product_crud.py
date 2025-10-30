"""CRUD operations for the product model."""

from datetime import datetime

from sqlalchemy.orm import Session

from fridge_app_backend.config import config
from fridge_app_backend.orm.crud.base_crud import CRUDBase
from fridge_app_backend.orm.models.db_models import Product, ProductLocation, ProductType
from fridge_app_backend.orm.schemas.product_schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """CRUD operations for product model."""

    def encode_model(self, obj_in: ProductCreate, session: Session) -> Product:
        """Encode a ProductCreate Pydantic model to its SQLAlchemy model counterpart."""
        obj_dict = obj_in.model_dump(exclude_unset=True)

        # Get product type
        product_type = (
            session.query(ProductType).filter(ProductType.name == obj_dict["product_type"]).first()
        )

        # Get product location
        product_location = (
            session.query(ProductLocation)
            .filter(ProductLocation.name == obj_dict["product_location"])
            .first()
        )

        return Product(
            name=obj_dict["product_name"],
            description=obj_dict["description"],
            quantity=obj_dict["quantity"],
            unit=obj_dict["unit"],
            creation_date=datetime.now(tz=config.brussels_tz),
            expiry_date=obj_dict["expiry_date"],
            product_type=product_type,
            product_location=product_location,
            image_location="file_path",
        )

    def get_names_starting_with(self, product_name: str, session: Session) -> list[str]:
        """Get product names starting with a specific string."""
        return [
            row.name
            for row in session.query(Product.name)
            .filter(Product.name.ilike(f"{product_name}%"))
            .all()
        ]


product_crud = CRUDProduct(Product)
