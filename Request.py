import requests
from bs4 import BeautifulSoup


class Requester:

    def __init__(self, url):
        self.__url = url
        self.__web_page = self.request()
        self.__web_page_lxml = self.parse_xml()
        self.__urls_tags = self.find_urls_lines()

    def request(self):
        return requests.get(self.__url)

    def parse_xml(self):
        return BeautifulSoup(self.__web_page.text, 'lxml')

    @staticmethod
    def tag_filter(tag):
        return tag.has_attr('href') and \
               tag.has_attr('title') and \
               tag.has_attr('class') and not \
                   tag.has_attr('rel') and not \
                   tag.has_attr('a') and not \
                   tag.has_attr('property')

    def find_urls_lines(self):
        return self.__web_page_lxml.find_all(self.tag_filter)


    @staticmethod
    def find_url_start(url_line):
        return url_line.find('href') + 6

    @staticmethod
    def find_url_end(url_line):
        return url_line.find('title') - 2

    @staticmethod
    def find_title_start(url_line):
        return url_line.find('title') + 7

    @staticmethod
    def find_title_end(url_line):
        return url_line.find('>') - 6

    def tag_split(self):
        dict = {}
        url = self.find_urls_lines()
        for line in range(len(url)):
            link = str(url[line])[self.find_url_start(str(url[line])):self.find_url_end(str(url[line]))]
            title = str(url[line])[self.find_title_start(str(url[line])):self.find_title_end(str(url[line]))]

            dict_temp = {title: link}

            dict.update(dict_temp)
        return dict
