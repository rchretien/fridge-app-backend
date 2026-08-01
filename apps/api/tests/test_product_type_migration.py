"""Tests for detailed product type migration behavior."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations


def _load_migration() -> ModuleType:
    """Load the data migration as a module without making Alembic a package."""
    path = (
        Path(__file__).resolve().parents[1]
        / "alembic/versions/8f4c2d9a1b6e_add_detailed_meat_and_fish_types.py"
    )
    spec = spec_from_file_location("detailed_product_types_migration", path)
    assert spec is not None and spec.loader is not None
    migration = module_from_spec(spec)
    spec.loader.exec_module(migration)
    return migration


def test_downgrade_remaps_detailed_types_before_removing_them() -> None:
    """Referenced detailed types should become broad types during rollback."""
    metadata = sa.MetaData()
    product_type = sa.Table(
        "product_type",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, unique=True, nullable=False),
    )
    product = sa.Table(
        "product",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("product_type_id", sa.Integer, sa.ForeignKey("product_type.id"), nullable=False),
    )
    engine = sa.create_engine("sqlite://")

    with engine.begin() as connection:
        metadata.create_all(connection)
        type_names = (
            "meat 🥩",
            "poultry 🍗",
            "fish 🐟",
            "pork 🐖",
            "chicken 🍗",
            "salmon 🐟",
            "beef 🥩",
        )
        connection.execute(sa.insert(product_type), [{"name": name} for name in type_names])
        type_ids = {
            name: type_id
            for name, type_id in connection.execute(
                sa.select(product_type.c.name, product_type.c.id)
            )
        }
        connection.execute(
            sa.insert(product),
            [
                {"product_type_id": type_ids["pork 🐖"]},
                {"product_type_id": type_ids["chicken 🍗"]},
                {"product_type_id": type_ids["salmon 🐟"]},
            ],
        )

        context = MigrationContext.configure(connection)
        with Operations.context(context):
            _load_migration().downgrade()

        remaining_types = set(connection.scalars(sa.select(product_type.c.name)))
        product_types = list(
            connection.scalars(
                sa.select(product_type.c.name)
                .select_from(product.join(product_type))
                .order_by(product.c.id)
            )
        )

    assert remaining_types == {"meat 🥩", "poultry 🍗", "fish 🐟"}
    assert product_types == ["meat 🥩", "poultry 🍗", "fish 🐟"]
