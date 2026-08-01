"""Shared ORM constants."""

from frozen_vault_backend.orm.enums.base_enums import ProductTypeEnum

PRODUCT_TYPE_CATEGORY: dict[ProductTypeEnum, ProductTypeEnum] = {
    ProductTypeEnum.CHICKEN: ProductTypeEnum.POULTRY,
    ProductTypeEnum.TURKEY: ProductTypeEnum.POULTRY,
    ProductTypeEnum.PORK: ProductTypeEnum.MEAT,
    ProductTypeEnum.BEEF: ProductTypeEnum.MEAT,
    ProductTypeEnum.SALMON_TROUT: ProductTypeEnum.FISH,
    ProductTypeEnum.SAITHE: ProductTypeEnum.FISH,
    ProductTypeEnum.NILE_PERCH: ProductTypeEnum.FISH,
    ProductTypeEnum.SALMON: ProductTypeEnum.FISH,
    ProductTypeEnum.REDFISH: ProductTypeEnum.FISH,
    ProductTypeEnum.WHITING: ProductTypeEnum.FISH,
}

# Application policy for best-quality storage at -18 C using the existing broad product types.
FREEZER_STORAGE_DAYS: dict[ProductTypeEnum, int] = {
    ProductTypeEnum.POULTRY: 270,
    ProductTypeEnum.MEAT: 270,
    ProductTypeEnum.FISH: 180,
    ProductTypeEnum.SEAFOOD: 120,
    ProductTypeEnum.VEGETABLE: 60,
    ProductTypeEnum.LIQUID: 120,
    ProductTypeEnum.FRUIT: 90,
    ProductTypeEnum.DESSERT: 120,
    ProductTypeEnum.DAIRY: 90,
    ProductTypeEnum.PREPARATIONS: 120,
}
