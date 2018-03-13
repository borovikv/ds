from matplotlib import pyplot as plt
from mglearn.make_blobs import make_blobs
from sklearn.cluster import DBSCAN
X, y = make_blobs(random_state=0, n_samples=120)
cluster = DBSCAN().fit_predict(X)
plt.show()
