import logging
import os

from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP

import services

# Standard Azure logging: Application Insights when configured, plus stdout for the App Service log stream.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    from azure.monitor.opentelemetry import configure_azure_monitor

    configure_azure_monitor(logger_name="app")
logger = logging.getLogger("app")

# --- MCP surface (for agents) ---
mcp = FastMCP("Combo Starter")


@mcp.tool
def list_products(category: str | None = None) -> list[dict]:
    """List products, optionally filtered by category (outdoor, office, kitchen)."""
    return services.list_products(category)


@mcp.tool
def get_product(product_id: str) -> dict:
    """Get a single product by id, e.g. P-100."""
    product = services.get_product(product_id)
    if product is None:
        raise ValueError(f"Product {product_id} not found")
    return product


@mcp.tool
def get_order(order_id: str) -> dict:
    """Get an order, including its total, by id, e.g. O-1."""
    order = services.get_order(order_id)
    if order is None:
        raise ValueError(f"Order {order_id} not found")
    return order


mcp_app = mcp.http_app(path="/", stateless_http=True)

# --- REST surface (for apps) ---
# The MCP app's lifespan must be passed to FastAPI so the MCP session manager starts.
app = FastAPI(title="Combo Starter", lifespan=mcp_app.lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/products")
def api_list_products(category: str | None = None):
    return services.list_products(category)


@app.get("/api/products/{product_id}")
def api_get_product(product_id: str):
    product = services.get_product(product_id)
    if product is None:
        raise HTTPException(404, f"Product {product_id} not found")
    return product


@app.get("/api/orders/{order_id}")
def api_get_order(order_id: str):
    order = services.get_order(order_id)
    if order is None:
        raise HTTPException(404, f"Order {order_id} not found")
    return order


app.mount("/mcp", mcp_app)
