"""Business logic shared by the REST API and the MCP server. Data is fake and in-memory."""

import logging

logger = logging.getLogger("app.services")

PRODUCTS = [
    {"id": "P-100", "name": "Trail Backpack", "category": "outdoor", "price": 89.99, "stock": 24},
    {"id": "P-101", "name": "Insulated Bottle", "category": "outdoor", "price": 24.50, "stock": 130},
    {"id": "P-200", "name": "Mechanical Keyboard", "category": "office", "price": 119.00, "stock": 8},
    {"id": "P-201", "name": "Standing Desk Mat", "category": "office", "price": 45.00, "stock": 0},
    {"id": "P-300", "name": "Espresso Grinder", "category": "kitchen", "price": 149.95, "stock": 12},
]

ORDERS = [
    {"id": "O-1", "customer": "Contoso", "status": "shipped", "items": [{"product_id": "P-100", "qty": 2}]},
    {"id": "O-2", "customer": "Fabrikam", "status": "processing", "items": [{"product_id": "P-200", "qty": 1}, {"product_id": "P-101", "qty": 3}]},
    {"id": "O-3", "customer": "Northwind", "status": "cancelled", "items": [{"product_id": "P-300", "qty": 1}]},
]


def list_products(category: str | None = None) -> list[dict]:
    logger.info("list_products category=%s", category)
    if category:
        return [p for p in PRODUCTS if p["category"] == category.lower()]
    return PRODUCTS


def get_product(product_id: str) -> dict | None:
    logger.info("get_product id=%s", product_id)
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def get_order(order_id: str) -> dict | None:
    logger.info("get_order id=%s", order_id)
    order = next((o for o in ORDERS if o["id"] == order_id), None)
    if order is None:
        return None
    total = sum(get_product(i["product_id"])["price"] * i["qty"] for i in order["items"])
    return {**order, "total": round(total, 2)}
