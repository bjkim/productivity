from tkinter import *
import pyautogui
from PIL import Image, ImageTk
from time import sleep
from win32 import win32gui
import time
import win32ui
import win32con
from dataclasses import dataclass


@dataclass
class CaptureData:
    root: str = ""
    filename: str = ""
    count: int = 0


# 변수명: 타입 = 초기값


class CaptureImage:
    def __init__(self):

        ####### dataclass #######

        self.CaptureData = CaptureData()

        ####### variable #######

        self._top = 0
        self._CapnvasDrawData = 0
        self.capture_range_flag = 0

    def __del__(self):
        print("CaptureImage 소멸")

    def capture_all(self, CaptureData):

        path = f"{CaptureData.root}/{CaptureData.filename}({CaptureData.count}).png"
        screenshot = pyautogui.screenshot(path)

        if screenshot == None:
            return -1

        return 0

    def capture_window(self, CaptureData):

        screenshot = pyautogui.screenshot()

        if screenshot == None:
            return -1

        capture_image = ImageTk.PhotoImage(screenshot)
        canvasdraw = CanvasDraw(capture_image)

        # self.caputure_initial()
        while not canvasdraw._capture_flag:
            sleep(0.2)

        result = canvasdraw.image_save(CaptureData)

        canvasdraw.destroy()

        return result

    def capture_program(self, CaptureData, hwndvalue):

        win32gui.ShowWindow(hwndvalue, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(hwndvalue)
        time.sleep(0.5)

        left, top, right, bot = win32gui.GetWindowRect(hwndvalue)
        w = right - left
        h = bot - top

        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer("RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        if result == None:
            # PrintWindow Succeeded
            im.save(f"{CaptureData.root}/{CaptureData.filename}({CaptureData.count}).png")
            # self.display_lb["text"] = "Window capture 완료."
            return 0

        return -1

    def capture_range(self, CaptureData):

        width = self._CapnvasDrawData.capture_end_x - self._CapnvasDrawData.capture_start_x
        height = self._CapnvasDrawData.capture_end_y - self._CapnvasDrawData.capture_start_y
        # print(self._CapnvasDrawData.capture_start_x, self._CapnvasDrawData.capture_start_y, width, height)

        path = f"{CaptureData.root}/{CaptureData.filename}({CaptureData.count}).png"

        pyautogui.screenshot(
            path,
            region=[self._CapnvasDrawData.capture_start_x, self._CapnvasDrawData.capture_start_y, width, height],
        )

        return 0

    def capture_range_search(self):

        screenshot = pyautogui.screenshot()

        if screenshot == None:
            return -1

        capture_image = ImageTk.PhotoImage(screenshot)
        canvasdraw = CanvasDraw(capture_image)

        while not canvasdraw._capture_flag:
            sleep(0.2)

        self._CapnvasDrawData = canvasdraw.image_location_get()

        canvasdraw.destroy()

        if self._CapnvasDrawData.capture_start_x == None:
            return -1

        self.capture_range_flag = 1
        return 0

    def capture_range_preview(self):

        screenshot = pyautogui.screenshot()
        if screenshot == None:
            return -1

        capture_image = ImageTk.PhotoImage(screenshot)
        canvasdraw = CanvasDraw(capture_image)

        canvasdraw.static_rectangle(
            self._CapnvasDrawData.capture_start_x,
            self._CapnvasDrawData.capture_start_y,
            self._CapnvasDrawData.capture_end_x,
            self._CapnvasDrawData.capture_end_y,
            outline="blue",
        )

        return 0

        # return self._CapnvasDrawData


@dataclass
class CanvasDrawData:
    capture_start_x: int = None
    capture_start_y: int = None
    capture_end_x: int = None
    capture_end_y: int = None


class CanvasDraw(Toplevel):
    def __init__(self, capture_image) -> None:
        super().__init__()

        self.capture_image = capture_image

        self._old_x = None
        self._old_y = None

        self.canvas_draw_data = CanvasDrawData()

        self._images = []
        self._root = self
        self._capture_flag = 0

        self.attributes("-fullscreen", True)

        self.canvas = Canvas(
            self,
            width=self.capture_image.width(),
            height=self.capture_image.height(),
        )

        self.canvas.create_image(0, 0, image=self.capture_image, anchor="nw")
        self.canvas.image = self.capture_image
        # 파이썬의 가비지 컬렉션의 삭제 방지. (레퍼런스 증가)
        # https://comdoc.tistory.com/entry/tkinter%EB%A5%BC-class%EC%99%80-%ED%95%A8%EA%BB%98-%EC%82%AC%EC%9A%A9%ED%95%98%EB%A9%B4-image%EA%B0%80-%EC%82%AC%EB%9D%BC%EC%A0%B8%EC%9A%94

        self.canvas.bind("<Button-1>", self.draw)  # 첫 번째 마우스 버튼 누르기
        self.canvas.bind("<B1-Motion>", self.draw)  # 누른채로 이동
        self.canvas.bind("<ButtonRelease-1>", self.draw_end)  # 버튼 떼기
        self.canvas.bind("<Button-3>", self.canvas_destroy)  # 첫 번째 마우스 버튼 누르기

        self.canvas.pack()

    def __del__(self):
        print("CanvasDraw 소멸")

    def canvas_destroy(self, new):
        self.destroy()
        self._capture_flag = 1

    def draw_initial(self):

        self._old_x = None
        self._old_y = None
        self.canvas_draw_data.capture_start_x = None
        self.canvas_draw_data.capture_start_y = None
        self.canvas_draw_data.capture_end_x = None
        self.canvas_draw_data.capture_end_y = None

        self._images = []

    def draw(self, new):

        if self._old_x == None and self._old_y == None:
            self._old_x = new.x
            self._old_y = new.y

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.capture_image, anchor="nw")

        # 4사분면에서 2사분면으로 Drag
        if self._old_x - new.x >= 0 and self._old_y - new.y >= 0:
            self.canvas_draw_data.capture_start_x = new.x
            self.canvas_draw_data.capture_start_y = new.y
            self.canvas_draw_data.capture_end_x = self._old_x
            self.canvas_draw_data.capture_end_y = self._old_y

        # 2사분면에서 4사분면으로 Drag
        elif new.x - self._old_x >= 0 and new.y - self._old_y >= 0:

            self.canvas_draw_data.capture_start_x = self._old_x
            self.canvas_draw_data.capture_start_y = self._old_y
            self.canvas_draw_data.capture_end_x = new.x
            self.canvas_draw_data.capture_end_y = new.y

        # 1사분면에서 3사분면으로 Drag
        elif self._old_x - new.x >= 0 and new.y - self._old_y >= 0:
            self.canvas_draw_data.capture_start_x = new.x
            self.canvas_draw_data.capture_start_y = self._old_y
            self.canvas_draw_data.capture_end_x = self._old_x
            self.canvas_draw_data.capture_end_y = new.y

        # 3사분면에서 1사분면으로 Drag
        elif new.x - self._old_x >= 0 and self._old_y - new.y >= 0:
            self.canvas_draw_data.capture_start_x = self._old_x
            self.canvas_draw_data.capture_start_y = new.y
            self.canvas_draw_data.capture_end_x = new.x
            self.canvas_draw_data.capture_end_y = self._old_y

        self.draw_rectangle(
            self.canvas_draw_data.capture_start_x,
            self.canvas_draw_data.capture_start_y,
            self.canvas_draw_data.capture_end_x,
            self.canvas_draw_data.capture_end_y,
            fill="black",
            outline="white",
            capture_range_lf=0.1,
        )

    def draw_end(self, new):

        self.canvas.create_rectangle(
            self.canvas_draw_data.capture_start_x,
            self.canvas_draw_data.capture_start_y,
            self.canvas_draw_data.capture_end_x,
            self.canvas_draw_data.capture_end_y,
            outline="blue",
        )

        # print(
        #     self.canvas_draw_data.capture_start_x,
        #     self.canvas_draw_data.capture_start_y,
        #     self.canvas_draw_data.capture_end_x,
        #     self.canvas_draw_data.capture_end_y,
        # )

        self._old_x, self._old_y = None, None
        self._images = []
        self._capture_flag = 1

    def draw_rectangle(self, x1, y1, x2, y2, **kwargs):
        if "capture_range_lf" in kwargs:
            capture_range_lf = int(kwargs.pop("capture_range_lf") * 255)
            fill = kwargs.pop("fill")
            fill = self._root.winfo_rgb(fill) + (capture_range_lf,)
            image = Image.new("RGBA", (x2 - x1, y2 - y1), fill)
            self._images.append(ImageTk.PhotoImage(image))

            self.canvas.create_image(x1, y1, image=self._images[-1], anchor="nw")
            self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def static_rectangle(self, x1, y1, x2, y2, **kwargs):

        # outline="blue"
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def image_get(self):

        width = self.canvas_draw_data.capture_end_x - self.canvas_draw_data.capture_start_x
        height = self.canvas_draw_data.capture_end_y - self.canvas_draw_data.capture_start_y

        # print(self.canvas_draw_data.capture_start_x, self.canvas_draw_data.capture_start_y, width, height)

        img = ImageTk.PhotoImage(
            pyautogui.screenshot(
                region=[self.canvas_draw_data.capture_start_x, self.canvas_draw_data.capture_start_y, width, height],
            )
        )
        return img

    def image_location_get(self):
        return self.canvas_draw_data

    def image_save(self, CaptureData):

        if CaptureData.root == None or CaptureData.root == "" or self.canvas_draw_data.capture_start_x == None:
            return -1

        # print(self.canvas_draw_data)

        width = self.canvas_draw_data.capture_end_x - self.canvas_draw_data.capture_start_x
        height = self.canvas_draw_data.capture_end_y - self.canvas_draw_data.capture_start_y

        # print(self.canvas_draw_data.capture_start_x, self.canvas_draw_data.capture_start_y, width, height)

        path = f"{CaptureData.root}/{CaptureData.filename}({CaptureData.count}).png"

        ImageTk.PhotoImage(
            pyautogui.screenshot(
                path,
                region=[self.canvas_draw_data.capture_start_x, self.canvas_draw_data.capture_start_y, width, height],
            )
        )
        return 0
