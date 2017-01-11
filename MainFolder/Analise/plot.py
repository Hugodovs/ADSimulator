from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from doTheJob import *

fig = plt.figure()
ax = fig.gca(projection='3d')

#x = [1,2,3]
#y = [1,4,9]
#z = [3,6,9]

result=doTheJob(politics=3,lambda_init=1,lambda_end=1000,lambda_step=100,mi_init=1,mi_end=1000,mi_step=100,iterations=1000)

x=result[0]
y=result[1]
z=result[18]
w=result[42]


ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
#ax.plot_trisurf(x, y, z, cmap=plt.colors() , linewidth=0.2)

ax.plot_trisurf(x, y, w, linewidth=0.2)


plt.show()
