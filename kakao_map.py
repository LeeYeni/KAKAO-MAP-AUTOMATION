from selenium import webdriver  # 셀레늄. 웹 브라우저 자동화.
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time

class KakaoMap():
    def __init__(self):
        # 브라우저 꺼짐 방지 옵션
        options = Options()
        options.add_experimental_option("detach", True)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        self.driver.maximize_window()

        self.driver.get("https://map.kakao.com/")

    #---------- 1. 로그인 여부 확인하는 메서드 ----------#
    def is_login(self) -> bool:
        while True:
            try:
                # 프로필 존재 여부 == 로그인 여부
                img = self.driver.find_element(By.CSS_SELECTOR, "#btnProfile")
                if img.is_displayed():
                    return True
            except (NoSuchElementException, StaleElementReferenceException):
                pass
            time.sleep(1)

    #---------- 2. element가 존재할 때 클릭하는 메서드 ----------#
    def click(self, class_name: str) -> None:
        WebDriverWait(self.driver, timeout=20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f".{class_name}"))
        )
        self.driver.find_element(By.CSS_SELECTOR, f".{class_name}").click()

    #---------- 3. 즐겨찾기 폴더가 존재할 때 클릭하는 메서드 ----------#
    def select_folder(self, folder_name: str) -> None:
        WebDriverWait(self.driver, timeout=20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f".txt_folder"))
        )
        folder_link = self.driver.find_element(
            By.XPATH,
            f"//strong[@class='txt_folder' and normalize-space(text())='{folder_name}']/ancestor::a"
        )
        folder_link.click()

    #---------- 4. 장소의 설명란에 장소명, 경위도를 입력하는 메서드 ----------#
    def input_info(self, input_name: str, id_name: str) -> None:
        memo_input = self.driver.find_element(By.ID, id_name)

        # readonly 속성 제거
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", memo_input)

        # 텍스트 입력
        memo_input.clear()
        memo_input.send_keys(input_name)

    #---------- 5. 장소 검색 후, 즐겨찾기에 저장하는 메서드 ----------#
    def search_and_save(self, coords: dict, folder_name: str) -> None:
        # coords = {
        #     "서울시청": (37.5665, 126.9780),
        #     "경복궁": (37.5700, 126.9827),
        #     "강남역": (37.4979, 127.0276),
        # }

        for idx, place, [x, y] in enumerate(coords.items(), start=1):
            # 경위도 검색
            search_box = self.driver.find_element(By.ID, "search.keyword.query")
            search_box.clear()
            search_box.send_keys(f"{x} {y}")
            search_box.send_keys(Keys.ENTER)

            # 즐겨찾기 클릭
            self.click("fav")

            self.select_folder(folder_name)  # 저장 위치(폴더)
            self.input_info(place, "display1")  # 장소명 작성
            self.input_info(f"위도: {x}, 경도: {y}", "favMemo")  # 경위도 작성
            self.click("btn_submit")  # 저장

            if idx % 10 == 0:
                time.sleep(10)  # 주기적으로 대기하여 API 요청 과부하 방지