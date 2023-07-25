import argparse
from pathlib import Path
import Pandas as pd
import os

from data_class import Data

class Simulation():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')

        self.get_filenames()

        # TODO
        self.simulation_data = self.load_simulation_data()

        # TODOk
        self.frame_filepath_list = self.get_frame_filepaths()

        
    def __delete__(self):
        pass

    def get_filenames(self):
        if argv != sys.argv[1:]:
			os.chdir(sys.path[0])

		self.parser.add_argument('--prefixframe', '-p', type=str, help='prefix for file pattern of frame-by-frame data files')
		self.parser.add_argument('--suffixframe', '-s', type=str, help='suffix for file pattern of frame-by-frame data files')
        self.parser.add_argument('--ifilesimulation', '-i', type=str, help='input file with data for the whole simulation (multiple frames)')

        # https://stackoverflow.com/a/31347222
		self.parser.add_argument('--ifilecolnames', default=False, action=argparse.BooleanOptionalAction, help='simulation input file contains column headers, default False')


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

    def process_frame_data(self)
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