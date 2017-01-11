from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

x = [1,2,3]
y = [1,4,9]
z = [3,6,9]

ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)

plt.show()
