from simulation_class import Simulation
from data_class import Data
from k_eff_pulling import KeffData

import pytest
import os
import sys
from pathlib import Path
import numpy as np

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
    assert type(mySimulation.motor_data_list) == list

    for frame in mySimulation.motor_data_list:
        assert type(frame) == dict
        assert type(frame['time']) == float
        assert type(frame['couple_data']) == list

        for couple in frame['couple_data']:
            assert type(couple) == dict

            assert type(couple['dir']) == np.ndarray
            assert couple['dir'].shape == (2,)

            assert type(couple['force']) == np.ndarray
            assert couple['force'].shape == (2,)

            assert type(couple['length']) == float
            assert type(couple['fil_id']) == int
    
    
        