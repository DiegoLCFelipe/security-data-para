import pandas as pd
from WebTable import WebTable
from os import listdir
from Links import Links
import urllib.request
from bs4 import BeautifulSoup
from FormatTableStrategies.IterfaceTableStrategy import InterfaceTableFormatStrategy
from FormatTableStrategies.FormatTableStrategy import FormatTableStrategy


def should_by_pass_file(file_name, exception_words):
    for words in exception_words:
        if words in file_name:
            return True
        return False


# for year in range(2010, 2021):
#     tables_links = Links(url_base + str(year))
#     dict_tables = tables_links.tag_split()
#
#     zipped_dictionary_table = zip(dict_tables.keys(), dict_tables.values())
#     for title, link in zipped_dictionary_table:
#         urllib.request.urlretrieve(link, 'data/' + str(title) + '_' + str(year) + '.html')

lst_data_frame = []
url_base = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-'

# Validation : Verify valid files
for file_name in listdir('data'):
    if should_by_pass_file(file_name, ['BELÉM', 'Ocorrências']):
        continue

    table_from_web = WebTable('data/' + file_name)
    data_frame = pd.DataFrame(columns=table_from_web.table_header(), data=table_from_web.table_content())
    # Remove columns 'Total'
    data_frame.drop(data_frame.columns[-1], axis=1, inplace=True)

    # Transpose dataFrama month columns
    data_frame_transposed = pd.melt(data_frame, id_vars=data_frame.columns[0:2], value_vars=data_frame.columns[2:],
                                    var_name='MÊS',
                                    value_name='NÚMERO DE OCORRÊNCIAS')

    # Remove NaN, None, Null etc.
    data_frame_transposed.dropna(inplace=True)

    # Transform NÚMERO DE OCORRÊNCIAS values in new registry's
    data_frame_transposed = data_frame_transposed.reindex(
        data_frame_transposed.index.repeat(data_frame_transposed['NÚMERO DE OCORRÊNCIAS']))

    # Drop NÚMERO DE OCORRÊNCIAS
    data_frame_transposed.drop(columns='NÚMERO DE OCORRÊNCIAS', inplace=True)

    # Create columns ANO and TIPO DE OCORRÊNCIA
    data_frame_transposed['ANO'] = file_name[-9:-5]
    data_frame_transposed['TiPO DE OCORRÊNCIA'] = file_name[:-10]

    lst_data_frame.append(data_frame_transposed)

data_concat = pd.concat(lst_data_frame, ignore_index=True)
data_concat.to_csv('ocorrencias.csv')

