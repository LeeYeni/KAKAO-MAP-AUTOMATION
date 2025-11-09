from fastapi import FastAPI

from data_handler import DataHandler
from kakao_map import KakaoMap

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