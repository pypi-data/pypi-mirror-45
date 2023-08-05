import pandas as pd #use this to handle data
import os

from io_21cm import get_data_file_path
from io_21cm import load_data

class Data21Cm:

	def __init__(self, filename, data_dir='data'):
		self.filename = filename
		self.data_dir = data_dir
		self.data_path = get_data_file_path(filename, data_dir)
		self.full_data = load_data(self.data_path)
		self.frequencies = self.full_data.iloc[:,0]
		self.temp = self.full_data.iloc[:,2]

#data21cm = Data21Cm('figure1_plotdata.csv')				
