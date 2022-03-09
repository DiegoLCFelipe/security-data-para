import urllib.request
import glob
import os


class FileHandler:

    def __init__(self, path, logHandler, from_web=True):
        self._path = path
        self.logHandler = logHandler

    def get_files_from_folder(self):
        return glob.glob(self._path + "/*")

    def open_file(self):
        return open(self._path)

    def save_html_code_locally(self, path_local):
        urllib.request.urlretrieve(self._path, path_local)
