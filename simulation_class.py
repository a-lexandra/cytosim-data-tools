import argparse
from pathlib import Path
import pandas as pd
import os
import sys
import re

from data_class import Data

class Simulation():
    def __init__(self, argv=sys.argv[1:], column_list=['class', 'identity']):
        self.column_list = column_list

        self.cwd = Path.cwd()
        self.parser = argparse.ArgumentParser(description='')
        self.get_args(argv)
        self.args = self.parser.parse_args(argv)

        self.frame_fname_search_pattern = self.get_frame_filename_pattern()

        self.simulation_file_path = Path.joinpath(self.cwd, self.args.ifilesimulation)

        self.simulation_df = self.load_simulation_data()

        self.frame_filepath_list = self.get_frame_filepaths()

        (self.frame_data_list, self.frame_time_list) = self.load_frame_data()
        
    def __delete__(self):
        for frame in self.frame_data_list:
            del frame

    def get_args(self, argv):
        if argv != sys.argv[1:]:
            os.chdir(self.cwd)

        self.parser.add_argument('--prefixframe', '-p', type=str, default='', help='prefix for file pattern of frame-by-frame data files')
        self.parser.add_argument('--suffixframe', '-s', type=str, default='', help='suffix for file pattern of frame-by-frame data files')
        self.parser.add_argument('--extframe', '-e', type=str, default='', help='extension for files of frame-by-frame data')
        self.parser.add_argument('--ifilesimulation', '-i', type=str, default='', help='input file with data for the whole simulation (multiple frames)')

        # https://stackoverflow.com/a/31347222
        self.parser.add_argument('--ifilecolnames', '-c', type=str, default='', help='file with column names for whole simulation input file')

        self.parser.add_argument('--ofile', '-o', type=str, default='k_eff.dat', help='name for the file to write output data')

    def get_frame_filename_pattern(self):
        # assemble prefix + * + suffix + extension into a match pattern 
        if self.args.extframe.count('.') == 1:
            fname_match_str = self.args.prefixframe + \
                              '[0-9]+' + \
                              self.args.suffixframe + \
                              self.args.extframe
        elif self.args.extframe.count('.') == 0:
            fname_match_str = self.args.prefixframe + \
                              '[0-9]+' + \
                              self.args.suffixframe + \
                              r'\.' + \
                              self.args.extframe

        return fname_match_str

    def load_simulation_data(self):
        col_names = []

        if len(self.args.ifilecolnames) > 0:
            col_name_file_path = Path.joinpath(self.cwd, self.args.ifilecolnames)
            with open(col_name_file_path, 'r') as col_file:
                lines = col_file.readlines()
                num_lines = sum(1 for line in lines)

                if num_lines == 1:
                    for line in lines:
                        col_names = line.strip().split(' ')

        df = pd.read_csv(self.simulation_file_path, delim_whitespace=True, names=col_names)

        return df

    def get_frame_filepaths(self):
        frame_filepath_list = []
    
        root_dir = self.cwd

        regex = re.compile(self.frame_fname_search_pattern)

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if regex.match(file):
                    file_path = Path(root).joinpath(file).absolute()
                    
                    if Path(root) == self.cwd:
                        frame_filepath_list.append(file_path)

        return frame_filepath_list

    def load_frame_data(self):
        frame_data_list = []
        frame_time_list = []

        for path in self.frame_filepath_list:
            # breakpoint()
            frame = Data(argv=['--ifile', path.name], \
                         column_list=self.column_list)
            frame_data_list.append(frame)
            frame_time_list.append(frame.time)

        def sort_frame_by_time(f):
            return f.time 

        frame_data_list.sort(key=sort_frame_by_time)
        frame_time_list.sort()

        return frame_data_list, frame_time_list

if __name__=="__main__":
    column_list = ['identity', \
                   'fiber1', 'pos1X', 'pos1Y', \
                   'fiber2', 'pos2X', 'pos2Y',\
                   'force']

    mySimulation = Simulation(column_list=column_list)

    del mySimulation

# how to overwrite methods in child classes???

# maybe things below will not be in init, idk

        # load forces.dat for whole simulation

        # get data file name pattern (e.g. report*.txt)

        # iterate over data files - create Data struct for each file and process
            # does Data have a child class for calculating motor force vector and extension? - find!