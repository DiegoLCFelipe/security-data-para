import urllib.request


class FileHandler:

    def __init__(self, path, logHandler, from_web=True):
        self._path = path
        self.logHandler = logHandler

    def open_file(self):
        return open(self._path)

    def save_html_code_locally(self, path_local):
        self.logHandler.log_info_timestamp(f'Saving locally: {self._path}')
        urllib.request.urlretrieve(self._path, path_local)
