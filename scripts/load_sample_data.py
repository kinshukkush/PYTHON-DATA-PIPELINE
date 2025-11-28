import json
import os
from pathlib import Path

from app.db import products_collection, orders_collection
from app.services.cleaning import clean_product, clean_order

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_products():
    file_path = DATA_DIR / "sample_products.json"
    with open(file_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    cleaned = [clean_product(p) for p in products]
    products_collection.insert_many(cleaned)
    print(f"Inserted {len(cleaned)} products")


def load_orders():
    file_path = DATA_DIR / "sample_orders.json"
    with open(file_path, "r", encoding="utf-8") as f:
        orders = json.load(f)

    cleaned = [clean_order(o) for o in orders]
    orders_collection.insert_many(cleaned)
    print(f"Inserted {len(cleaned)} orders")


if __name__ == "__main__":
    load_products()
    load_orders()
