from itertools import combinations

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.svm import SVC
import numpy as np
from sklearn.model_selection import GridSearchCV
iris = load_iris()
logreg = LogisticRegression()
scores = cross_val_score(logreg, iris.data, iris.target, cv=5)
print(list(scores))

# Решетчатый поиск
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=0)

gamma_c_params = list(combinations([0.001, 0.01, 0.1, 1, 10, 100], 2))


def to_score(gamma, c):
    svm = SVC(gamma=gamma, C=c)
    return np.mean(cross_val_score(svm, X_train, y_train, cv=5))


print('-'* 100)
scores = {(g, c): to_score(g, c) for g, c in gamma_c_params}
max_value = max(scores.values())
max_keys = list(filter(lambda params: scores[params] == max_value, scores))
print(max_value, max_keys)

print('-'* 100)
df = pd.DataFrame({'gamma_c': gamma_c_params, 'score': [to_score(g, c) for g, c in gamma_c_params]})
max_df = df[df.score == df.score.max()]
print(max_df)

print('-'* 100)
param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 1, 10, 100]}
grid_search = GridSearchCV(SVC(), param_grid, cv=5)
grid_search.fit(X_train, y_train)
print(grid_search.best_estimator_)
print(grid_search.best_params_)
print(grid_search.best_score_)


print('-'* 100)
scores = cross_val_score(GridSearchCV(SVC(), param_grid, cv=5), iris.data, iris.target, cv=5)
print(scores)
print(scores.mean())
