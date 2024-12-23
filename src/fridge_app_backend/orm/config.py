"""Configuration for the ORM."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LOCATION_LIST_FILE_PATH = ROOT_DIR / "data/location_list.json"
PRODUCT_TYPE_LIST_FILE_PATH = ROOT_DIR / "data/product_type_list.json"
