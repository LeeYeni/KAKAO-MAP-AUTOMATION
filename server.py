from fastmcp import FastMCP

import httpx
import threading

API_BASE = "https://kakao-map-automation.onrender.com"

# MCP: Model Context Protocol. API 통역가.
mcp = FastMCP(name="kakao-map-automation")

@mcp.tool()
def kakao_map_automation(folder_name: str, file_path: str) -> dict:
    #---------- 1. 데이터 불러오기 & 전처리 ----------#
    response = httpx.get(
        f"{API_BASE}/data_processor",
        params={"file_path": file_path},
    )
    data = response.json()

    if data.get("status") != "success":
        return {
            "status": "error",
            "message": "데이터 처리 실패"
        }
    
    coords = data.get("coords")

    if not coords:  # coords가 비어있는지 확인
        return {
            "status": "error",
            "message": "추가할 장소 없음"
        }

    #---------- 2. 카카오맵 즐겨찾기 추가 자동화 ----------#
    response2 = httpx.post(
        f"{API_BASE}/kakao_map_task",
        json={"coords": coords, "folder_name": folder_name},
        timeout=httpx.Timeout(300.0),
    )

    data2 = response2.json()

    if data2.get("status") != "success":
        return {
            "status": "error",
            "message": "카카오맵 즐겨찾기 추가 실패"
        }

    return data2

if __name__ == "__main__":
    mcp.run()