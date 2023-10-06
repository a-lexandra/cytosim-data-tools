import numpy as np
import matplotlib.pyplot as plt

n_trj = 50
time_avg = 10 #s

dt = 0.1
n_step_avg = int(time_avg // dt)

Rg_list = []

for i in range(n_trj):
    filename = "trj" + str(i) + "/sf/rad_gyr.dat"

    data = np.loadtxt(filename, usecols=(1,4))

    tail_data = data[n_step_avg:,1]

    mean = np.mean(tail_data)

    Rg_list.append(mean)

bundle_Rg_list = [ rg for rg in Rg_list if rg > 0.125 ] 

print(len(bundle_Rg_list)/n_trj)
