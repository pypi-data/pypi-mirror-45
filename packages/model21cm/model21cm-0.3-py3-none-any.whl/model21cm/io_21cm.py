import pandas as pd
import os

def get_data_file_path(filename, data_dir='data'):
	start = os.path.abspath(__file__)
	start_dir = os.path.dirname(start)
	data_dir = os.path.join(start_dir, data_dir)
	file_path = os.path.join(data_dir, filename)
	return file_path


def load_data(data_file):
	return pd.read_csv(data_file, sep=',')
