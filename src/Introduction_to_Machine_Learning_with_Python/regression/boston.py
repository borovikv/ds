import mglearn
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split


def try_regression(method, X, y, **kwargs):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    r = method(**kwargs).fit(X_train, y_train)
    print(f"{method.__name__} Правильность на обучающем наборе: {r.score(X_train, y_train):.2f}")
    print(f"{method.__name__} Правильность на тестовом наборе: {r.score(X_test, y_test):.2f}")
    print(f"{method.__name__} Количество использованных признаков: {np.sum(r.coef_ != 0)} from {len(r.coef_)}")

    return r


X, y = mglearn.datasets.load_extended_boston()
# boston = load_boston()
# X, y = boston.data, boston.target

try_regression(LinearRegression, X, y)
try_regression(Ridge, X, y)
lasso = try_regression(Lasso, X, y, alpha=0.01, max_iter=100000)
