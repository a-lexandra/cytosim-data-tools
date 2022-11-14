import numpy as np
import matplotlib.pyplot as plt

time = 0
frame_count = 0
force_dict = {}

with open("couple_links.txt", "r") as f:
    for line in f:
        if "time" in line:
            time = float(line.strip().split()[-1])
            force_list = []
        elif (not "%" in line) and (not line.isspace()):
            force_list.append(line.strip().split()[-2])
        elif "% end" in line:
            force_dict[time] = np.array(force_list, dtype=float)
            frame_count += 1

avg_force_dict = {}
avg_force_list = []

keys = list(force_dict.keys())
start_time = keys[0]
end_time = keys[-1]
dt = keys[1] - keys[0]

for time in force_dict:
    force_avg = np.mean(force_dict[time])
    force_std = np.std(force_dict[time])
    avg_force_list.append([time, force_avg, force_std])

avg_force_arr = np.array(avg_force_list, dtype=float)
np.savetxt("avg_force.dat", avg_force_arr, fmt="%.8f", delimiter=" ")

plt.errorbar(avg_force_arr[:,0], avg_force_arr[:,1], yerr=avg_force_arr[:,2])

plt.xlabel("time")
plt.ylabel("<f>_t")

plt.savefig("avg_force.png", dpi=150, bbox_inches="tight")

