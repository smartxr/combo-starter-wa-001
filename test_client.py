"""Smoke test: calls the REST API and the MCP endpoint of a running instance."""

import asyncio
import json
import sys
from urllib.request import urlopen

from fastmcp import Client

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"


async def main():
    with urlopen(f"{BASE}/api/orders/O-2") as r:
        rest = json.load(r)
    print("REST:", rest)

    async with Client(f"{BASE}/mcp/") as client:
        print("MCP tools:", [t.name for t in await client.list_tools()])
        result = await client.call_tool("get_order", {"order_id": "O-2"})
        print("MCP:", result.data)
        assert result.data == rest, "REST and MCP results differ"
    print("OK: parity")


asyncio.run(main())
