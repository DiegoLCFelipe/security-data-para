import os
import pandas as pd
from Request import Requester
from Helper.AdpterHTMLToLXML import AdapterHTMLToLXML
from Helper.LXMLHandler import LXMLHandler
from Helper.FileHandler import FileHandler
from bs4 import BeautifulSoup


def should_get_data_from_web(path):
    data_directory_path = path
    print(f"Directory {path} is not empty \n")
    if not os.listdir(data_directory_path):
        return True
    return False

def should_by_pass_file(file_name, exception_words):
    for words in exception_words:
        if words in file_name:
            print(f'By Passing {file_name}')
            return True
        return False


URL_BASE = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-'
DATA_PATH = 'data/'
IGNORED_FILES_NAMES = ['BELÉM']
lst_data_frame = []

# Web Scrapping
if should_get_data_from_web(DATA_PATH):
    print(f'{DATA_PATH} is empty: Performing web scrapping.. {URL_BASE} \n')
    for year in range(2010, 2021)[0:1]:
        portal_transparencia_html = Requester(URL_BASE + str(year)).page_html_code()
        portal_transparencia_html_to_lxml = AdapterHTMLToLXML(portal_transparencia_html).parse_xml()
        lxml_tags_with_urls = LXMLHandler(portal_transparencia_html_to_lxml)
        titles, urls = lxml_tags_with_urls.get_urls()
        for title, url in zip(titles, urls):
            FileHandler(url).save_html_code_locally(DATA_PATH +  str(title) + '_' + str(year) + '.html')

# Data Mananger
for file_name in os.listdir(DATA_PATH):
    if should_by_pass_file(file_name, IGNORED_FILES_NAMES):
        continue

    html_data_saved_locally = FileHandler(DATA_PATH + file_name).open_file()
    lxml_from_data_saved_locally = AdapterHTMLToLXML(html_data_saved_locally).parse_xml()
    print(file_name)
    table_content_from_html_local_file = LXMLHandler(lxml_from_data_saved_locally).table_content()
    table_header_from_html_local_file = LXMLHandler(lxml_from_data_saved_locally).table_header()

    data_table = pd.DataFrame(columns=table_header_from_html_local_file, data=table_content_from_html_local_file)

    print(data_table)

