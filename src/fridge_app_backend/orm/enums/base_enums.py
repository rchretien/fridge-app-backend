"""Enumeration classes for the ORM models and CRUD classes."""

from enum import Enum


class OrderByEnum(str, Enum):
    """Enumeration for ordering options."""

    ID = "id"
    NAME = "name"
    CREATED_AT = "created_at"
    EXPIRY_DATE = "expiry_date"
