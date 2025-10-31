"""Add seed data for product types and locations

Revision ID: 4fa661ad883c
Revises: ea84b5ce47e9
Create Date: 2025-10-31 11:47:50.862786

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4fa661ad883c"
down_revision: str | Sequence[str] | None = "ea84b5ce47e9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add seed data from enums."""
    from fridge_app_backend.orm.enums.base_enums import ProductLocationEnum, ProductTypeEnum

    # Insert product types
    product_type_table = sa.table("product_type", sa.column("name", sa.String))
    op.bulk_insert(product_type_table, [{"name": pt.value} for pt in ProductTypeEnum])

    # Insert product locations
    product_location_table = sa.table("product_location", sa.column("name", sa.String))
    op.bulk_insert(product_location_table, [{"name": pl.value} for pl in ProductLocationEnum])


def downgrade() -> None:
    """Remove seed data."""
    op.execute("DELETE FROM product_type")
    op.execute("DELETE FROM product_location")
