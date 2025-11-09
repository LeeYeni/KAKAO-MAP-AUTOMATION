from fastmcp import FastMCP
from fastapi import FastAPI
import httpx
from dotenv import load_dotenv
import os
import threading

from data_handler import DataHandler
from kakao_map import KakaoMap

API_BASE = "https://kakao-map-automation.onrender.com"

api = FastAPI(title="kakao-map-automation")

@api.get("/")
def root() -> dict:
    return {"status": "serving is running"}

#---------- 1. 데이터 불러오기 & 전처리 ----------#
@api.get("/data_processor")
def data_processor(file_path: str) -> dict:
    data_handler = DataHandler(file_path)
    coords = data_handler.processor()
    return coords

#---------- 2. 카카오맵 '즐겨찾기 추가' 기능 수행 ----------#
@api.post("/kakao_map_task")
def kakao_map_task(data: dict) -> dict:
    kakao_map = KakaoMap()

    while True:
        if kakao_map.is_login():  # 로그인
            break

    kakao_map.click("skyview")  # 스카이뷰
    kakao_map.search_and_save(data["coords"], data["folder_name"])  # 즐겨찾기 추가
    kakao_map.driver.quit()  # 브라우저 종료

    return {"status": "success"}

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

def run_mcp():
    mcp.run()

threading.Thread(target=run_mcp, daemon=True).start()