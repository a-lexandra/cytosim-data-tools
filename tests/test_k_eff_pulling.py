from simulation_class import Simulation
from data_class import Data
from k_eff_pulling import KeffData

import pytest
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

@pytest.fixture
def mySimulation():
    os.chdir(Path(sys.path[0]).joinpath("tests/test_data/keff_pulling/sf"))

    column_list = ['identity', \
                   'fiber1', 'pos1X', 'pos1Y', \
                   'fiber2', 'pos2X', 'pos2Y',\
                   'force']

    argv = ['--prefixframe', 'report', \
            '--suffixframe', '', \
            '--extframe', 'txt', \
            '--ifilesimulation', 'forces.dat', \
            '--ifilecolnames', 'forces.cols' ]
          
    return KeffData(argv=argv, column_list=column_list)

def test_calculate_motor_states(mySimulation):
    assert type(mySimulation.motor_df) == pd.DataFrame

    for entry in mySimulation.motor_df['time']:
        assert type(entry) == float
    
    for entry in mySimulation.motor_df['dir']:
        assert type(entry) == np.ndarray
        assert entry.shape == (2,)

    for entry in mySimulation.motor_df['force']:
        assert type(entry) == np.ndarray
        assert entry.shape == (2,)

    for entry in mySimulation.motor_df['length']:
        assert type(entry) == float

    for entry in mySimulation.motor_df['fil_id']:
        assert type(entry) == int
    
    for entry in mySimulation.motor_df['couple_id']:
        assert type(entry) == int

def test_calculate_k_eff(mySimulation):
    assert type(mySimulation.motor_df) == pd.DataFrame

    for entry in mySimulation.motor_df['f_net']:
        assert type(entry) == np.ndarray
        assert entry.shape == (2,)

    for entry in mySimulation.motor_df['f_net_mag']:
        assert type(entry) == float
    
    for entry in mySimulation.motor_df['n']:
        assert type(entry) == int
    
    for entry in mySimulation.motor_df['k_eff']:
        assert type(entry) == float

def test_write_output(mySimulation):
    pass
    # check that output file exists after writing