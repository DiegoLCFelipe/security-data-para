import pandas as pd
from WebTable import WebTable
from Links import Links

url = 'http://sistemas.segup.pa.gov.br/transparencia/estatisticas-2019/'

lst_dados = []

links = Links(url)
dict_tables = links.tag_split()
content_columns_dropped = []
lst_data_formated = []

for title, link in zip(dict_tables.keys(), dict_tables.values()):
    if ('BELÉM' in title) or (title == 'Ocorrências'):
        continue

    else:
        Table = WebTable(link)
        header = Table.header
        content = Table.content

        id_vars = header[0:2]
        value_vars = header[2:14]

        for table_line in content:
            for index, item in enumerate(table_line):
                table_line[index] = table_line[index].replace(",", "")

            content_columns_dropped.append((table_line[:-1]))

        dados = pd.DataFrame(columns=header[0:14], data=content_columns_dropped)

        data_transposed = pd.melt(dados, id_vars=id_vars, value_vars=value_vars, var_name='MÊS',
                                  value_name='N_OCORRENCIAS')

        data_transposed.dropna(inplace=True)

        data_transposed = data_transposed.reindex(data_transposed.index.repeat(data_transposed['N_OCORRENCIAS']))

        data_transposed.drop(columns='N_OCORRENCIAS', inplace=True)

        data_transposed['ANO'] = url[-5:-1]
        data_transposed['OCORRÊNCIA'] = title

        if header[0] == 'MUNICIPIOS':
            data_transposed.rename({'MUNICIPIOS': 'MUNICIPIO'}, axis='columns', inplace=True)

        lst_data_formated.append(data_transposed)

data_transposed = pd.concat(lst_data_formated, ignore_index=True)
data_transposed.to_csv('ocorrencias.csv', index=False)
print(data_transposed)
