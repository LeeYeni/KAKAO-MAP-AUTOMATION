from data_handler import DataHandler
from kakao_map import KakaoMap
from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv
import os

load_dotenv()
FILE_PATH = os.getenv("file_path")
FOLDER_NAME = os.getenv("folder_name")

api = FastAPI(title="kakao-map-automation")

@api.get("/")
def root() -> dict:
    return {"status": "serving is running"}

#---------- 1. 데이터 불러오기 & 전처리 ----------#
@api.get("/data_processor")
def data_processor() -> dict:
    data_handler = DataHandler(FILE_PATH)
    coords = data_handler.processor()
    return coords

#---------- 2. 카카오맵 '즐겨찾기 추가' 기능 수행 ----------#
@api.post("/kakao_map_task")
def kakao_map_automation(coords: dict) -> dict:
    kakao_map = KakaoMap()

    while True:
        if kakao_map.is_login():  # 로그인
            break

    kakao_map.click("skyview")  # 스카이뷰
    kakao_map.search_and_save(coords["coords"], FOLDER_NAME)  # 즐겨찾기 추가
    kakao_map.driver.quit()  # 브라우저 종료

    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("internal_api:api", host="0.0.0.0", port=8000)