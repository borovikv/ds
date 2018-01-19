import matplotlib.pyplot as plt
import mglearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

from Introduction_to_Machine_Learning_with_Python.utils import curry


def make_wave():
    X, y = mglearn.datasets.make_wave(n_samples=40)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    plt.plot(X_train, y_train, 'o')
    plt.plot(X_test, y_test, 's')
    plt.ylim(-3, 3)
    plt.xlabel("Признак")
    plt.ylabel("Целевая переменная")

    score = curry(X_train, X_test, y_train, y_test)

    prediction = score(KNeighborsRegressor, n_neighbors=3).predict(X_test)
    plt.plot(X_test, prediction, '*')

    prediction = score(LinearRegression).predict(X_test)
    plt.plot(X_test, prediction, '+')


def test_test_neighbors_settings(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    score = curry(X_train, X_test, y_train, y_test)
    scores = [score(KNeighborsRegressor, n_neighbors=i).score(X_test, y_test) for i in range(1, 11)]
    plt.plot(range(1, 11), scores)


# make_wave()
test_test_neighbors_settings(*mglearn.datasets.make_wave(n_samples=40))
plt.show()
