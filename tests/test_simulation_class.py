from simulation_class import Simulation
import argparse
import pytest
import os
import sys
import re

def test_init():
    mySimulation = Simulation(argv=['--prefixframe', 'report', \
                                    '--suffixframe', '', \
                                    '--extframe', 'txt', \
                                    '--ifilesimulation', 'forces.dat' \
                                    ])

def test_get_args():
    mySimulation = Simulation(argv=['--prefixframe', 'report', \
                                    '--suffixframe', 'frame', \
                                    '--extframe', '.txt', \
                                    '--ifilesimulation', 'forces.dat' \
                                    ])

    assert type(mySimulation.args.prefixframe) == str
    assert mySimulation.args.prefixframe.isalpha()
    
    assert type(mySimulation.args.suffixframe) == str
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
    m = re.search(r'^[A-Za-z0-9]+\.[A-Za-z0-9]+$', mySimulation.args.ifilesimulation)
    assert m 

def test_get_frame_filename_pattern():
    mySimulation = Simulation(argv=['--prefixframe', 'report', \
                                    '--suffixframe', '', \
                                    '--extframe', '.txt', \
                                    '--ifilesimulation', 'forces.dat' \
                                    ])


    pass

def test_load_simulation_data():
    pass

def test_get_frame_filepaths():
    os.chdir(sys.path[0])
    pass

def test_load_frame_data():
    pass

def test_process_frame_data():
    pass