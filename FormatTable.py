import pandas as pd

class FormatTable:
    def __init__(self, dados):
        self._dados = dados

    @property
    def dados(self):
        return self._dados

    def wide_to_long_format(self, id_columns, values_columns, id_columns_name, values_columns_name):
        """
            Transforma uma ou mais colunas (variáveis identificadoras) em linhas , enquanto todas as outras colunas
             (variáveis medidads) não são transpostas. A transposição resulta em duas colunas não nomeadas que devem
             ser nomeadas manualmente.

        Args:
            id_columns: colunas não transpostas
            values_columns: colunas que transformadas em linhas
            id_columns_name: nome da colunas com as variáveis identificadoras
            values_columns_name: nome da coluna com os valores das variáveis identificadoras

        Returns:
            Retorna um dataFrama em formato longo

        """
        self._dados = pd.melt(self._dados, id_vars=id_columns, value_vars=values_columns, var_name=id_columns_name,
                              value_name=values_columns_name)

    def repeat_record(self, by_column):
        """
        Usa uma coluna numérica para gerar um número de registros igual ao valor da coluna numérica

        Args:
            by_column: Coluna numérica utilizada como parâmetro para a criação dos novos registros
        """
        self._dados.dropna(inplace=True)
        self._dados = self._dados.reindex(self._dados.index.repeat(self._dados[by_column]))
        self._dados.drop(columns=by_column, inplace=True)

    def create_columns(self, columns, columns_values):
        """
        Cria novas colunas com valores únicos

        Args:
            columns: Nome das novas colunas
            columns_values: Mono valor utilizado nas novas colunas

        """
        for columns, values in zip(columns, columns_values):
            self._dados[columns] = values

    def save_table(self, path):
        """
        Salva o dataFrame em um arquivo

        Args:
            path: Caminho onde o arquivo deverá ser salvo
        """
        self._dados.to_csv(path, index=False)