import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import sys
import argparse

class PThetaPlotter():
    def __init__(self, argv=sys.argv[1:]):
        self.cwd = Path.cwd()
        self.parser = argparse.ArgumentParser(description='')
        self.getArgs(argv)
        self.args = self.parser.parse_args(argv)

        self.theta_arr = np.loadtxt(self.args.thetafile)

        self.plotPTheta()

    def getArgs(self, argv):
        if argv != sys.argv[1:]:
            os.chdir(self.cwd)

        self.parser.add_argument('--time', type=float, help='')
        self.parser.add_argument('--thetafile', type=str, help='')
        self.parser.add_argument('--clustersize', type=int, help='')

    def plotPTheta(self):
        self.ofile = Path(self.args.thetafile).with_suffix("").with_suffix(".ptheta.png")
        N_pts = self.theta_arr.shape[0]
        title = r"t=%f s, $N_{\theta}=$%d, $N_{f}=$%d" % (self.args.time, N_pts, self.args.clustersize)
        plt.title(title)
        plt.hist(self.theta_arr, alpha=0.7, density=False, stacked=False)
        plt.ylim((0,300))
        plt.xlabel(r"$\theta$")
        plt.ylabel(r"$P(\theta)$")
        plt.savefig(self.ofile)

if __name__=="__main__":
    myPTP = PThetaPlotter()
   
    print(myPTP.ofile)
    del myPTP


