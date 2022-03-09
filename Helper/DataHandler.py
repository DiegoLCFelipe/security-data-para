import pandas as pd
from tqdm import tqdm


def pandas_load_bar_customization():
    tqdm.pandas(bar_format="{desc}: {percentage:.1f}%|{bar}| {n:.0f}/{total_fmt} [{elapsed}<{remaining}]")


pandas_load_bar_customization()


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

    def drop_columns_by_index(self, index):
        self._data_frame.drop(self.data_frame.columns[index], axis=1, inplace=True)
        self._columns = self.columns()

    def drop_columns_by_name(self, columns):
        self._data_frame.drop(columns, axis=1, inplace=True)
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

    def concat_broken_columns(self, columns_to_concate, new_column_name):
        self._data_frame[new_column_name] = self._data_frame[columns_to_concate].progress_apply(
            lambda x: ''.join(x.dropna().astype(str)), axis=1)

    def filter_data_by_columns_value(self, column, value):
        return self._data_frame.loc[self._data_frame[column]==value]

    def save_data_as_csv(self, path):
        self._data_frame.to_csv(path, index=False)
