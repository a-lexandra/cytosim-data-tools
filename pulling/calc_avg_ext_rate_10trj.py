import numpy as np
import matplotlib.pyplot as plt

data_list = []

num_trj = 64

for trj_idx in range(num_trj):
    fname = "trj" + str(trj_idx) + "/release/contraction_rate.txt"

    data_list.append(np.loadtxt(fname))

data_arr = np.array(data_list)

fig, ax = plt.subplots()

ax.axhline(0,color="green",linestyle="--")

t = data_arr[0,:,0]
y = data_arr[:,:,1].mean(axis=0)
s = data_arr[:,:,1].std(axis=0)

ax.plot(t, y)
ax.fill_between(t, y-s, y+s, alpha=0.2)

#plt.errorbar(data_arr[0,:,0], data_arr[:,:,1].mean(axis=0), yerr=data_arr[:,:,1].std(axis=0))
#plt.xlabel("t")
plt.xlim(left=109.9,right=110.5)

plt.yticks(fontsize=16)
plt.xticks(fontsize=16)

fig.canvas.draw()
ax.xaxis.set_major_locator(plt.MaxNLocator(6))
ax.yaxis.set_major_locator(plt.MaxNLocator(6))
#plt.ylabel("contraction rate (um/s)")
plt.savefig(f"contraction_avg_{num_trj}trj.png")

