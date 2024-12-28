"""Base class for CRUD operations."""

from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, selectinload

from fridge_app_backend.exceptions import ModelNotHavingAttributeError
from fridge_app_backend.orm.enums.base_enums import OrderByEnum
from fridge_app_backend.orm.models.db_models import BaseWithID

ModelType = TypeVar("ModelType", bound=BaseWithID)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations.

    ModelType: SQLAlchemy model,
    CreateSchemaType: Pydantic schema for creating a new model instance,
    UpdateSchemaType: Pydantic schema for updating an existing model instance.
    """

    # Options to control how relationships are loaded when querying the database with the
    # recursive option. Can be overwritten in subclasses if needed.
    recursive_options = (selectinload("*"),)

    def __init__(self, model: type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""
        self.model = model

    def encode_model(self, obj_in: CreateSchemaType, session: Session) -> ModelType:
        """Encode a Pydantic model to a SQLAlchemy model."""
        return self.model(**jsonable_encoder(obj_in))

    def encode_update_model(self, obj_in: UpdateSchemaType, session: Session) -> ModelType:
        """Encode a Pydantic model to a SQLAlchemy model."""
        return self.model(**jsonable_encoder(obj_in))

    def get(self, session: Session, row_id: int) -> ModelType | None:
        """Get a single model instance by ID."""
        result: ModelType | None = session.get(self.model, row_id)
        return result

    def get_multi(
        self,
        session: Session,
        skip: int = 0,
        limit: int = 100,
        *,
        ascending: bool = False,
        order_by: OrderByEnum = OrderByEnum.ID,
    ) -> list[ModelType]:
        """Get multiple model instances."""
        if not hasattr(self.model, order_by.value):
            raise ModelNotHavingAttributeError(model=self.model, attribute=order_by.value)

        # Base query statement
        base_statement = (
            select(self.model)
            .order_by(
                getattr(self.model, order_by.value).asc()
                if ascending
                else getattr(self.model, order_by.value).desc()
            )
            .offset(skip)
            .limit(limit)
        )

        return list(session.scalars(base_statement).all())

    def get_all(self, session: Session) -> list[ModelType]:
        """Get all model instances."""
        return session.query(self.model).all()

    def create(self, session: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new database record."""
        db_obj = self.encode_model(obj_in, session)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def create_multi(self, session: Session, obj_in: list[CreateSchemaType]) -> list[ModelType]:
        """Create multiple database records."""
        db_objs = [self.encode_model(obj, session) for obj in obj_in]
        session.add_all(db_objs)
        session.commit()
        for db_obj in db_objs:
            session.refresh(db_obj)
        return db_objs

    def update(self, session: Session, row_id: int, obj_in: UpdateSchemaType) -> ModelType:
        """Update an existing database record."""
        db_obj = session.get(self.model, row_id)

        # Check if the object exists
        if db_obj is None:
            raise NoResultFound

        # Check if all fields are present in the object
        update_data = self.encode_update_model(obj_in, session)
        for field, value in update_data.__dict__.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        # Update the object
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

        return db_obj

    def remove(self, session: Session, row_id: int) -> ModelType:
        """Delete a database record."""
        db_obj = session.get(self.model, row_id)

        # Check if the object exists
        if db_obj is None:
            raise NoResultFound

        session.delete(db_obj)
        session.commit()
        return db_obj
