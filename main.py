import os
import pandas as pd
from Request import Requester
from Helper.AdpterHTMLToLXML import AdapterHTMLToLXML
from Helper.LXMLHandler import LXMLHandler
from Helper.FileHandler import FileHandler
from Helper.LogHandler import LogHandler
from Helper.DataHandler import DataHandler


def should_get_data_from_web(path):
    data_directory_path = path
    if not os.listdir(data_directory_path):
        logHandler.log_info_timestamp(f'{DATA_PATH} is empty: Performing web scrapping.. {URL_BASE} \n')
        return True
    logHandler.log_warning_timestamp(f"Directory {path} is not empty \n")
    return False


def should_by_pass_file(file_name, exception_words):
    for words in exception_words:
        if words in file_name:
            logHandler.log_info_timestamp(f'By Passing {file_name}')
            return True
        return False


logHandler = LogHandler()
TOTAL_COLUMN_INDEX = -1
URL_BASE = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-'
DATA_PATH = 'data/'
FIRST_YEAR = 2010
LAST_YEAR = 2021
IGNORED_FILES_NAMES = ['BELÉM']
lst_data_frame = []

# Web Scrapping
if should_get_data_from_web(DATA_PATH):
    for year in range(FIRST_YEAR, LAST_YEAR):
        portal_transparencia_html = Requester(URL_BASE + str(year), logHandler).page_html_code()
        portal_transparencia_html_to_lxml = AdapterHTMLToLXML(portal_transparencia_html).parse_xml()
        lxml_tags_with_urls = LXMLHandler(portal_transparencia_html_to_lxml)
        titles, urls = lxml_tags_with_urls.get_urls()
        for title, url in logHandler.using_loading_bar(zip(titles, urls), total=len(urls)):
            FileHandler(url, logHandler).save_html_code_locally(DATA_PATH + str(title) + '_' + str(year) + '.html')

# Data Mananger
lst_data_security = []
for file_name in logHandler.using_loading_bar(os.listdir(DATA_PATH), description=f'Reading files from: {DATA_PATH}'):
    if should_by_pass_file(file_name, IGNORED_FILES_NAMES):
        continue

    html_data_saved_locally = FileHandler(DATA_PATH + file_name, logHandler).open_file()
    lxml_from_data_saved_locally = AdapterHTMLToLXML(html_data_saved_locally).parse_xml()
    table_content_from_html_local_file = LXMLHandler(lxml_from_data_saved_locally).table_content()
    table_header_from_html_local_file = LXMLHandler(lxml_from_data_saved_locally).table_header()

    data_table = pd.DataFrame(columns=table_header_from_html_local_file, data=table_content_from_html_local_file)
    data_security = DataHandler(data_table)
    data_security.drop_columns([TOTAL_COLUMN_INDEX])

    data_security.transpose_data_frame(id_columns=data_security.data_frame_columns[0:1],
                                       value_columns=data_security.data_frame_columns[2:],
                                       id_columns_names='MÊS',
                                       value_columns_name='QUANTIDADE')

    data_security.add_column('ANO', str(file_name)[-9:-5])
    data_security.add_column('OCORRÊNCIA', str(file_name)[:-10])

    data_security.drop_null_values()

    lst_data_security.append(data_security.data_frame)

full_data_security = pd.concat(lst_data_security)
full_data_security.to_csv('ocorrencias.csv')
