import requests
from bs4 import BeautifulSoup
import pandas as pd
from WebTable import WebTable
from FormatTable import FormatTable

path = 'http://sistemas.segup.pa.gov.br/transparencia/'

dic_tabels = {
    'tablepress-145': 'homicidios-2021',
    'tablepress-151': 'latrocinios-2021',
    'tablepress-155': 'lesao-corporal-seguida-de-morte-2021',
    'tablepress-153': 'roubo-2021',
    'tablepress-154': 'trafico-2021',
    'tablepress-156': 'estupros-2020-3',
    'tablepress-158': 'furtos-2021',
    'tablepress-152': 'lesao-corporal-2020-2',

    'tablepress-159': 'homicidios-no-transito-2021',
    'tablepress-160': 'morte-no-transito-2021',
    'tablepress-161': 'lesao-no-transito-2021',
    'tablepress-168': 'morte-decorrente-de-intervencao-policial-2021',
    'tablepress-169': 'policiais-mortos-em-servico-2021',
    'tablepress-170': 'policiais-mortos-fora-de-servico-2021',
    'tablepress-171': 'feminicidio-2021'
}

lst_dados = []

for key, value in zip(dic_tabels.keys(), dic_tabels.values()):
    Table = WebTable(path + value)
    header = Table.table_header()
    content = Table.table_content()

    id_vars = header[0:1]

    value_vars = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET']

    dados = pd.DataFrame(columns=header[0:12], data=content)
    table_formated = FormatTable(dados)
    table_formated.wide_to_long_format(id_vars, value_vars, 'MÊS', 'N_OCORRENCIAS')
    table_formated.repeat_record('N_OCORRENCIAS')
    table_formated.create_columns(['CRIME', 'ANO'], [value[:-5], '2021'])
    lst_dados.append(table_formated.dados)

dados = pd.concat(lst_dados, ignore_index=True)
dados.to_csv('ocorrencias.csv', index=False)
print(dados)


