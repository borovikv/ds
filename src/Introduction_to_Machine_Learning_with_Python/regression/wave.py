import matplotlib.pyplot as plt
import mglearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


def make_wave():
    X, y = mglearn.datasets.make_wave(n_samples=40)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    plt.plot(X_train, y_train, 'o')
    plt.plot(X_test, y_test, 's')
    plt.ylim(-3, 3)
    plt.xlabel("Признак")
    plt.ylabel("Целевая переменная")

    prediction, _ = predict(KNeighborsRegressor, X_train, X_test, y_train, y_test, n_neighbors=3)
    plt.plot(X_test, prediction, 'v')

    prediction, _ = predict(LinearRegression, X_train, X_test, y_train, y_test)
    plt.plot(X_test, prediction, '+')


def predict(method, X_train, X_test, y_train, y_test, **kwargs):
    reg = method(**kwargs).fit(X_train, y_train)
    print(f"{method.__name__} Правильность на обучающем наборе: {reg.score(X_train, y_train):.2f}")
    print(f"{method.__name__} Правильность на тестовом наборе: {reg.score(X_test, y_test):.2f}")
    return reg.predict(X_test), reg.score(X_test, y_test)


def test_test_neighbors_settings(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    scores = [predict(KNeighborsRegressor, X_train, X_test, y_train, y_test, n_neighbors=i)[1] for i in range(1, 11)]
    plt.plot(range(1, 11), scores)


make_wave()
# test_test_neighbors_settings(*mglearn.datasets.make_wave(n_samples=40))
plt.show()
