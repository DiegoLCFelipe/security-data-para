import requests
from bs4 import BeautifulSoup
from Helper.LXMLHandler import LXMLHandler


class Requester:

    def __init__(self, url):
        self.__url = url
        self.__web_page = self.request()
        self.__web_page_lxml = self.parse_xml()

    def request(self):
        return requests.get(self.__url)

    def parse_xml(self):
        return BeautifulSoup(self.__web_page.text, 'lxml')

    def tag_split(self):
        lxml_file = LXMLHandler(self.__web_page_lxml)
        dict_urls ={}
        for tag in range(len(lxml_file.find_urls_lines())):
            tag_url = lxml_file.find_tag_link(tag)
            tag_title = lxml_file.find_tag_title(tag)

            dict_temp = {tag_title: tag_url}

            dict_urls.update(dict_temp)
        return dict_urls

