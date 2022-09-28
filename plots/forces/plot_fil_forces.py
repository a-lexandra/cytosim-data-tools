import numpy as np
import matplotlib.pyplot as plt

fil_dict = {}
fil_list = []
fil_count = 0

with open("force.txt", "r") as f:
   for line in f:
       if "%" in line:
           if "fiber f" in line:
               if fil_count > 0:
                   fil_dict[fil_count] = np.asarray(fil_list, dtype=float)
                   fil_list = []
               fil_count += 1
       else:
           if len(line.strip().split())>0:
               fil_list.append(line.strip().split())

fig, ax = plt.subplots()

force_mag_list = []

for fil_id in fil_dict:
    for seg in fil_dict[fil_id]:
        force_mag_list.append(abs(seg[-1]))

max_force = max(np.array(force_mag_list))

for fil_id in fil_dict:
    #plt.plot(fil_dict[fil_id][:,1], fil_dict[fil_id][:,2])

    for seg in fil_dict[fil_id]:
        if (np.sqrt(seg[3]**2 + seg[4]**2)>0) and seg[5]>0:
            plt.quiver(seg[1], seg[2], seg[3], seg[4], scale=np.float64(1/seg[5])*0.01, scale_units="xy", alpha=abs(seg[5])/max_force)

#plt.plot(fil_dict[1][:,1], fil_dict[1][:,2])


ax.set_aspect('equal')

plt.xlim(-3.5,3.5)
plt.ylim(-3.5,3.5)

plt.savefig("forces.png", dpi=150, bbox_inches="tight")

# plt.quiver(x,y,u,v,scale=)
