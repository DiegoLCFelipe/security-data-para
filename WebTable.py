import requests
from bs4 import BeautifulSoup


class WebTable:
    """ Extração e armazenamento de tabelas de páginas html
    """

    def __init__(self, url):
        """__init__ Método construtor de classe

        Args:
            url (str): endreço da página que contém a tabela
            id (str): id do objeto tabela dentro do código html

        Raises:
            ValueError: Sem resposta 
        """
        print("Scrapping Table... {}".format(self))
        self.__url = url
        self.__page = self.request()

    def request(self):
        """request Executa a requisição no servidor 

        Returns:
            [type]: Resposta do servidor
        """
        return requests.get(self.__url)


    def parse_xml(self):
        """parse_xml Transformar o código html em um formato mais amigável para o python (unicode)

        Returns:
            [type]: Retorna o arquivo em unicode
        """

        return BeautifulSoup(self.__page.text, 'lxml')

    def find_table(self):
        """find_table Procura a tabela dentro da página

        Returns:
            Retorna apenas a tabela
        """
        return self.parse_xml().find('table')

    def table_header(self):
        """table_header Procrua do cabeçalho da tabela

        Returns:
            Cabeçalho da tabela
        """
        self.find_table()
        self.header = []
        for i in self.find_table().find_all('th'):
            titulo = i.text
            self.header.append(titulo)
        return self.header

    def table_content(self):
        """table_content Procura o conteúdo da tabela

        Returns:
            Retorna o conteúdo da tabela
        """
        self.find_table()
        self.lst_row = []
        for j in self.find_table().find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            self.lst_row.append(row)

        return self.lst_row
