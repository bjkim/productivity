import my_pakage.mp_load as mp
import my_pakage.mp_imageArrary as ia
import my_pakage.mp_captureimage as mc
import my_pakage.mp_fraArray as mf
import tkinter.ttk as tt
from tkinter import *

import keyboard
from win32 import win32gui


class MainFrame(Tk):
    def __init__(self):
        super().__init__()

        self.notebook = tt.Notebook(self, width=800, height=500)
        self.notebook.pack()

        self.tab1 = tt.Frame(self)
        self.notebook.add(self.tab1, text="ImageArray")
        self.tab2 = tt.Frame(self)
        self.notebook.add(self.tab2, text="CaptureImage")
        self.tab3 = tt.Frame(self)
        self.notebook.add(self.tab3, text="FRAArray")

        self.image_array_frame = Frame(self.tab1)
        self.image_array_class = ImageArrayFrame(self.image_array_frame)
        self.image_array_class.pack()

        self.capture_image_frame = Frame(self.tab2)
        self.capture_image_class = CaptureImageFrame(self.capture_image_frame)
        self.capture_image_class.pack()

        self.fra_array_frame = Frame(self.tab3)
        self.fra_array_class = FRAArrayFrame(self.fra_array_frame)
        self.fra_array_class.pack()

        self.image_array_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.capture_image_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.fra_array_frame.pack(side=TOP, fill=BOTH, expand=True)


class ImageArrayFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        ####### class #######

        self.load = mp.Load()
        self.IMAGEARRAY = ia.ImageArray()

        ####### result_screen_lf #######
        self.result_screen_lf = LabelFrame(self, text="결과 화면", padx=10, pady=10)
        self.result_screen_lf.grid(row=0, column=0, columnspan=10)

        self.display_lb = Label(self.result_screen_lf, text="Wait...")
        self.display_lb.pack(side="top")

        ####### loadstart_button_lf #######
        self.loadstart_bttn_lf = LabelFrame(self, text="Load/ Start", padx=10, pady=10)

        self.loadstart_bttn_lf.grid(row=1, column=0, columnspan=10)

        self.loadstart_label = Label(
            self.loadstart_bttn_lf,
            text="Please load the location of the file to be sorted.",
        )
        self.loadstart_label.pack(side="top")

        self.load_bttn = Button(self.loadstart_bttn_lf, text="Load", command=self.load_button)
        self.load_bttn.pack(side="top")

        self.result_button = Button(
            self.loadstart_bttn_lf,
            text="Start",
            command=self.start_button,
        )
        self.result_button.pack(side="top")

        self.file_name_label = Label(self.loadstart_bttn_lf, text="저장 파일 이름 : ")
        self.file_name_label.pack(side="top")

        self.file_name_entry = Entry(
            self.loadstart_bttn_lf,
            fg="black",
            justify=CENTER,
            font=("Arial", 10),
        )
        self.file_name_entry.pack(side="top")
        self.file_name_entry.insert(index=END, string="result")

        ####### array_file_setting_lf #######

        self.array_file_setting_lf = LabelFrame(self, text="정렬 파일 설정", padx=10, pady=10)
        self.array_file_setting_lf.grid(row=2, column=0, columnspan=10)
        """
        self.array_file_extension_entry = Entry(
            self.array_file_setting_lf, fg="black", bg="white", justify=CENTER, font=("Arial", 10)
        )
        self.arrayfile_extension_entry.pack(side="bottom")
        self.arrayfile_extension_entry.insert(index=END, string="JPG")
        """
        file_extension = ["png", "gif", "jpg", "tif", "heic"]

        self.array_file_extension_cb = tt.Combobox(self.array_file_setting_lf, height=15, values=file_extension)
        self.array_file_extension_cb.pack()
        self.array_file_extension_cb.set("jpg")

        ####### array_file_setting_lf #######

        self.array_file_setting_lf = LabelFrame(self, text="정렬 축 설정", padx=10, pady=10)
        self.array_file_setting_lf.grid(row=3, column=0, columnspan=10)

        self.axis_array_var = IntVar()

        self.x_axis_array_rb = Radiobutton(
            self.array_file_setting_lf,
            text="X-axis Array",
            value=1,
            variable=self.axis_array_var,
        )
        self.x_axis_array_rb.pack(side="left")
        self.x_axis_array_rb.select()

        self.y_axis_array_bt = Radiobutton(
            self.array_file_setting_lf,
            text="Y-axis Array",
            value=2,
            variable=self.axis_array_var,
        )
        self.y_axis_array_bt.pack(side="left")

        self.array_num_entry = Entry(
            self.array_file_setting_lf,
            fg="black",
            justify=CENTER,
            font=("Arial", 10),
        )
        self.array_num_entry.pack(side="left")
        self.array_num_entry.insert(index=END, string="10")
        self.array_num_label = Label(self.array_file_setting_lf, text="정렬 갯수")
        self.array_num_label.pack(side="left")

        ####### size_control_lf #######
        self.size_control_lf = LabelFrame(self, text="Image Size", padx=10, pady=10)
        self.size_control_lf.grid(row=4, column=0, columnspan=10)

        # self.var = IntVar()
        self.image_size_scale = Scale(
            master=self.size_control_lf,
            # variable=self.var,
            command=self.scale_control,
            orient="horizontal",
            showvalue=True,
            tickinterval=10,
            from_=10,
            to=100,
            length=300,
        )

        self.image_size_scale.set(100)
        self.image_size_scale.pack(side="top")

        self.image_size_label = Label(self.size_control_lf, text="값 : 0")
        self.image_size_label.pack(side="top")

    def load_button(self):

        root_name = self.load.file_load()
        self.loadstart_label["text"] = root_name
        self.display_lb["text"] = "Wait..."

    def start_button(self):
        if self.load.get_root_name() == None or self.load.get_root_name() == "":
            self.display_lb["text"] = "Please Load Click"
            return

        result = self.IMAGEARRAY.image_array(
            _root_name=self.load.get_root_name(),
            _root_files=self.load.get_root_files(),
            _line_num=int(self.array_num_entry.get()),
            _y_axis_size_scale=self.image_size_scale.get(),
            _array_file_extension=self.array_file_extension_cb.get(),
            _axis_array_setting=self.axis_array_var.get(),
            _file_name=self.file_name_entry.get(),
        )
        if result == -1:
            self.display_lb["text"] = "엑셀 파일을 종료해주세요"
        elif result == 0:
            self.display_lb["text"] = "Finish"

    def scale_control(self, test):
        y_axis_size = round(float(test) * 0.14 + 0.38, 2)
        self.image_size_label["text"] = "이미지 세로 크기 : " + str(y_axis_size) + "cm"


# 변수명: 타입 = 초기값


class CaptureImageFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        ####### dataclass #######

        self.load = mp.Load()
        self.capture_data = mc.CaptureData()
        self.capture_image = mc.CaptureImage()

        ####### variable #######

        self._top = 0

        keyboard.unhook_all()
        keyboard.add_hotkey("ctrl+1", lambda: self.capture_all_button())
        keyboard.add_hotkey("ctrl+2", lambda: self.capture_window_button())
        keyboard.add_hotkey("ctrl+3", lambda: self.capture_range_button())

        ####### result_screen_lf #######
        self.result_screen_lf = LabelFrame(self, text="결과 화면", padx=10, pady=10)
        self.result_screen_lf.grid(row=0, column=0, columnspan=10)

        self.display_lb = Label(self.result_screen_lf, text="Wait...")
        self.display_lb.pack(side="top")

        ####### image_save_setting_lf #######
        self.image_save_setting_lf = LabelFrame(self, text="Image Save Setting", padx=10, pady=10)
        self.image_save_setting_lf.grid(row=1, column=0, columnspan=10)

        self.loadstart_label = Label(
            self.image_save_setting_lf,
            text="Please load the location of the file to be sorted.",
        )
        self.loadstart_label.pack(side="top")

        self.load_bttn = Button(self.image_save_setting_lf, text="저장 위치", command=self.load_button)
        self.load_bttn.pack(side="top")

        self.file_name_label = Label(self.image_save_setting_lf, text="저장 파일 이름 : ")
        self.file_name_label.pack(side="left")

        self.file_name_entry = Entry(
            self.image_save_setting_lf,
            fg="black",
            justify=CENTER,
            font=("Arial", 10),
        )
        self.file_name_entry.pack(side="left")
        self.file_name_entry.insert(index=END, string="graph")

        self.file_count_label = Label(self.image_save_setting_lf, text="파일 번호 : ")
        self.file_count_label.pack(side="left")

        self.file_count_var = IntVar()

        validate_command = (self.image_save_setting_lf.register(self.file_count_spinbox_value_check), "%P")
        invalid_command = (self.image_save_setting_lf.register(self.file_count_spinbox_value_error), "%P")
        self.file_count_spinbox = Spinbox(
            self.image_save_setting_lf,
            textvariable=self.file_count_var,
            from_=0,
            to=10000,
            validate="all",
            validatecommand=validate_command,
            invalidcommand=invalid_command,
        )
        self.file_count_spinbox.pack(side="left")

        self.file_count_reset_bttn = Button(
            self.image_save_setting_lf,
            text="Reset",
            command=self.file_count_reset_button,
        )
        self.file_count_reset_bttn.pack(side="left")
        """
        # self.file_count_spinbox.invoke("buttonup")
        # # self.file_count_spinbox.invoke("buttondown")
        # print(self.file_count_var.get())

        # self.file_count_var.set(7)
        # self.file_count_var.get()
        """

        ####### capture_all_button_lf #######
        self.capture_all_bttn_lf = LabelFrame(self, text="Capture All", padx=10, pady=10)
        self.capture_all_bttn_lf.grid(row=2, column=0, columnspan=10)

        self.capture_all_bttn = Button(
            self.capture_all_bttn_lf,
            text="ctrl+1",
            command=self.capture_all_button,
        )
        self.capture_all_bttn.pack(side="top")

        ####### capture_program_lf #######
        self.capture_program_lf = LabelFrame(self, text="Capture Program", padx=10, pady=10)
        self.capture_program_lf.grid(row=3, column=0, columnspan=10)

        self.hwnd_dict = self.get_program_hwnd_list()
        # self.window_list_cb = tt.Combobox(self.capture_program_lf, height=15, values=list(hwnd_dict))
        self.window_list_cb = tt.Combobox(self.capture_program_lf, height=15, values=list(self.hwnd_dict.keys()))
        self.window_list_cb.grid(row=0, column=0)
        self.window_list_cb.set("선택")

        self.program_list_reset_bttn = Button(
            self.capture_program_lf,
            text="Reset",
            command=self.program_list_reset_button,
        )
        self.program_list_reset_bttn.grid(row=0, column=1)

        self.capture_program_bttn = Button(self.capture_program_lf, text="Capture", command=self.capture_program_button)
        self.capture_program_bttn.grid(row=1, column=0, columnspan=10)

        ####### capture_range_lf #######
        self.capture_range_lf = LabelFrame(self, text="Capture Range", padx=10, pady=10)
        self.capture_range_lf.grid(row=4, column=0, columnspan=10)

        self.capture_range_reset_bttn = Button(
            self.capture_range_lf,
            text="Reset",
            command=self.capture_range_reset_button,
        )
        self.capture_range_reset_bttn.grid(row=0, column=1, padx=3)
        self.capture_range_reset_bttn["state"] = "disabled"

        self.capture_range_preview_bttn = Button(
            self.capture_range_lf,
            text="Preview",
            command=self.capture_range_preview_button,
        )
        self.capture_range_preview_bttn.grid(row=0, column=2, padx=3)
        self.capture_range_preview_bttn["state"] = "disabled"

        self.capture_range_bttn = Button(
            self.capture_range_lf,
            text="ctrl+3",
            # command=self.capture_range_button,
        )
        self.capture_range_bttn.grid(row=0, column=3, padx=3)

    def load_button(self):

        # root_name = self.load.file_load()
        self.capture_data.root = self.load.file_load()
        self.loadstart_label["text"] = self.capture_data.root
        self.display_lb["text"] = "Wait..."

    def load_check(self):

        self.file_count_spinbox.invoke("buttonup")

        # self.capture_data.root = self.load.get_root_name()
        self.capture_data.filename = self.file_name_entry.get()
        self.capture_data.count = self.file_count_var.get()

        if self.capture_data.root == None or self.capture_data.root == "":
            self.file_count_spinbox.invoke("buttondown")
            self.display_lb["text"] = "Please Load Click"
            return -1

        return 0

    def capture_range_reset_button(self):

        self.capture_image.capture_range_flag = 0
        self.capture_range_reset_bttn["state"] = "disabled"
        self.capture_range_preview_bttn["state"] = "disabled"

    def capture_range_preview_button(self):

        if self.capture_image.capture_range_flag == 0:
            return

        result = self.capture_image.capture_range_preview()

        if result == -1:
            self.display_lb["text"] = "Capture Range Preview 안됨"

        elif result == 0:
            self.display_lb["text"] = "Finish"

    def capture_range_button(self):

        if self.capture_image.capture_range_flag == 0:
            result = self.capture_image.capture_range_search()
            if result == 0:
                self.capture_range_reset_bttn["state"] = "normal"
                self.capture_range_preview_bttn["state"] = "normal"
            elif result == -1:
                self.display_lb["text"] = "Capture Range 안됨"
            return

        load_check_result = self.load_check()
        if load_check_result == -1:
            return

        result = self.capture_image.capture_range(self.capture_data)

        if result == -1:
            self.file_count_spinbox.invoke("buttondown")
            self.display_lb["text"] = "Capture Range 안됨"
        elif result == 0:
            self.display_lb["text"] = "Finish"

    def file_count_reset_button(self):
        self.file_count_var.set("0")

    def file_count_spinbox_value_check(self, value):
        self.display_lb["text"] = "Wait..."

        valid = False
        if value.isdigit():
            if int(value) <= 10000 and int(value) >= 0:
                valid = True
        elif value == "":
            valid = True
        return valid

    def file_count_spinbox_value_error(self, value):
        self.display_lb["text"] = f"숫자 이외의 문자 ({value}) 을/를 입력하셨습니다."

    def capture_program_button(self):

        load_check_result = self.load_check()
        if load_check_result == -1:
            return

        hwndkey = self.window_list_cb.get()

        if hwndkey == "선택":
            self.file_count_spinbox.invoke("buttondown")
            self.display_lb["text"] = "Capture Program 항목을 선택해 주세요."
            return

        hwndvalue = self.hwnd_dict[hwndkey]

        result = self.capture_image.capture_program(self.capture_data, hwndvalue)

        if result == -1:
            self.file_count_spinbox.invoke("buttondown")
            self.display_lb["text"] = "윈도우 프로그램 안됨"
        elif result == 0:
            self.display_lb["text"] = "Finish"

    def program_list_reset_button(self):
        self.hwnd_dict = self.get_program_hwnd_list()
        self.window_list_cb["values"] = list(self.hwnd_dict.keys())
        self.window_list_cb.set("선택")

    def get_program_hwnd_list(self):
        def callback(_hwnd, _result: list):
            title = win32gui.GetWindowText(_hwnd)
            if win32gui.IsWindowEnabled(_hwnd) and win32gui.IsWindowVisible(_hwnd) and title is not None and len(title) > 0:
                _result.append(_hwnd)
            return True

        hwnd_list = []
        win32gui.EnumWindows(callback, hwnd_list)
        hwnd_dict = {hwnd: win32gui.GetWindowText(hwnd) for hwnd in hwnd_list}
        hwnd_dict = {v: k for k, v in hwnd_dict.items()}
        return hwnd_dict

    def capture_all_button(self):

        load_check_result = self.load_check()
        if load_check_result == -1:
            return

        result = self.capture_image.capture_all(self.capture_data)

        if result == -1:
            self.file_count_spinbox.invoke("buttondown")
            self.display_lb["text"] = "Capture All 안됨"

        elif result == 0:
            self.display_lb["text"] = "Finish"

        """
        self._top = Toplevel(self)
        self._top.attributes("-fullscreen", True)

        path = f"{CaptureData.root}/{CaptureData.filename}({CaptureData.count}).png"
        screenshot = pyautogui.screenshot(path)

        if screenshot == None:
            return -1

        capture_image = ImageTk.PhotoImage(screenshot)

        canvas = Canvas(
            self._top,
            width=capture_image.width(),
            height=capture_image.height(),
        )

        canvas.create_image(0, 0, image=capture_image, anchor="nw")
        canvas.image = capture_image
        # 파이썬의 가비지 컬렉션의 삭제 방지. (레퍼런스 증가)
        # https://comdoc.tistory.com/entry/tkinter%EB%A5%BC-class%EC%99%80-%ED%95%A8%EA%BB%98-%EC%82%AC%EC%9A%A9%ED%95%98%EB%A9%B4-image%EA%B0%80-%EC%82%AC%EB%9D%BC%EC%A0%B8%EC%9A%94
        canvas.pack()

        return 0

        """

    def capture_window_button(self):

        load_check_result = self.load_check()
        if load_check_result == -1:
            return

        result = self.capture_image.capture_window(self.capture_data)

        if result == -1:
            self.file_count_spinbox.invoke("buttondown")
            self.display_lb["text"] = "Capture Window 안됨"
        elif result == 0:
            self.display_lb["text"] = "Finish"


class FRAArrayFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        ####### class #######
        self.load = mp.Load()
        # self.fra_array = mf.FRAArray()

        ####### result_screen_lf #######
        self.result_screen_lf = LabelFrame(self, text="결과 화면", padx=10, pady=10)
        self.result_screen_lf.grid(row=0, column=0, columnspan=10)

        self.display_lb = Label(self.result_screen_lf, text="Wait...")
        self.display_lb.pack(side="top")

        ####### loadstart_button_lf #######
        self.loadstart_bttn_lf = LabelFrame(self, text="Load/ Start", padx=10, pady=10)

        self.loadstart_bttn_lf.grid(row=1, column=0, columnspan=10)

        self.loadstart_label = Label(
            self.loadstart_bttn_lf,
            text="Please load the location of the file to be sorted.",
        )
        self.loadstart_label.pack(side="top")

        self.load_bttn = Button(self.loadstart_bttn_lf, text="Load", command=self.load_button)
        self.load_bttn.pack(side="top")

        self.result_button = Button(
            self.loadstart_bttn_lf,
            text="Start",
            command=self.start_button,
        )
        self.result_button.pack(side="top")

        self.file_name_label = Label(self.loadstart_bttn_lf, text="저장 파일 이름 : ")
        self.file_name_label.pack(side="top")

        self.file_name_entry = Entry(
            self.loadstart_bttn_lf,
            fg="black",
            justify=CENTER,
            font=("Arial", 10),
        )
        self.file_name_entry.pack(side="top")
        self.file_name_entry.insert(index=END, string="result")

        ####### array_file_setting_lf #######

        self.array_file_setting_lf = LabelFrame(self, text="정렬 파일 설정", padx=10, pady=10)
        self.array_file_setting_lf.grid(row=2, column=0, columnspan=10)
        """
        self.array_file_extension_entry = Entry(
            self.array_file_setting_lf, fg="black", bg="white", justify=CENTER, font=("Arial", 10)
        )
        self.arrayfile_extension_entry.pack(side="bottom")
        self.arrayfile_extension_entry.insert(index=END, string="JPG")
        """
        file_extension = ["txt", "csv", "xlsx", "xls"]

        self.array_file_extension_cb = tt.Combobox(self.array_file_setting_lf, height=15, values=file_extension)
        self.array_file_extension_cb.pack()
        self.array_file_extension_cb.set("csv")

        ####### array_file_setting_lf #######

        self.array_file_setting_lf = LabelFrame(self, text="정렬 축 설정", padx=10, pady=10)
        self.array_file_setting_lf.grid(row=3, column=0, columnspan=10)

        self.folder_array_var = IntVar()

        self.current_folder_array_rb = Radiobutton(
            self.array_file_setting_lf,
            text="현재 폴더 정렬",
            value=1,
            variable=self.folder_array_var,
        )
        self.current_folder_array_rb.pack(side="left")
        self.current_folder_array_rb.select()

        self.all_folder_array_rb = Radiobutton(
            self.array_file_setting_lf,
            text="전체 폴더 정렬",
            value=2,
            variable=self.folder_array_var,
        )
        self.all_folder_array_rb.pack(side="left")

        ####### array_file_edit_lf #######

        self.array_file_edit_lf = LabelFrame(self, text="정렬 파일 편집", padx=10, pady=10)
        self.array_file_edit_lf.grid(row=4, column=0, columnspan=10)

        self.file_format_frame = Frame(self.array_file_edit_lf)
        self.file_format_frame.pack()

        file_format = ["AKM FRA", "AKM Sinewave", "AKM Ringing", "동운 FRA", "동운 Hallscan"]

        self.file_format_cb = tt.Combobox(self.file_format_frame, height=15, values=file_format)
        self.file_format_cb.pack(side="left")
        self.file_format_cb.set("AKM FRA")

        # self.file_format_reset_bttn = Button(
        #     self.file_format_frame,
        #     text="Reset",
        #     command=self.file_format_reset_button,
        # )
        # self.file_format_reset_bttn.pack(side="left")

        self.file_format_set_bttn = Button(
            self.file_format_frame,
            text="set",
            command=self.file_format_set_button,
        )
        self.file_format_set_bttn.pack(side="left")

        self.file_array_frame = Frame(self.array_file_edit_lf)
        self.file_array_frame.pack()

        self.array_from_label = Label(self.file_array_frame, text="From")
        self.array_from_label.pack(side="left")

        self.array_from_entry = Entry(
            self.file_array_frame,
            fg="black",
            justify=CENTER,
            font=("Arial", 10),
        )
        self.array_from_entry.pack(side="left")
        self.array_from_entry.insert(index=END, string="0")

        self.array_to_label = Label(self.file_array_frame, text="to")
        self.array_to_label.pack(side="left")

        self.array_to_entry = Entry(
            self.file_array_frame,
            fg="black",
            justify=CENTER,
            font=("Arial", 10),
        )
        self.array_to_entry.pack(side="left")
        self.array_to_entry.insert(index=END, string="301")

    def file_format_reset_button(self):
        self.file_format_cb.set("선택")

    def file_format_set_button(self):
        file_format = self.file_format_cb.get()

        self.array_from_entry.delete(0, "end")
        self.array_to_entry.delete(0, "end")

        if file_format == "AKM FRA":
            self.array_from_entry.insert(index=END, string="0")
            self.array_to_entry.insert(index=END, string="301")
        elif file_format == "AKM Sinewave":
            self.array_from_entry.insert(index=END, string="19")
            self.array_to_entry.insert(index=END, string="419")
        elif file_format == "AKM Ringing":
            self.array_from_entry.insert(index=END, string="20")
            self.array_to_entry.insert(index=END, string="172")
        elif file_format == "동운 FRA":
            self.array_from_entry.insert(index=END, string="0")
            self.array_to_entry.insert(index=END, string="301")
        elif file_format == "동운 Hallscan":
            self.array_from_entry.insert(index=END, string="0")
            self.array_to_entry.insert(index=END, string="31")

    def load_button(self):

        root_name = self.load.file_load()
        self.loadstart_label["text"] = root_name
        self.display_lb["text"] = "Wait..."

    def start_button(self):

        if self.load.get_root_name() == None or self.load.get_root_name() == "":
            self.display_lb["text"] = "Please Load Click"
            return

        fra_array = mf.FRAArray(
            root_name=self.load.get_root_name(),
            array_file_extension=self.array_file_extension_cb.get(),
            folder_array_setting=self.folder_array_var.get(),
            file_name=self.file_name_entry.get(),
            array_from=int(self.array_from_entry.get()),
            array_to=int(self.array_to_entry.get()),
        )

        fra_array_result = fra_array.fra_array_start()

        if fra_array_result == -1:
            self.display_lb["text"] = "엑셀 파일을 종료해주세요"
        elif fra_array_result == -2:
            self.display_lb["text"] = "파일이 없습니다."
        elif fra_array_result == 0:
            self.display_lb["text"] = "Finish"


"""
    def start_button(self):

        if self.load.get_root_name() == None or self.load.get_root_name() == "":
            self.display_lb["text"] = "Please Load Click"
            return

        fra_array = mf.FRAArray(
            _root_name=self.load.get_root_name(),
            _array_file_extension=self.array_file_extension_cb.get(),
            _folder_array_setting=self.folder_array_var.get(),
            _file_name=self.file_name_entry.get(),
            _array_from=int(self.array_from_entry.get()),
            _array_to=int(self.array_to_entry.get()),
        )

        fra_array_result = fra_array.fra_array_start()

        # fra_array_result = self.fra_array.fra_array_start(
        #     _root_name=self.load.get_root_name(),
        #     _array_file_extension=self.array_file_extension_cb.get(),
        #     _folder_array_setting=self.folder_array_var.get(),
        #     _file_name=self.file_name_entry.get(),
        #     _array_from=int(self.array_from_entry.get()),
        #     _array_to=int(self.array_to_entry.get()),
        # )

        if fra_array_result == -1:
            self.display_lb["text"] = "엑셀 파일을 종료해주세요"
        elif fra_array_result == 0:
            self.display_lb["text"] = "Finish"

"""
main_frame = MainFrame()

main_frame.title("KBJ")

main_frame.mainloop()


# https://coding-kindergarten.tistory.com/173
# pyinstaller -w -F --noconsole 221125_mainFrame.py --upx-dir H:\kbj\lecture\_4v14-220725-133654\강의노트_문제풀이_챕터4이후\upx-4.0.1-win64\upx-4.0.1-win64
