import pandas as pd
import os

class Data21Cm:

        def __init__(self, filename, data_dir='data'):
                self.filename = filename
                self.data_dir = data_dir
                self.data_path = get_data_file_path(filename, data_dir)
                self.full_data = load_data(self.data_path)
                self.frequencies = self.full_data.iloc[:,0]
                self.temp = self.full_data.iloc[:,2]


def get_data_file_path(filename, data_dir='data'):
	start = os.path.abspath(__file__)
	start_dir = os.path.dirname(start)
	data_dir = os.path.join(start_dir, data_dir)
	file_path = os.path.join(data_dir, filename)
	return file_path


def load_data(data_file):
	return pd.read_csv(data_file, sep=',')
