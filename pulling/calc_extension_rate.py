
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

start_from_head_bool = True


rad_gyr_arr = np.loadtxt('rad_gyr.dat', usecols=(1,4))

num_pts = rad_gyr_arr.shape[0]

rsq_list = []

# linear relaxation - not always not true
if start_from_head_bool:
    for idx in range(50,num_pts):
        t = rad_gyr_arr[0:idx,0]
        rg = rad_gyr_arr[0:idx,1]

        p = sp.stats.linregress(t, rg)

        rsq_list.append([t[-1],p.rvalue**2])
else:
    for idx in range(0,num_pts-50):
        t = rad_gyr_arr[idx:-1,0]
        rg = rad_gyr_arr[idx:-1,1]

        p = sp.stats.linregress(t,rg)

        rsq_list.append([t[0], p.rvalue**2])


t = rad_gyr_arr[:,0]
rg = rad_gyr_arr[:,1]

rsq_arr = np.array(rsq_list)

peak_idx = np.argmax(rsq_arr[:,1])
peak_t   = rsq_arr[peak_idx, 0]
peak_rsq = rsq_arr[peak_idx, 1]

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.scatter(t, rg)
ax2.plot(rsq_arr[:,0], rsq_arr[:,1],color='red')
ax1.axvline(peak_t,color='green')
plt.show()



print(peak_idx, peak_t, peak_rsq)