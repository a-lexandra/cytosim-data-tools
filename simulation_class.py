import argparse
from pathlib import Path
import pandas as pd
import os
import sys

from data_class import Data

class Simulation():
    def __init__(self, argv=sys.argv[1:]):
        self.parser = argparse.ArgumentParser(description='')
        self.get_args(argv)
        self.args = self.parser.parse_args(argv)

        self.frame_fname_search_pattern = self.get_frame_filename_pattern()

        # TODO
        self.simulation_data = self.load_simulation_data()

        # TODO
        self.frame_filepath_list = self.get_frame_filepaths()

        
    def __delete__(self):
        pass

    def get_args(self, argv):
        if argv != sys.argv[1:]:
            os.chdir(sys.path[0])

        self.parser.add_argument('--prefixframe', '-p', type=str, default='', help='prefix for file pattern of frame-by-frame data files')
        self.parser.add_argument('--suffixframe', '-s', type=str, default='', help='suffix for file pattern of frame-by-frame data files')
        self.parser.add_argument('--extframe', '-e', type=str, help='extension for files of frame-by-frame data')
        self.parser.add_argument('--ifilesimulation', '-i', type=str, help='input file with data for the whole simulation (multiple frames)')

        # https://stackoverflow.com/a/31347222
        self.parser.add_argument('--ifilecolnames', default=False, action=argparse.BooleanOptionalAction, help='simulation input file contains column headers, default False')

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
                              '.' + \
                              self.args.extframe

        return fname_match_str

    def load_simulation_data(self):
        # return np.loadtxt(self.parser.ifilesimulation)
        # for now return generic numpy array? or maybe pandas - might need paths for pandas
        # overwrite for specific uses in child classes
        # arg for if column names are present? or check each time 
        pass

    def get_frame_filepaths(self):
        frame_filepath_list = []
        # get filenames that match pattern provided through parser
        # will likely need pathlib for finding files matching patterns
        # get paths for those files

        return frame_filepath_list

    def load_frame_data(self):
        # load data from each frame file as a pandas df - generic
        pass

    def process_frame_data(self):
        # generic - get timestamp and loaded columns
        pass


if __name__=="__main__":
    mySimulation = Simulation()

    del mySimulation

# how to overwrite methods in child classes???

# maybe things below will not be in init, idk

        # load forces.dat for whole simulation

        # get data file name pattern (e.g. report*.txt)

        # iterate over data files - create Data struct for each file and process
            # does Data have a child class for calculating motor force vector and extension? - find!