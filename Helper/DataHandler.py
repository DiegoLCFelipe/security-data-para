import pandas as pd


class DataHandler:

    def __init__(self, data_frame):
        self._data_frame = data_frame
        self._columns = self.columns()

    @property
    def data_frame(self):
        return self._data_frame

    @property
    def data_frame_columns(self):
        return self._columns

    @data_frame_columns.setter
    def data_frame_columns(self, value):
        self._columns = value

    def columns(self):
        return self._data_frame.columns

    def drop_columns(self, columns):
        self._data_frame.drop(self.data_frame.columns[columns], axis=1, inplace=True)
        self._columns = self.columns()

    def drop_null_values(self):
        self._data_frame.dropna(inplace=True)

    def transpose_data_frame(self, id_columns, value_columns, id_columns_names, value_columns_name):
        self._data_frame = pd.melt(self.data_frame,
                                   id_vars=id_columns,
                                   value_vars=value_columns,
                                   var_name=id_columns_names,
                                   value_name=value_columns_name)

        self._columns = self.columns()

    def add_column(self, column_name, values):
        self._data_frame.insert(loc=len(self._columns), column=column_name, value=values)
