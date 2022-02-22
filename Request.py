import requests


class Requester:

    def __init__(self, url, logHandler):
        self.logHandler = logHandler
        self.__url = url
        self.__web_page = self._request()

    def _request(self):
        return requests.get(self.__url)

    def _successful_request(self):
        if self.__web_page.status_code == 200:
            self.logHandler.log_info_timestamp(f'Successful request on: {str(self.__url)}')
            return True
        raise RuntimeError(f'Request Failure on: {str(self.__url)}')

    def page_html_code(self):
        if self._successful_request():
            return self.__web_page.text

