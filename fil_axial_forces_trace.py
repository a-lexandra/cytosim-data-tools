import sys
import argparse
from pathlib import Path
import numpy as np

def main(argv):
    parser = argparse.ArgumentParser(description='')
    self.parser.add_argument('--ifile', '-i', type=str, help='')
	self.args = self.parser.parse_args(argv)

    input_file_name=self.args.ifile
    input_file_path  = Path(input_file_name)
	
    frame_idx = 0

    with open(input_file_path, "r") as ifile:
        pass

if __name__=="__main__":
    main(sys.argv[1:])
