import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats

n_trj = 32
window_fraction = 0.1
start_pt_fraction = window_fraction/5

trj_list = []

for trj_idx in range(n_trj):
    slope_list = []

    fname = "trj" + str(trj_idx) + "/f0/rad_gyr.dat"
    rad_gyr_arr = np.loadtxt(fname, usecols=(1,4))

    num_pts = rad_gyr_arr.shape[0]

    window_size = int(window_fraction * num_pts)
    start_pt = int(start_pt_fraction * num_pts)

    end_of_window = num_pts - window_size - start_pt - 1

    for start_idx in range(start_pt, num_pts-window_size-start_pt-1, window_size):
        end_idx = start_idx + window_size

        t = rad_gyr_arr[start_idx:end_idx,0]
        rg = rad_gyr_arr[start_idx:end_idx,1]

        lin_reg = sp.stats.linregress(t, rg)


        slope_list.append([t[0], lin_reg.slope, lin_reg.stderr])

    trj_list.append(slope_list)

trj_arr = np.array(trj_list)

#fig, ax = plt.subplots()

for idx in range(trj_arr.shape[0]):
    trj_data = trj_arr[idx,:,:]

    plt.errorbar(trj_data[:,0], trj_data[:,1],trj_data[:,2])
    plt.show()

#ax.errorbar(np.mean(trj_arr, axis=0)[:,0], np.mean(trj_arr, axis=0)[:,1], np.sum(trj_arr, axis=0)[:,2])

#plt.show()
