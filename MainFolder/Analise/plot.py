from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
from doTheJob import *

fig = plt.figure()
ax = fig.gca(projection='3d')


result=doTheJob(politics=1,lambda_init=1,lambda_end=10,lambda_step=1,mi_init=1,mi_end=10,mi_step=1,iterations=1000)

x=result[0]
y=result[1]
z=result[36]
w=result[49]

#z_linha=[]
z_linha=z

'''for item in z:
    var=np.random.randint(0,2)
    if var==1:
        z_linha.append(item+np.random.random_sample()/400)
    else:
        z_linha.append(item-np.random.random_sample()/400)'''

plt.xlabel('lambda')
plt.ylabel('mi')

plt.title('E[B]')


ax.plot_trisurf(x, y, z_linha, color='blue', linewidth=0.2)  #numerico
ax.plot_trisurf(x, y, w, color='red' , linewidth=0.2,alpha=0.5)  #analitico


plt.show()

'''import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from doTheJob import *

result=doTheJob(politics=1,lambda_init=1,lambda_end=1000,lambda_step=100,mi_init=1,mi_end=1000,mi_step=100,iterations=1000)

x1=result[0]
x2=result[1]
x3=result[24]
x4=result[41]

X1, X2 = np.meshgrid(x1, x2)

X3 = []
for i in range(len(x1)):
    X3.append(x3)

X4 = []
for i in range(len(x1)):
    X4.append(x4)

fig = plt.figure()
ax = Axes3D(fig)

ax.plot_surface(X1, X2, X3, cmap='plasma', edgecolor='w', alpha=0.5)
#ax.plot_surface(X1, X2, X4, cmap='Set1', edgecolor='w', alpha=0.5)

plt.show()'''
