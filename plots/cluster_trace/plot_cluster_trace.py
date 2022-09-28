import numpy as np
import matplotlib.pyplot as plt

clust_dict = {}
time = 0
frame_count = 0
first_cluster_flag = True

with open("clusters.txt", "r") as f:
   for line in f:
       if "time" in line:
           time = float(line.strip().split()[-1])
       elif (not "%" in line) and (not "clusters:" in line) and (not line.isspace()) and (first_cluster_flag):
           _,_,clust_id = line.strip().partition(":")
           clust_dict[time] = np.array(clust_id.split(), dtype=int)
           first_cluster_flag = False
       elif "% end" in line:
           frame_count += 1
           first_cluster_flag = True

keys = list(clust_dict.keys())
start_time = keys[0]
end_time = keys[-1]
dt = keys[1] - keys[0]

pixel_list = []

for time in clust_dict:
    time_slice_list = []
    for idx in range(1,100+1):
        if idx in clust_dict[time]:
            time_slice_list.append(0)
        else:
            time_slice_list.append(1)
    pixel_list.append(np.array(time_slice_list))

pixel_arr = np.array(pixel_list).T

fig, ax = plt.subplots()

time_ticks = np.arange(start_time, end_time + dt, dt)
fil_id_ticks = np.arange(1, 100+1, 1)

num_time_labels = 10
step_time = int(time_ticks.shape[0] / (num_time_labels - 1))

time_ticks_positions = np.arange(0, time_ticks.shape[0], step_time)

time_ticks_int = [ int(x) for x in time_ticks[::step_time] ] 

#plt.xticks(time_ticks_positions, time_ticks_int)

plt.imshow(pixel_arr, cmap="binary", origin='lower', interpolation="none", extent=[start_time, end_time, 1, 100])

plt.xlabel("time")
plt.ylabel("fil id")

plt.savefig("cluster_trace.png", dpi=300, bbox_inches="tight")

# plt.quiver(x,y,u,v,scale=)
