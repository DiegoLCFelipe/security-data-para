import pandas as pd
from WebTable import WebTable
from Links import Links
from FormatTableStrategies.IterfaceTableStrategy import InterfaceTableFormatStrategy
from FormatTableStrategies.FormatTableStrategy import FormatTableStrategy

url = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-'

lst_dados = []
content_columns_dropped = []
lst_data_formated = []
year = 2020

links = Links(url + str(year))
dict_tables = links.tag_split()


class DataFrame:

    def __init__(self, strategy):
        self._header = None
        self._content = None
        self._strategy = strategy

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: InterfaceTableFormatStrategy):
        self._strategy = strategy

    def create_dataFrame_of_year(self):
        zipped_dictionary_table = zip(dict_tables.keys(), dict_tables.values())

        for title, link in zipped_dictionary_table:

            if self._should_by_pass_table(title):
                continue

            self._header, self._content = self._get_header_and_content(link)

            self._apply_line_format_strategy()

        return pd.DataFrame(columns=self._header[0:15], data=self._content)

    @staticmethod
    def _should_by_pass_table(with_title, exception_titles):
        for title in exception_titles:
            if title in with_title:
            return True
        return False

    def _apply_line_format_strategy(self):
        for table_line in self._content:
            for index, item in enumerate(table_line):
                table_line[index] = self._strategy.formatLine(self, table_line=table_line[index])

    @staticmethod
    def _get_header_and_content(from_link):
        table = WebTable(from_link)
        return table.header, table.content


meuObjetoTop = DataFrame(FormatTableStrategy)

print(meuObjetoTop.create_dataFrame_of_year())