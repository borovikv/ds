from mglearn.make_blobs import make_blobs
from scipy.cluster.hierarchy import dendrogram, ward
from matplotlib import pyplot as plt

X, y = make_blobs(random_state=0, n_samples=120)
linkage_array = ward(X)
dendrogram(linkage_array)
ax = plt.gca()
bounds = ax.get_xbound()
ax.plot(bounds, [7.25, 7.25], '--', c='k')
ax.plot(bounds, [4, 4], '--', c='k')
ax.text(bounds[1], 7.25, 'два кластера', va='center', fontdict={'size': 15})
ax.text(bounds[1], 4, 'три кластера', va='center', fontdict={'size': 15})
plt.xlabel("Индекс наблюдения")
plt.ylabel("Кластерное  расстояние")
plt.show()