from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from doTheJob import *

fig = plt.figure()
ax = fig.gca(projection='3d')


result=doTheJob(politics=1,lambda_init=3,lambda_end=10,lambda_step=1,mi_init=1,mi_end=10,mi_step=1,iterations=1000)

x=result[0]
y=result[1]
z=result[36]
w=result[49]


plt.xlabel('lambda')
plt.ylabel('mi')

plt.title('E[U]')


ax.plot_trisurf(x, y, z, color='blue', linewidth=0.2)  #numerico
ax.plot_trisurf(x, y, w, color='red' , linewidth=0.2,alpha=0.5)  #analitico


plt.show()
