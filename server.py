from fastmcp import FastMCP
import httpx
from dotenv import load_dotenv
import os

load_dotenv()
API_BASE = os.getenv("api_base")

# MCP: Model Context Protocol. API 통역가.
mcp = FastMCP(name="kakao-map-automation")

@mcp.tool()
def kakao_map_automation() -> dict:
    response = httpx.get(f"{API_BASE}/data_processor")
    coords = response.json()

    post_response = httpx.post(
        f"{API_BASE}/kakao_map_task",
        json={"coords": coords},
        timeout=httpx.Timeout(300.0)
    )

    return post_response.json()

if __name__ == "__main__":
    mcp.run()