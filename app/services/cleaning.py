from typing import Dict, Any


def clean_product(raw_product: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply simple cleaning rules to product data.
    """
    product = raw_product.copy()

    # Normalize name and category
    if "name" in product and isinstance(product["name"], str):
        product["name"] = product["name"].strip()

    if "category" in product and isinstance(product["category"], str):
        product["category"] = product["category"].strip().lower()

    # Ensure price is float
    if "price" in product:
        product["price"] = float(product["price"])

    # Default currency if missing
    if "currency" not in product or not product["currency"]:
        product["currency"] = "INR"

    # Default in_stock if missing
    if "in_stock" not in product:
        product["in_stock"] = True

    return product


def clean_order(raw_order: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply simple cleaning rules to order data.
    """
    order = raw_order.copy()

    # Strip strings
    for key in ["order_id", "user_id"]:
        if key in order and isinstance(order[key], str):
            order[key] = order[key].strip()

    # Ensure total_amount is float
    if "total_amount" in order:
        order["total_amount"] = float(order["total_amount"])

    # Default currency
    if "currency" not in order or not order["currency"]:
        order["currency"] = "INR"

    # Items: ensure quantity is int
    if "items" in order and isinstance(order["items"], list):
        for item in order["items"]:
            if "quantity" in item:
                item["quantity"] = int(item["quantity"])

    return order
