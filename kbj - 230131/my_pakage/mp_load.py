from tkinter import filedialog
import natsort
import os


class Load:
    def __init__(self):

        self._root_name = None

    def file_load(self):

        self._root_name = filedialog.askdirectory()
        return self._root_name

    def get_root_name(self):

        return self._root_name

    def get_root_files(self):
        return natsort.natsorted(os.listdir(self._root_name))
