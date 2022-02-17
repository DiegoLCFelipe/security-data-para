import requests
from bs4 import BeautifulSoup


class Requester:

    def __init__(self, url):

        self.__url = url

    def request(self):

        page = requests.get(self.__url)
        return page

    def parse_xml(self):

        page = self.request()
        soup = BeautifulSoup(page.text, 'lxml')
        return soup

    @staticmethod
    def tag_filter(tag):

        return tag.has_attr('href') and \
               tag.has_attr('title') and \
               tag.has_attr('class') and not \
                   tag.has_attr('rel') and not \
                   tag.has_attr('a') and not \
                   tag.has_attr('property')

    def find_links(self):

        soup = self.parse_xml()
        links = soup.find_all(self.tag_filter)
        return links

    def tag_split(self):

        dict = {}
        links = self.find_links()
        for line in range(len(links)):
            indice_href = str(links[line]).find('href')
            indice_title = str(links[line]).find('title')
            indice_final = str(links[line]).find('>')
            link = str(links[line])[indice_href + 6:indice_title - 2]
            titulo = str(links[line])[indice_title + 7:indice_final - 6]

            dict_temp = {titulo: link}

            dict.update(dict_temp)
        return dict