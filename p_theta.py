from data_class import Data
import sys
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

class PTheta(Data):
    def __init__(self, column_list=['identity']):
        super().__init__(column_list=column_list)
        
        self.cluster_size = self.getClusterSize()


    def doCalculations(self):
        self.theta_arr = self.calculateTheta()
        self.p_theta, self.p_theta_bins = self.calculatePTheta()

    def getClusterSize(self):
        fil_id_list = []

        print(self.temp_dataframe)

        for fil_id, df_fil in self.temp_dataframe.groupby('fiber1'):
            fil_id_list.append(fil_id)

        for fil_id, df_fil in self.temp_dataframe.groupby('fiber2'):
            fil_id_list.append(fil_id)

        fil_id_arr = np.array(fil_id_list)

        unique_fil_id_arr = np.unique(fil_id_arr)
        

        num_fils = unique_fil_id_arr.shape[0]

        return num_fils


    def calculateTheta(self):
        cos_theta_arr = self.temp_dataframe['cos_angle'].values

        theta_arr = np.arctan2(np.sqrt(1-cos_theta_arr**2), cos_theta_arr)

        return theta_arr

    def calculatePTheta(self):
        hist, bins = np.histogram(self.theta_arr)

        bin_centers = (bins[1:] + bins[:-1])/2

        return (hist, bin_centers)

    def writeTheta(self):
        ofile = Path(self.args.ifile).with_suffix(".theta.dat")
        np.savetxt(ofile, self.theta_arr, delimiter="\t", fmt='%.8f')

    def writePTheta(self):
        ofile = Path(self.args.ifile).with_suffix(".ptheta.dat")
        output_arr = np.column_stack((self.p_theta_bins,self.p_theta))
        np.savetxt(ofile, output_arr, delimiter="\t", fmt='%.8f')

    def plotPTheta(self):
        ofile = Path(self.args.ifile).with_suffix(".ptheta.png")
        N_pts = self.theta_arr.shape[0]
        title = r"t=%f s, $N_{\theta}=$%d, $N_{f}=$%d" % (self.time, N_pts, self.cluster_size)
        plt.title(title)
        plt.hist(self.theta_arr, alpha=0.7, density=False, stacked=False)
        plt.ylim((0,300))
        plt.xlabel(r"$\theta$")
        plt.ylabel(r"$P(\theta)$")
        plt.savefig(ofile)

if __name__=="__main__":

    column_list = [ 'cluster', 'cos_angle', 'fiber1', 'fiber2' ]

    myPTheta = PTheta(column_list)

    myPTheta.doCalculations()
    myPTheta.writeTheta()
    myPTheta.writePTheta()
    myPTheta.plotPTheta()

    del myPTheta
