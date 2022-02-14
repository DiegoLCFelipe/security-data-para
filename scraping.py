import pandas as pd
from WebTable import WebTable
from FormatTable import FormatTable
from Links import Links

url = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-2021/'

lst_dados = []

links = Links(url)
dict_tables = links.tag_split()

print(dict_tables)

for title, link in zip(dict_tables.keys(), dict_tables.values()):
    if title != 'Ocorrências':
        Table = WebTable(link)
        header = Table.table_header()
        content = Table.table_content()

        id_vars = header[0:2]
        value_vars = header[2:12]
    else:
        continue

    dados = pd.DataFrame(columns=header[0:12], data=content[0:12])

    table_formated = FormatTable(dados)
    table_formated.wide_to_long_format(id_vars, value_vars, 'MÊS', 'N_OCORRENCIAS')
    table_formated.repeat_record('N_OCORRENCIAS')
    table_formated.create_columns(['CRIME', 'ANO'], [title, url[-1:-5]])
    lst_dados.append(table_formated.dados)

dados = pd.concat(lst_dados, ignore_index=True)
# # dados.to_csv('ocorrencias.csv', index=False)
print(dados)
