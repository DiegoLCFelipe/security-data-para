from bs4 import BeautifulSoup


class LXMLHandler:

    def __init__(self, web_page_lxml_code):
        self.__web_page_lxml_code = web_page_lxml_code

    def find_urls_lines(self):
        return self.__web_page_lxml_code.find_all(self.tag_filter)

    @staticmethod
    def tag_filter(tag):
        return tag.has_attr('href') and \
               tag.has_attr('title') and \
               tag.has_attr('class') and not \
                   tag.has_attr('rel') and not \
                   tag.has_attr('a') and not \
                   tag.has_attr('property')

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

    def find_tag_link(self, tag):
        url = self.find_urls_lines()
        return str(url[tag])[self.find_url_start(str(url[tag])):self.find_url_end(str(url[tag]))]

    def find_tag_title(self, tag):
        url = self.find_urls_lines()
        return str(url[tag])[self.find_title_start(str(url[tag])):self.find_title_end(str(url[tag]))]
