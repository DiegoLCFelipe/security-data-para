from bs4 import BeautifulSoup


class AdapterHTMLToLXML:
    def __init__(self, html_code):
        self.__html_code = html_code

    def parse_xml(self):
        return BeautifulSoup(self.__html_code, 'lxml')
