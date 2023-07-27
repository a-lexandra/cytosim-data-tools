import sys # for command line arguments
import argparse # for parsing command line arguments to script

# https://stackoverflow.com/a/42288083
from pathlib import Path # for stripping filename extensions

import os # for removing files

import pandas as pd # for processing data file

# pd.set_option("display.max_rows", None, "display.max_columns", None)

import pytest

from pathlib import Path

class RuntimeArgumentError(ValueError):
	pass

class MultiFrameError(ValueError):
	pass

class Data():
	def __init__(self, argv=sys.argv[1:], column_list=['class', 'identity']):

		# if (	('--ifile' not in argv) or \
		#  		('-i' not in argv)) or \
		# 		(len(argv) < 2):
		# 	raise ValueError("No input file specified")

		self.cwd = Path.cwd()
		self.parser = argparse.ArgumentParser(description='')
		self.get_args(argv)
		self.args = self.parser.parse_args(argv)

		self.file_dict = {}
		self.get_file_paths()

		self.temp_dataframe = pd.DataFrame()
		self.column_list = column_list
		self.time = None # set by preprocess_file()
		self.preprocess_file()

		self.get_relevant_columns(self.column_list)

		self.output_df = pd.DataFrame()
		if (self.args.largest == True) and ('cluster' in self.temp_dataframe.columns) :
			self.largest_cluster_id = self.get_largest_cluster_id() ;
			self.get_largest_cluster_data()

	def __del__(self):
		self.delete_temp_file()

	def get_args(self, argv):
		"""Parse the command line input flags and arguments"""

		if argv != sys.argv[1:]:
			os.chdir(self.cwd)

		input_file_name = ''
		output_file_name = ''

		self.parser.add_argument('--ifile', '-i', type=str, help='')
		self.parser.add_argument('--ofile', '-o', type=str, help='')
		# https://stackoverflow.com/a/31347222
		self.parser.add_argument('--largest', default=True, action=argparse.BooleanOptionalAction, help='calculate forces exerted by couples attached to filaments beloning to the largest cluster, ignore all other couples')

		

	def get_file_paths(self):
		"""Generate the paths for the file names provided by args

		Return: file names + paths? as a dict?
		"""
		input_file_name=self.args.ifile
		output_file_name=self.args.ofile

		# If outputfile name not provided, replace/add suffix '.dat' to input file name
		if not output_file_name:
			input_file_path  = Path(input_file_name)
			output_file_path = input_file_path.with_suffix('.dat')
			output_file_name = output_file_path.name
		else:
			output_file_path = Path(output_file_name)

		# Copy input file to a temporary file which will be modified
		# (modifications: remove lines and columns with irrelevant comments and data)

		input_file_path = Path(input_file_name)
		temp_file_name = input_file_path.with_suffix('.tmp').name
		temp_file_path = Path(temp_file_name)

		input_dict = {"name": input_file_name, "path": input_file_path}
		output_dict = {"name": output_file_name, "path": output_file_path}
		temp_dict = {"name": temp_file_name, "path": temp_file_path}

		self.file_dict = {"input": input_dict, "output": output_dict, "temp": temp_dict}

	def preprocess_file(self):
		"""Pre-process input data to remove extraneous (non-data or non-column
		header) lines.

		Returns: Pandas dataframe
		"""
		# Remove blank lines and lines with % (Cytosim comments)
		# BUT Keep line with column headers
		# https://stackoverflow.com/a/11969474 , https://stackoverflow.com/a/2369538
		with open(self.file_dict["input"]["path"]) as input_file, \
			 open(self.file_dict["temp"]["path"], 'w') as temp_file:
			for line in input_file:
				if not (line.isspace() or ("%" in line and (not self.column_list[-2] in line))):
					temp_file.write(line.replace("%",""))
				if "time" in line:
					self.time=float(line.split(' ')[-1])
		# Read the whitespace-delimited data file that is output by Cytosim
		self.temp_dataframe = pd.read_csv(self.file_dict["temp"]["path"], delim_whitespace=True)
		# Check that data from only one simulation frame was loaded
		if self.temp_dataframe[self.column_list[-2]].isin([self.column_list[-2]]).any():
			raise ValueError("Data for more than one frame loaded.")

		self.write_temp_dataframe()

	def get_relevant_columns(self, column_list):
		self.temp_dataframe = self.temp_dataframe[column_list]
		self.write_temp_dataframe()

	def get_largest_cluster_id(self):
		return self.temp_dataframe['cluster'].mode().values[0]

	def get_largest_cluster_data(self):
		for cluster_id, df_cluster in self.temp_dataframe.groupby('cluster'):
			if cluster_id == self.largest_cluster_id:
				self.temp_dataframe = df_cluster
				self.write_temp_dataframe()

	def write_temp_dataframe(self):
		# Update the temp file, mostly for debugging.
		# File not used for calculations, calcs done with the dataframe object
		self.temp_dataframe.to_csv(self.file_dict["temp"]["path"], sep="\t", index=None)

	def write_output_file(self):
		# Write to output file
		self.output_df.to_csv(self.file_dict["output"]["path"], float_format='%.8f', header=False, index=None, sep="\t")

	def delete_temp_file(self):
		if os.path.isfile(self.file_dict["temp"]["path"]):
			try:
				os.remove(self.file_dict["temp"]["path"])
			except OSError as e:  ## if failed, report it back to the user ##
				print ("Error: %s - %s." % (e.filename, e.strerror))
