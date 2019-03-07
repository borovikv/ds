import numpy as np
import pandas as pd
from matplotlib import cm, pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv('hf3.csv')  # .sort_values(['f1', 'f2', 'f3'])

# print(df.head())
# threedee = plt.figure().gca(projection='3d')
# threedee.scatter(df.f1, df.f2, df.f3)
# plt.axis('equal')

fig = plt.figure()
ax = Axes3D(fig)
X = df.f1.values.reshape(-1, 1)
Y = df.f2.values.reshape(-1, 1)
Z = df.f3.values.reshape(-1, 1)
X, Y = np.meshgrid(X, Y)
# print(X )
ax.plot_surface(X, Y, Z) #, rstride=1, cstride=1) #, cmap=cm.coolwarm, linewidth=0, antialiased=False)

plt.show()
