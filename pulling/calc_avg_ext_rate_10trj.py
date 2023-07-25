import numpy as np
import matplotlib.pyplot as plt

data_list = []

for trj_idx in range(10):
    fname = "trj" + str(trj_idx) + "/release/contraction_rate.txt"

    data_list.append(np.loadtxt(fname))

data_arr = np.array(data_list)
plt.axhline(0,color="green",linestyle="--")
plt.errorbar(data_arr[0,:,0], data_arr[:,:,1].mean(axis=0), yerr=data_arr[:,:,1].std(axis=0))
plt.xlabel("t")
plt.xlim(right=110.5)

plt.ylabel("contraction rate (um/s)")
plt.savefig("contraction_avg_10trj.png")

