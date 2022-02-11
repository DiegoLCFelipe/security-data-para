import requests
from bs4 import BeautifulSoup


class Links:
    """
    Classe responsável por encontrar e armazenar os links com os dados
    """

    def __init__(self, url):
        """
        Método construtor da classe

        Args:
            url: endereço da página que contém os links de interesse
        """
        self.__url = url

    def request(self):
        """request Executa a requisição no servidor

        Returns:
            [type]: Resposta do servidor
        """
        page = requests.get(self.__url)
        return page

    def parse_xml(self):
        """parse_xml Transformar o código html em um formato mais amigável para o python (unicode)

        Returns:
            [type]: Retorna o arquivo em unicode
        """
        page = self.request()
        soup = BeautifulSoup(page.text, 'lxml')
        return soup

    @staticmethod
    def tag_filter(tag):
        """
        Filtro utilizado para encontrontrar tags espefíficas

        Args:
            tag: tag (não definir o atributo)

        Returns:

        """
        return tag.has_attr('href') and \
               tag.has_attr('title') and \
               tag.has_attr('class') and not \
               tag.has_attr('rel') and not \
               tag.has_attr('a') and not \
               tag.has_attr('property')

    def find_links(self):
        """
        Encontra os links dentro das tags filtradas

        Returns: Retorna os links filtrados

        """
        soup = self.parse_xml()
        links = soup.find_all(self.tag_filter)
        return links

    def tag_split(self):
        """
        Retorna apenas o link da tag

        Returns: Retorna

        """
        links = self.find_links()
        data_links = []
        for line in range(len(links)):
            indice_href = str(links[line]).find('href')
            indice_title = str(links[line]).find('title')

            data_links.append(str(links[line])[indice_href + 6:indice_title - 2])
        return data_links


url = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-2010/'
links = Links(url)
print(links.find_links())

