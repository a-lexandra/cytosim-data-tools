import sys
import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

# code from https://stackoverflow.com/a/61733206

ifile = sys.argv[1]

n_seg = int(sys.argv[2])

data = np.loadtxt(ifile)

n_data = data.shape[0]

fig, (ax0, ax1) = plt.subplots(1,2)

x = data[:,0]
y = data[:,1]

dy = np.gradient(y, x)

rgr = DecisionTreeRegressor(max_leaf_nodes=n_seg)
rgr.fit(x.reshape(-1,1), dy.reshape(-1,1))
dy_dt = rgr.predict(x.reshape(-1,1)).flatten()

#breakpoint()

y_sl = np.ones(len(x)) * np.nan

for yval in np.unique(dy_dt):
    msk = dy_dt == yval

    lin_reg = LinearRegression()
    lin_reg.fit(x[msk].reshape(-1,1), y[msk].reshape(-1,1))
    y_sl[msk] = lin_reg.predict(x[msk].reshape(-1,1)).flatten()

    ax0.plot([x[msk][0], x[msk][-1]], 
             [y[msk][0], y[msk][-1]],
             color='r', zorder=1)

ax0.scatter(x, y, label='data')
ax0.scatter(x, y_sl, s=3**2, label='seg lin reg', color='g', zorder=5)
ax0.legend()

ax1.scatter(x, y, label='data')

ax2 = ax1.twinx()
ax2.scatter(x, dy_dt, label='DecisionTree', s=2**2, color='g')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax2.legend(lines1 + lines2, labels1 + labels2, loc=0)

plt.show()
