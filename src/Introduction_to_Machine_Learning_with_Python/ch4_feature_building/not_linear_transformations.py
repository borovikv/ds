import numpy as np
from sklearn.linear_model import Ridge
# from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor



from Introduction_to_Machine_Learning_with_Python.utils import score

rnd = np.random.RandomState(0)
X_org = rnd.normal(size=(1000, 3))
w = rnd.normal(size=3)
X = rnd.poisson(10 * np.exp(X_org))
y = np.dot(X_org, w)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
score(Ridge, X_train, X_test, y_train, y_test)
score(DecisionTreeRegressor, X_train, X_test, y_train, y_test)
score(KNeighborsRegressor, X_train, X_test, y_train, y_test)
score(MLPRegressor, X_train, X_test, y_train, y_test)

print('transformation')
print('-'*100)

X_train_log = np.log(X_train + 1)
X_test_log = np.log(X_test + 1)
score(Ridge, X_train_log, X_test_log, y_train, y_test)
score(KNeighborsRegressor, X_train_log, X_test_log, y_train, y_test)
score(MLPRegressor, X_train_log, X_test_log, y_train, y_test)


# plt.show()
