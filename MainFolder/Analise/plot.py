'''from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from doTheJob import *

fig = plt.figure()
ax = fig.gca(projection='3d')

#x = [1,2,3]
#y = [1,4,9]
#z = [3,6,9]

result=doTheJob(politics=1,lambda_init=1,lambda_end=1000,lambda_step=100,mi_init=1,mi_end=1000,mi_step=100,iterations=1000)

x=result[0]
y=result[1]
z=result[24]
w=result[41]


ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
#ax.plot_trisurf(x, y, z, cmap=plt.colors() , linewidth=0.2)

ax.plot_trisurf(x, y, w, linewidth=0.2)


plt.show()'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

x1 = [1,2,3]
x2 = [4,8,12]
x3 = [10, 20, 30]

X1, X2 = np.meshgrid(x1, x2)

X3 = []
for i in range(len(x1)):
    X3.append(x3)

fig = plt.figure()
ax = Axes3D(fig)

ax.plot_surface(X1, X2, X3, cmap='Set1', edgecolor='w', alpha=0.5)

plt.show()
