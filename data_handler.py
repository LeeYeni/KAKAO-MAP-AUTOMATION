import pandas as pd
import openpyxl

class DataHandler():
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path, engine="openpyxl")
        print(self.df)
        self.df.columns = ["name", "x", "y"]

    def processor(self):
        """
        coords = {
            "서울시청": (37.5665, 126.9780),
            "경복궁": (37.5700, 126.9827),
            "강남역": (37.4979, 127.0276),
        }
        """
        coords = {row["name"]: (row.x, row.y) for _, row in self.df.iterrows()}
        return coords