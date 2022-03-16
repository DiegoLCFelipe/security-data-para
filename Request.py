from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from Helper.LogHandler import LogHandler

logHandler = LogHandler()


class Requester:

    def __init__(self, url, logHandler):
        self.logHandler = logHandler
        self.__url = url

    def get_html(self):
        try:
            return urlopen(self.__url)
        except HTTPError as error:
            logHandler.log_error_timestamp(error)
        except URLError:
            logHandler.log_error_timestamp('The server could not be found !')
        logHandler.log_error_timestamp('Successful request')
