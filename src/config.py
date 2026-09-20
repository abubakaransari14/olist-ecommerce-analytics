from pathlib import Path

# X------------- PROJECT PATHS ---------------X

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DATA_DIR = DATA_DIR / "exports"

REPORTS_DIR = PROJECT_ROOT / "reports"

DATA_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# X-------- CREATE REQUIRED DIRECTORY ----------X

PROCESSED_DATA_DIR.mkdir(
    parents = True,
    exist_ok = True
)

EXPORTS_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


