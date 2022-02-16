from bs4 import BeautifulSoup


class WebTable:
    def __init__(self, html_path):
        self.__html_path = html_path
        self.__html_file = self.open_file()
        self.__lxml_data = self.parse_lxml()
        self.__lxml_table_data = self.find_table()

    @property
    def html_path(self):
        return self.__html_path

    @html_path.setter
    def html_path(self, value):
        self.__html_path = value

    @property
    def lxml_data(self):
        return self.__lxml_data

    @property
    def lxml_table_data(self):
        return self.__lxml_table_data

    def open_file(self):
        return open(self.__html_path)

    def parse_lxml(self):
        return BeautifulSoup(self.__html_file, 'lxml')

    def find_table(self):
        return self.__lxml_data.find('table')

    def table_header(self):
        table_content = self.table_content()
        header = []
        for i in self.__lxml_table_data.find_all('th'):
            title = i.text
            header.append(title)

        if len(header) > len(table_content[0]):
            return header[0:len(table_content[0])]

        return header

    def table_content(self):
        lst_row_data = []
        for j in self.find_table().find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            lst_row_data.append(row)

        return lst_row_data
