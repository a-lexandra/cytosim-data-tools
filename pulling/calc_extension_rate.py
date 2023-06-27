
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats

rad_gyr_arr = np.loadtxt('rad_gyr.dat', usecols=(1,4))

num_pts = rad_gyr_arr.shape[0]

window_size = 50

slope_list = []

for start_idx in range(num_pts-window_size):
    end_idx = start_idx + window_size
    t = rad_gyr_arr[start_idx:end_idx,0]
    rg = rad_gyr_arr[start_idx:end_idx,1]

    p = sp.stats.linregress(t, rg)

    slope_list.append([t[0],p.slope])


t = rad_gyr_arr[:,0]
rg = rad_gyr_arr[:,1]

slope_arr = np.array(slope_list)

zero_idx = np.argmax(slope_arr[:,1]>0)
zero_t   = slope_arr[zero_idx, 0]

relax_time = zero_t - slope_arr[0,0]

with open('relax_time.txt', 'w') as f:
    f.write(str(relax_time)+'\n')

plot_bool = False

if plot_bool:

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.set_xlabel("time (s)")
    ax1.scatter(t, rg)
    ax1.set_ylabel("R_g")
    ax2.scatter(slope_arr[:,0], slope_arr[:,1],color='red')
    ax2.set_ylabel("linear fit slope")
    ax2.axhline(0,color='green')
    ax2.axvline(zero_t,color='green')
    plt.show()
