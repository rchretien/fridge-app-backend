"""Add detailed meat and fish product types.

Revision ID: 8f4c2d9a1b6e
Revises: 37a5a7b73d4a
Create Date: 2026-07-23
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8f4c2d9a1b6e"
down_revision: str | Sequence[str] | None = "37a5a7b73d4a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TYPE_CATEGORY = {
    "pork 🐖": "meat 🥩",
    "chicken 🍗": "poultry 🍗",
    "turkey 🦃": "poultry 🍗",
    "beef 🥩": "meat 🥩",
    "salmon trout 🐟": "fish 🐟",
    "saithe 🐟": "fish 🐟",
    "nile perch 🐟": "fish 🐟",
    "salmon 🐟": "fish 🐟",
    "redfish 🐟": "fish 🐟",
    "whiting 🐟": "fish 🐟",
}
PRODUCT_TYPES = tuple(TYPE_CATEGORY)


def upgrade() -> None:
    """Seed detailed types in databases created before they existed."""
    product_type = sa.table(
        "product_type", sa.column("id", sa.Integer), sa.column("name", sa.String)
    )
    connection = op.get_bind()
    existing = set(
        connection.scalars(
            sa.select(product_type.c.name).where(product_type.c.name.in_(PRODUCT_TYPES))
        )
    )
    missing = [
        {"name": product_type_name}
        for product_type_name in PRODUCT_TYPES
        if product_type_name not in existing
    ]
    if missing:
        connection.execute(sa.insert(product_type), missing)


def downgrade() -> None:
    """Remap detailed types to broad categories, then remove them."""
    product_type = sa.table(
        "product_type", sa.column("id", sa.Integer), sa.column("name", sa.String)
    )
    product = sa.table("product", sa.column("product_type_id", sa.Integer))
    connection = op.get_bind()
    type_ids = {
        name: type_id
        for type_id, name in connection.execute(
            sa.select(product_type.c.id, product_type.c.name).where(
                product_type.c.name.in_(set(TYPE_CATEGORY) | set(TYPE_CATEGORY.values()))
            )
        )
    }
    for detailed_type, category in TYPE_CATEGORY.items():
        detailed_type_id = type_ids.get(detailed_type)
        if detailed_type_id is not None:
            connection.execute(
                sa.update(product)
                .where(product.c.product_type_id == detailed_type_id)
                .values(product_type_id=type_ids[category])
            )

    connection.execute(sa.delete(product_type).where(product_type.c.name.in_(PRODUCT_TYPES)))
