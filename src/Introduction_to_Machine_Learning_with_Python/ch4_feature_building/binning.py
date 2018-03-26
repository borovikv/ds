import mglearn
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder

X, y = mglearn.datasets.make_wave(n_samples=100)
plt.plot(X[:, 0], y, 'o', c='k')
line = np.linspace(-3, 3, 1000, endpoint=False).reshape(-1, 1)

reg = DecisionTreeRegressor(min_samples_split=3).fit(X, y)
plt.plot(line, reg.predict(line), label="дерево решений")

reg = LinearRegression().fit(X, y)
plt.plot(line, reg.predict(line), label="линейная регрессия")

bins = np.linspace(-3, 3, 11)
print(bins)
which_bin = np.digitize(X, bins=bins)

encoder = OneHotEncoder(sparse=False).fit(which_bin)
X_binned = encoder.transform(which_bin)
line_binned = encoder.transform(np.digitize(line, bins=bins))


# import pandas as pd
# df = pd.DataFrame(which_bin).applymap(str)
# d = pd.get_dummies(df)

reg = DecisionTreeRegressor(min_samples_split=3).fit(X_binned, y)
plt.plot(line, reg.predict(line_binned), label="дерево решений X_binned")

reg = LinearRegression().fit(X_binned, y)
plt.plot(line, reg.predict(line_binned), label="линейная регрессия X_binned")


plt.vlines(bins, -3, 3, linewidth=1, alpha=.2)
plt.ylabel("Выход регрессии")
plt.xlabel("Входной признак")
plt.legend(loc="best")
plt.show()