import os
import pandas as pd
from Request import Requester
from Helper.AdpterHTMLToLXML import AdapterHTMLToLXML
from Helper.LXMLHandler import LXMLHandler
from Helper.FileHandler import FileHandler
from Helper.LogHandler import LogHandler
from bs4 import BeautifulSoup

logHandler = LogHandler()

def should_get_data_from_web(path):
    data_directory_path = path
    logHandler.log_error_timestamp(f"Directory {path} is not empty \n")
    if not os.listdir(data_directory_path):
        return True
    return False

def should_by_pass_file(file_name, exception_words):
    for words in exception_words:
        if words in file_name:
            logHandler.log_info_timestamp(f'By Passing {file_name}')
            return True
        return False


URL_BASE = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-'
DATA_PATH = 'data/'
IGNORED_FILES_NAMES = ['BELÉM']
lst_data_frame = []

# Web Scrapping
if should_get_data_from_web(DATA_PATH):
    logHandler.log_info_timestamp(f'{DATA_PATH} is empty: Performing web scrapping.. {URL_BASE} \n')
    for year in range(2010, 2021)[0:1]:
        portal_transparencia_html = Requester(URL_BASE + str(year), logHandler).page_html_code()
        portal_transparencia_html_to_lxml = AdapterHTMLToLXML(portal_transparencia_html).parse_xml()
        lxml_tags_with_urls = LXMLHandler(portal_transparencia_html_to_lxml)
        titles, urls = lxml_tags_with_urls.get_urls()
        for title, url in zip(titles, urls):
            FileHandler(url, logHandler).save_html_code_locally(DATA_PATH +  str(title) + '_' + str(year) + '.html')

# Data Mananger
for file_name in os.listdir(DATA_PATH):
    if should_by_pass_file(file_name, IGNORED_FILES_NAMES):
        continue

    html_data_saved_locally = FileHandler(DATA_PATH + file_name, logHandler).open_file()
    lxml_from_data_saved_locally = AdapterHTMLToLXML(html_data_saved_locally).parse_xml()
    table_content_from_html_local_file = LXMLHandler(lxml_from_data_saved_locally).table_content()
    table_header_from_html_local_file = LXMLHandler(lxml_from_data_saved_locally).table_header()

    data_table = pd.DataFrame(columns=table_header_from_html_local_file, data=table_content_from_html_local_file)

    # Remove columns 'Total'
#     data_frame.drop(data_frame.columns[-1], axis=1, inplace=True)
#
#     # Transpose dataFrama month columns
#     data_frame_transposed = pd.melt(data_frame, id_vars=data_frame.columns[0:2], value_vars=data_frame.columns[2:],
#                                     var_name='MÊS',
#                                     value_name='NÚMERO DE OCORRÊNCIAS')
#
#     # Remove NaN, None, Null etc.
#     data_frame_transposed.dropna(inplace=True)
#
#     # Transform NÚMERO DE OCORRÊNCIAS values in new registry's
#     data_frame_transposed = data_frame_transposed.reindex(
#         data_frame_transposed.index.repeat(data_frame_transposed['NÚMERO DE OCORRÊNCIAS']))
#
#     # Drop NÚMERO DE OCORRÊNCIAS
#     data_frame_transposed.drop(columns='NÚMERO DE OCORRÊNCIAS', inplace=True)
#
#     # Create columns ANO and TIPO DE OCORRÊNCIA
#     data_frame_transposed['ANO'] = file_name[-9:-5]
#     data_frame_transposed['TiPO DE OCORRÊNCIA'] = file_name[:-10]
#
#     print(data_frame_transposed)
#     lst_data_frame.append(data_frame_transposed)
#
# data_concat = pd.concat(lst_data_frame, ignore_index=True)
# data_concat.to_csv('ocorrencias.csv')
