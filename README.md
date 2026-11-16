# Combo Starter: FastAPI + FastMCP on Azure App Service

One Python app, two front-ends over the same fake data (`services.py`):

| Surface | Path | Audience |
|---|---|---|
| REST API | `/api/products`, `/api/products/{id}`, `/api/orders/{id}`, `/health`, `/docs` | apps |
| MCP (Streamable HTTP, stateless) | `/mcp/` | agents |

## Run locally
```
pip install -r requirements.txt
python -m uvicorn main:app --port 8000
uvicorn main:app --port 8000
python test_client.py          # calls REST and MCP, asserts same result
```

## Deploy (Linux App Service, Python 3.12+)
```
az webapp up --name <app> --resource-group <rg> --runtime "PYTHON:3.13" --sku B1
az webapp config set -g <rg> -n <app> --startup-file "bash startup.sh"
```

## Logging
- stdout goes to the App Service log stream (`az webapp log tail`).
- Set `APPLICATIONINSIGHTS_CONNECTION_STRING` in app settings to send logs, traces and requests to Application Insights.
