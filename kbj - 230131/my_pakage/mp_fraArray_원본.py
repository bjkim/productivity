import pandas as pd
import glob
import os
import natsort
import threading
import time


class Timer:
    def __init__(self):
        self.start = time.time()

    def __enter__(self):
        return self  # as로 사용할 수 있도록 self 반환

    def __exit__(self, *args):
        print("Elapsed time = ", time.time() - self.start)


class FRAArray:
    def __init__(
        self,
        root_name: str = 0,
        array_file_extension: str = "csv",
        folder_array_setting: int = 1,
        file_name: str = "result",
        array_from: int = 0,
        array_to: int = 301,
    ):
        self._root_name = root_name
        self._array_file_extension = array_file_extension
        self._folder_array_setting = folder_array_setting
        self._file_name = file_name
        self._array_from = array_from
        self._array_to = array_to
        self.array_result = []

    def work_folder_check(self) -> list:

        dir_list = []
        dir_list.append(self._root_name)

        folder_cnt = 0

        for dir_addr in dir_list:
            files = natsort.natsorted(os.listdir(dir_addr))
            # print(files)

            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == "":
                    folder_cnt += 1
                    dir_list.append(os.path.join(dir_addr, file))

        return dir_list

    def file_extension_cnt(self, _root_files):

        file_extension_dic = {}
        for file in _root_files:
            filename, ext = os.path.splitext(file)

            ext = ext[1:]

            if ext == "":
                ext = "folder"

            if ext in file_extension_dic:
                file_extension_dic[ext] += 1
            else:
                file_extension_dic[ext] = 1

        # print(file_extension_dic)

        return file_extension_dic

    # https://m.blog.naver.com/jangsam24/221389314127 참고

    def fra_file_array_multi(self, folder_root_name):

        file_root = f"{folder_root_name}/*.{self._array_file_extension}"
        all_file_list = natsort.natsorted(glob.glob(file_root))

        all_data = []  # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다

        file_count = 0

        for file in all_file_list:

            # nrows 참고자료
            # https://seong6496.tistory.com/231?category=903876

            if self._array_file_extension == "txt":
                df = pd.read_table(file, skiprows=self._array_from, nrows=self._array_to)
            elif self._array_file_extension == "csv":
                # df = pd.read_csv(
                #     file,
                #     skiprows=9,
                #     nrows=14,
                #     names=["Idx", "col1", "col2"],
                #     # header=0,
                #     # usecols=["col1", "col2"],
                #     on_bad_lines="skip",
                # )  # sinewave/ Ringing result data
                df = pd.read_csv(file, index_col=0, skiprows=self._array_from, nrows=self._array_to)
            elif self._array_file_extension == "xlsx":
                df = pd.read_excel(file, skiprows=self._array_from, nrows=self._array_to)
            elif self._array_file_extension == "xls":
                df = pd.read_excel(file, skiprows=self._array_from, nrows=self._array_to)

            file_count += 1

            df.rename(
                columns={df.columns[0]: ("Gain_" + os.path.basename(os.path.normpath(file)))},
                inplace=True,
            )

            all_data.append(df)

        if file_count == 0:
            self.array_result.append(-2)
            return -2

        dataCombine = pd.concat(all_data, axis=1, ignore_index=False)

        # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
        # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정

        try:
            path = f"{folder_root_name}/{self._file_name}.xlsx"
            dataCombine.to_excel(path, index=True)
            self.array_result.append(0)
            return 0

        except PermissionError:
            self.array_result.append(-1)
            return -1

    def fra_file_array_single(self):

        file_root = f"{self._root_name}/*.{self._array_file_extension}"
        all_file_list = natsort.natsorted(glob.glob(file_root))

        all_data = []  # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다

        file_count = 0

        for file in all_file_list:

            # nrows 참고자료
            # https://seong6496.tistory.com/231?category=903876

            if self._array_file_extension == "txt":
                df = pd.read_table(file, skiprows=self._array_from, nrows=self._array_to)
            elif self._array_file_extension == "csv":
                # df = pd.read_csv(
                #     file,
                #     skiprows=9,
                #     nrows=14,
                #     names=["Idx", "col1", "col2"],
                #     # header=0,
                #     # usecols=["col1", "col2"],
                #     on_bad_lines="skip",
                # )  # sinewave/ Ringing result data
                df = pd.read_csv(file, index_col=0, skiprows=self._array_from, nrows=self._array_to)
            elif self._array_file_extension == "xlsx":
                df = pd.read_excel(file, skiprows=self._array_from, nrows=self._array_to)
            elif self._array_file_extension == "xls":
                df = pd.read_excel(file, skiprows=self._array_from, nrows=self._array_to)

            file_count += 1

            df.rename(
                columns={df.columns[0]: ("Gain_" + os.path.basename(os.path.normpath(file)))},
                inplace=True,
            )

            all_data.append(df)

        if file_count == 0:
            self.array_result.append(-2)
            return -2

        dataCombine = pd.concat(all_data, axis=1, ignore_index=False)

        # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
        # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정

        try:
            path = f"{self._root_name}/{self._file_name}.xlsx"
            dataCombine.to_excel(path, index=True)
            self.array_result.append(0)
            return 0

        except PermissionError:
            self.array_result.append(-1)
            return -1

    def fra_array_start(self):

        if self._folder_array_setting == 1:

            with Timer():
                result = self.fra_file_array_single()

            return result

        elif self._folder_array_setting == 2:
            folder_list = self.work_folder_check()

            with Timer():

                thread_list = [threading.Thread(target=self.fra_file_array_multi, args=(folder,)) for folder in folder_list]
                list(map(lambda t: t.start(), thread_list))
                list(map(lambda t: t.join(), thread_list))
                # print(self.array_result)

                if -1 in self.array_result:
                    return -1
                elif -2 in self.array_result:
                    return -2
                else:
                    return 0

        """
        elif self._folder_array_setting == 2:
            folder_list = self.work_folder_check()
            with Timer():
                for folder_root_name in folder_list:
                    result = self.fra_file_array(folder_root_name)
                    if result == -1:
                        # print("엑셀 파일을 종료해주세요")
                        return result
        """


# 실행파일 만들기
# https://hongku.tistory.com/338
# https://velog.io/@pjs102793/Pyinstaller%EB%A1%9C-%EB%A7%8C%EB%93%A0-%EC%8B%A4%ED%96%89-%ED%8C%8C%EC%9D%BC-UPX%EB%A1%9C-%EC%9A%A9%EB%9F%89-%EC%A4%84%EC%9D%B4%EA%B8%B0
# https://www.baragi.net/bbs/board.php?bo_table=dev&wr_id=8871
# pyinstaller -w -F --noconsole FRA.py --upx-dir D:\software\python\upx-3.96-win64\upx-3.96-win64

"""
class FRAArray:
    def __init__(self) -> None:
        pass
    def work_folder_check(self, root_name: str = "0") -> list:
        dir_list = []
        dir_list.append(root_name)
        folder_cnt = 0
        for dir_addr in dir_list:
            files = natsort.natsorted(os.listdir(dir_addr))
            # print(files)
            for file in files:
                filename, ext = os.path.splitext(file)
                if ext == "":
                    folder_cnt += 1
                    dir_list.append(os.path.join(dir_addr, file))
        return dir_list
    def file_extension_cnt(self, _root_files):
        file_extension_dic = {}
        for file in _root_files:
            filename, ext = os.path.splitext(file)
            ext = ext[1:]
            if ext == "":
                ext = "folder"
            if ext in file_extension_dic:
                file_extension_dic[ext] += 1
            else:
                file_extension_dic[ext] = 1
        # print(file_extension_dic)
        return file_extension_dic
    # https://m.blog.naver.com/jangsam24/221389314127 참고
    def fra_file_array(self, root_name: str = "0", file_name: str = "0", array_file_extension: str = "0", array_from: int = 0, array_to: int = 0):
        file_root = f"{root_name}/*.{array_file_extension}"
        all_file_list = natsort.natsorted(glob.glob(file_root))
        all_data = []  # 읽어 들인 csv파일 내용을 저장할 빈 리스트를 하나 만든다
        file_count = 0
        for file in all_file_list:
            # nrows 참고자료
            # https://seong6496.tistory.com/231?category=903876
            if array_file_extension == "txt":
                df = pd.read_table(file, skiprows=array_from, nrows=array_to)
            elif array_file_extension == "csv":
                # df = pd.read_csv(
                #     file,
                #     skiprows=9,
                #     nrows=14,
                #     names=["Idx", "col1", "col2"],
                #     # header=0,
                #     # usecols=["col1", "col2"],
                #     on_bad_lines="skip",
                # )  # sinewave/ Ringing result data
                df = pd.read_csv(file, index_col=0, skiprows=array_from, nrows=array_to)
            elif array_file_extension == "xlsx":
                df = pd.read_excel(file, skiprows=array_from, nrows=array_to)
            elif array_file_extension == "xls":
                df = pd.read_excel(file, skiprows=array_from, nrows=array_to)
            file_count += 1
            df.rename(
                columns={df.columns[0]: ("Gain_" + os.path.basename(os.path.normpath(file)))},
                inplace=True,
            )
            all_data.append(df)
        if file_count == 0:
            return
        dataCombine = pd.concat(all_data, axis=1, ignore_index=False)
        # axis=0은 수직으로 병합함. axis=1은 수평. ignore_index=True는 인데스 값이 기존 순서를 무시하고 순서대로 정렬되도록 한다.
        # to_csv함수로 저장한다. 인데스를 빼려면 False로 설정
        try:
            path = f"{root_name}/{file_name}.xlsx"
            dataCombine.to_excel(path, index=True)
            return 0
        except PermissionError:
            return -1
    def fra_array_start(
        self,
        _root_name: str = 0,
        _array_file_extension: str = "csv",
        _folder_array_setting: int = 1,
        _file_name: str = "result",
        _array_from: int = 0,
        _array_to: int = 301,
    ):
        if _folder_array_setting == 1:
            result = self.fra_file_array(_root_name, _file_name, _array_file_extension, _array_from, _array_to)
            if result == -1:
                # print("엑셀 파일을 종료해주세요")
                return result
        elif _folder_array_setting == 2:
            folder_list = self.work_folder_check(_root_name)
            for folder_root_name in folder_list:
                result = self.fra_file_array(folder_root_name, _file_name, _array_file_extension, _array_from, _array_to)
                if result == -1:
                    # print("엑셀 파일을 종료해주세요")
                    return result
        return 0
"""
