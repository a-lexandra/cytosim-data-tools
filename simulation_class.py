import argparse
from pathlib import Path
import pandas as pd
import os
import sys
import re
import numpy as np


from data_class import Data

class Simulation():
    def __init__(self, argv=sys.argv[1:], column_list=['class', 'identity'], simulation_column_list=['frame', 'time', 'fil_id', 'f_posX', 'f_posY', 'f_dirX', 'f_dirY']):
        self.column_list = column_list
        self.simulation_column_list = simulation_column_list

        self.cwd = Path.cwd()
        self.parser = argparse.ArgumentParser(description='')
        self.get_args(argv)
        self.args = self.parser.parse_args(argv)

        self.load_config_params()

        self.frame_fname_search_pattern = self.get_frame_filename_pattern()

        self.simulation_file_path = Path.joinpath(self.cwd, self.args.ifilesimulation)

        if os.path.getsize(self.simulation_file_path) > 0:
            self.simulation_df = self.load_simulation_data()
        else:
            self.simulation_df = None

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

        self.parser.add_argument('--ofile', '-o', type=str, default='dk.dat', help='name for the file to write output data')

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
        df = pd.read_csv(self.simulation_file_path, delim_whitespace=True, names=self.simulation_column_list)

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

    def load_config_params(self):
        with open('config.cym', 'r') as config_file:
            lines = config_file.readlines()

            for line in lines:
                if 'unloaded_speed' in line:
                    self.unloaded_speed = np.float(line.strip().split(' ')[-1])
                if 'unbinding_force' in line:
                    self.unbinding_force = np.float(line.strip().split(' ')[-1])


if __name__=="__main__":
    #column_list = ['identity', \
    #               'fiber1', 'pos1X', 'pos1Y', \
    #               'fiber2', 'pos2X', 'pos2Y',\
    #               'force']

    column_list = ['class','identity','fiber1','abscissa1','pos1X','pos1Y','dirFiber1X','dirFiber1Y','fiber2','abscissa2','pos2X','pos2Y','dirFiber2X','dirFiber2Y','force','cos_angle']

    mySimulation = Simulation(column_list=column_list)

    breakpoint()

    del mySimulation

# how to overwrite methods in child classes???

# maybe things below will not be in init, idk

        # load forces.dat for whole simulation

        # get data file name pattern (e.g. report*.txt)

        # iterate over data files - create Data struct for each file and process
            # does Data have a child class for calculating motor force vector and extension? - find!
