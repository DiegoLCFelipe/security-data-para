import pandas as pd
from Helper.FileHandler import FileHandler
from Helper.DataHandler import DataHandler
from Helper.LogHandler import LogHandler

POPULATION_DATA_FOLDER_PATH = 'data_populacao'
csv_population_data_files = FileHandler(POPULATION_DATA_FOLDER_PATH, LogHandler).get_files_from_folder()

print(csv_population_data_files)
for csv_population_files in csv_population_data_files[1:6]:
    data_population = pd.read_csv(csv_population_files)
    data_population_PA = DataHandler(data_population).filter_data_by_columns_value('UF', 'PA')
    print(data_population_PA)