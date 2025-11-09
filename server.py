from fastmcp import FastMCP

import httpx
import threading

API_BASE = "https://kakao-map-automation.onrender.com"

# MCP: Model Context Protocol. API 통역가.
mcp = FastMCP(name="kakao-map-automation")

@mcp.tool()
def kakao_map_automation(folder_name: str, file_path: str) -> dict:
    response = httpx.get(f"{API_BASE}/data_processor", params={"file_path": file_path})
    coords = response.json()

    post_response = httpx.post(
        f"{API_BASE}/kakao_map_task",
        json={"coords": coords, "folder_name": folder_name},
        timeout=httpx.Timeout(300.0)
    )

    return post_response.json()

if __name__ == "__main__":
    mcp.run()