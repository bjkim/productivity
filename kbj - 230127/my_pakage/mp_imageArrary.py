import openpyxl as op

# 이미지 삽입을 위한 openpyxl 모듈의 Image 클래스 import
from openpyxl.drawing.image import Image as openImage
from tkinter import *
import os
import math

############


class ImageArray:  # (Frame):
    EXCEL_COL = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    PIXEL = 37.7952755906

    def __init__(self):
        # super().__init__(master)
        pass

    def print(self, text):
        pass

    def image_array(
        self,
        _root_name: str = 0,
        _root_files: list = 0,
        _line_num: int = 10,
        _y_axis_size_scale: float = 14.38,
        _array_file_extension: str = "jpg",
        _axis_array_setting: int = 1,
        _file_name: str = "result",
    ):

        wb = op.Workbook()
        ws = wb.active

        _array_file_extension = "." + _array_file_extension

        filenames = []
        for file in _root_files:
            filename, ext = os.path.splitext(file)
            # print(filename + "\t" + ext)
            if ext == _array_file_extension or ext == _array_file_extension.upper():
                filenames.append(filename)

        print("파일 갯수", len(filenames))

        if len(filenames) == 0:
            return

        extension_cnt = 0

        y_axis_size = round(float(_y_axis_size_scale) * 0.14 + 0.38, 2)

        for row_line in range(math.ceil((len(filenames) / _line_num))):
            for file_cnt in range(_line_num):

                if extension_cnt >= len(filenames):
                    break

                # Image 클래스의 객체 img 선언 : Image 클래스 선언시 매개변수는 이미지 파일 경로이다.
                img = openImage(_root_name + "/" + filenames[extension_cnt] + _array_file_extension)

                ratio = img.width / img.height

                print(filenames[extension_cnt] + _array_file_extension)

                # PIXEL = 37.7952755906

                # height = 543/ 409 = 1.328
                img.height = round(ImageArray.PIXEL * y_axis_size)
                # width = 723/ 90 = 8.033
                img.width = round(img.height * ratio)

                # ws.add_image(img, "B" + str(i))
                if _axis_array_setting == 1:  # X축 정렬
                    ws.row_dimensions[row_line + 1].height = img.height // 1.328
                    # 409
                    ws.column_dimensions[ImageArray.EXCEL_COL[file_cnt]].width = img.width // 8.033
                    ws.add_image(img, ImageArray.EXCEL_COL[file_cnt] + str(row_line + 1))
                elif _axis_array_setting == 2:  # Y축 정렬
                    ws.row_dimensions[file_cnt + 1].height = img.height // 1.328
                    # 409
                    ws.column_dimensions[ImageArray.EXCEL_COL[row_line]].width = img.width // 8.033
                    ws.add_image(img, ImageArray.EXCEL_COL[row_line] + str(file_cnt + 1))

                # 행마다 행크기 변경

                extension_cnt += 1

        # Column 크기는 1번만 실행해도 됨(엑셀의 열을 생각해보자.)
        try:
            path = f"{_root_name}/{_file_name}.xlsx"
            wb.save(path)
            return 0

        except PermissionError:
            return -1
