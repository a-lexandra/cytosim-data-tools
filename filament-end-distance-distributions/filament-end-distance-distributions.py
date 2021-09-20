#!/usr/bin/python
"""Usage:
python /path/to/script.py -i input_file.txt

The input file is a single-frame output of Cytosim report function ...

Output file name is automatically generated as ???.dat
If input file already has '.dat' extension, an additional '.dat' is appended to
the input file name to avoid overwriting the input file.
Can specify a custom output file name with the -o flag
"""

import sys # for command line arguments

# https://docs.python.org/3/library/argparse.html
import argparse

# https://docs.python.org/3/library/pathlib.html
# https://stackoverflow.com/a/42288083
from pathlib import Path # for stripping filename extensions

import os # for removing files

import pandas as pd # for processing data file

pd.set_option("display.max_rows", None, "display.max_columns", None)

import numpy as np

import functools

def get_file_names(argv):
	"""Parse the command line input flags and arguments"""

	input_file_name = ''
	output_file_name = ''

	parser = argparse.ArgumentParser(description='Calculate the end-end distribution(s) of filaments in largest cluster only (as defined by motor connectivity),')

	parser.add_argument('-i', '--input', help='-i <input file name>', type=str, required=True)
	parser.add_argument('-o', '--output', help='-o <output file name>', type=str, required=False)
	parser.add_argument('--pp', action='count', default=0)
	parser.add_argument('--pm','--mp', action='count', default=0)
	parser.add_argument('--mm', action='count', default=0)

	args = parser.parse_args(argv)

	input_file_name = args.input

	# If output file name parameter was not specified, set to default
	# Default: remove extension of input file and replace with '.dat'
	if not output_file_name:
		input_file_path = Path(input_file_name)
		input_ext = input_file_path.suffix.lower()
		if input_ext!='.dat':
			output_file_name = input_file_path.with_suffix('.dat')
		else:
			output_file_name = input_file_path.with_suffix('.dat.dat')

	return (input_file_name, output_file_name, bool(args.pp), bool(args.pm), bool(args.mm))

def calc_distance(arr_a, arr_b):
	return np.linalg.norm(np.asarray(arr_a) - np.asarray(arr_b))

def process_file(input_file_name, output_file_name, \
				 generate_plus_plus, generate_plus_minus, generate_minus_minus):
	"""Open input file, make a copy, remove unnecessary lines, process data,
	write to output file
	"""

	# Copy input file to a temporary file which will be modified
	# (modifications: remove lines and columns with irrelevant comments and data)

	input_file_path = Path(input_file_name)
	temp_file_name = input_file_path.with_suffix('.tmp')
	temp_file_path = Path(temp_file_name)

	### Pre-process input data in temp file ###

	# Remove blank lines and lines with % (Cytosim comments)
	# BUT Keep line with column headers
	# https://stackoverflow.com/a/11969474 , https://stackoverflow.com/a/2369538
	with open(input_file_name) as input_file, open(temp_file_name, 'w') as temp_file:
		for line in input_file:
			if not (line.isspace() or ("%" in line and (not "class" in line))):
				temp_file.write(line.replace("%",""))

	# Read the whitespace-delimited data file that is output by Cytosim
	temp_dataframe = pd.read_csv(temp_file_name, delim_whitespace=True)

	# Update the temp file, mostly for debugging.
	# File not used for calculations, calcs done with the dataframe object
	#temp_dataframe.to_csv(temp_file_name, sep="\t", index=None)

	### Write to output file ###
	output_file_path = Path(output_file_name)

	cluster_idx = 0

	fil_length=0.25

	distance_cutoff=fil_length*2

	# initialize the cluster id for all filaments (sequentially)

	num_filaments=temp_dataframe.shape[0]

	output_df = pd.DataFrame(columns=['distance_MM', 'distance_PM', 'distance_PP'])

	for fil_i, df_fil_i in temp_dataframe.groupby('identity'):
		fil_i_id=df_fil_i['identity'].values[0]
		# temp_dataframe.loc[(temp_dataframe.identity == fil_i_id), 'identity']=69
		fil_i_pos_M_arr=df_fil_i[['posMX', 'posMY']].values[0]
		fil_i_pos_P_arr=df_fil_i[['posPX', 'posPY']].values[0]

		for fil_j, df_fil_j in temp_dataframe.groupby('identity'):
			fil_j_id=df_fil_j['identity'].values[0]

			if fil_j_id > fil_i_id:
				fil_j_pos_M_arr=df_fil_j[['posMX', 'posMY']].values[0]
				fil_j_pos_P_arr=df_fil_j[['posPX', 'posPY']].values[0]

				if generate_plus_plus:
					distance_PP=calc_distance(tuple(fil_i_pos_P_arr), tuple(fil_j_pos_P_arr))
					if distance_PP < distance_cutoff:
						output_df = output_df.append({'distance_PP' : float(distance_PP)}, ignore_index=True)

				if generate_plus_minus:
					distance_PM=calc_distance(tuple(fil_i_pos_P_arr), tuple(fil_j_pos_M_arr))
					if distance_PM < distance_cutoff:
						output_df = output_df.append({'distance_PM' : float(distance_PM)}, ignore_index=True)

				if generate_minus_minus:
					distance_MM=calc_distance(tuple(fil_i_pos_M_arr), tuple(fil_j_pos_M_arr))
					if distance_MM < distance_cutoff:
						output_df = output_df.append({'distance_MM' : float(distance_MM)}, ignore_index=True)

	if generate_minus_minus:
		df_MM=output_df.distance_MM.dropna()
		df_MM.to_csv(output_file_path.with_suffix('.distance_MM.dat'), header=False, index=None, sep="\t")

	if generate_plus_minus:
		df_PM=output_df.distance_PM.dropna()
		df_PM.to_csv(output_file_path.with_suffix('.distance_PM.dat'), header=False, index=None, sep="\t")

	if generate_plus_plus:
		df_PP=output_df.distance_PP.dropna()
		df_PP.to_csv(output_file_path.with_suffix('.distance_PP.dat'), header=False, index=None, sep="\t")

	try:
		os.remove(temp_file_path)
	except OSError as e:  ## if failed, report it back to the user ##
		print ("Error: %s - %s." % (e.filename, e.strerror))

def main(argv):

	# Get file name(s) from command line arguments
	(input_file_name, output_file_name, \
		generate_plus_plus, generate_plus_minus, \
		generate_minus_minus) = get_file_names(argv)

	# Do the calculations and output results to file
	process_file(input_file_name, output_file_name,\
				 generate_plus_plus, generate_plus_minus, generate_minus_minus)


if __name__ == "__main__":
	# Performance profiling code
	import timeit
	print(timeit.repeat('main(sys.argv[1:])', setup="from __main__ import main",number=1,repeat=10))
	#main(sys.argv[1:])
