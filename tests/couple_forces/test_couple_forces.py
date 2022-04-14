import pytest

import argparse
from pathlib import Path
import pandas as pd
import os
import numpy as np
import sys

from couple_forces.couple_forces import get_args, process_file

def test_get_args():
    args = get_args(['--ifile', 'input_filename', \
                     '--ofile', 'output_filename', \
                     '--largest'])

    assert type(args.ifile) == str
    assert type(args.ofile) == str
    assert type(args.largest) == bool

def test_process_file():
    args = get_args(['--ifile', 'couple_forces/link_cluster.txt', \
                     '--largest'])

    process_file(args)
