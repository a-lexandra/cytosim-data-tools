from simulation_class import Simulation
from data_class import Data
import argparse
import pytest
import os
import sys
import re
import pathlib
from pathlib import Path

@pytest.fixture
def mySimulation():
    return Simulation(argv=['--prefixframe', 'report', \
                            '--suffixframe', 'fr', \
                            '--extframe', 'txt', \
                            '--ifilesimulation', 'forces.dat', \
                            '--ifilecolnames', 'forces.cols' \
                            ])

def test_get_args(mySimulation):
    assert type(mySimulation.args.prefixframe) == str
    
    if len(mySimulation.args.prefixframe) > 0:
        assert mySimulation.args.prefixframe.isalpha()
    
    assert type(mySimulation.args.suffixframe) == str
    
    if len(mySimulation.args.suffixframe)> 0:
        assert mySimulation.args.suffixframe.isalpha()

    # Either prefix or suffix string len must be nonzero
    assert (len(mySimulation.args.prefixframe) > 0 or 
            len(mySimulation.args.suffixframe) > 0 )

    assert type(mySimulation.args.extframe) == str
    
    # check presence of leading . and length
    dot_count = mySimulation.args.extframe.count('.')
    assert (dot_count == 0) or (dot_count == 1)

    leading_dot_idx = mySimulation.args.extframe.find('.')

    assert (leading_dot_idx == 0) or (leading_dot_idx == -1)

    if leading_dot_idx == 0: 
        assert len(mySimulation.args.extframe) > 1
    elif leading_dot_idx == -1:
        assert len(mySimulation.args.extframe) > 0
        assert mySimulation.args.extframe.isalpha()

    assert type(mySimulation.args.ifilesimulation) == str
    assert len(mySimulation.args.ifilesimulation) > 0

    # Check valid format of filename
    # Use raw string for regex search
    m_fname_sim = re.search(r'^[A-Za-z0-9]+\.[A-Za-z0-9]+$', mySimulation.args.ifilesimulation)
    assert m_fname_sim

    assert type(mySimulation.args.ifilecolnames) == str
    
    if len(mySimulation.args.ifilecolnames) > 0:
        m_fname_cols = re.search(r'^[A-Za-z0-9]+\.[A-Za-z0-9]+$', mySimulation.args.ifilecolnames)
        assert m_fname_cols

@pytest.fixture
def mySimulation():
    os.chdir(Path(sys.path[0]).joinpath("tests/test_data/keff_pulling/sf"))

    return Simulation(argv=['--prefixframe', 'report', \
                            '--suffixframe', '', \
                            '--extframe', 'txt', \
                            '--ifilesimulation', 'forces.dat', \
                            '--ifilecolnames', 'forces.cols' \
                            ])

def test_get_frame_filename_pattern(mySimulation):
    assert re.compile(mySimulation.frame_fname_search_pattern)

def test_load_simulation_data(mySimulation):
    os.chdir(Path(sys.path[0]).joinpath("tests/test_data/keff_pulling/sf"))

    # breakpoint()
    if len(mySimulation.args.ifilecolnames) > 0:
        assert os.path.isfile(mySimulation.simulation_file_path)
        assert os.stat(mySimulation.simulation_file_path).st_size > 0
    

def test_get_frame_filepaths(mySimulation):
    os.chdir(Path(sys.path[0]).joinpath("tests/test_data/keff_pulling/sf/"))

    assert len(mySimulation.frame_filepath_list) > 0

    for path in mySimulation.frame_filepath_list:
        assert type(path) == pathlib.PosixPath
        assert os.path.isfile(path)
        assert os.stat(path).st_size > 0

def test_load_frame_data(mySimulation):
    os.chdir(Path(sys.path[0]).joinpath("tests/test_data/keff_pulling/sf/"))

    assert type(mySimulation.frame_data_list) == list

    for frame in mySimulation.frame_data_list:
        assert type(frame) == Data

    assert len(mySimulation.frame_data_list) == len(mySimulation.frame_filepath_list)