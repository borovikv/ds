import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE, SelectFromModel, SelectPercentile
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree.tree import DecisionTreeClassifier

from Introduction_to_Machine_Learning_with_Python.utils import score

fig, axes = plt.subplots(3, 1, figsize=(10, 3))
counter = 0


def draw_selected_indexes(selected):
    print('draw')
    global counter
    mask = selected.get_support()
    axes[counter].matshow(mask.reshape(1, -1), cmap='gray_r')
    axes[counter].set_xlabel("Индекс примера")
    counter += 1


def transform(select, *data):
    return [select.transform(d) for d in data]


cancer = load_breast_cancer()
rng = np.random.RandomState(42)
noise = rng.normal(size=(len(cancer.data), 50))
X_w_noise = np.hstack([cancer.data, noise])
X_train, X_test, y_train, y_test = train_test_split(X_w_noise, cancer.target, random_state=0, test_size=.5)
print("форма массива X_train: {}".format(X_train.shape))

print('одномерные статистики (univariate statistics)')
select = SelectPercentile(percentile=50)
select.fit(X_train, y_train)
draw_selected_indexes(select)
X_train_selected, X_test_selected = transform(select, X_train, X_test)
print("форма массива X_train_selected: {}".format(X_train_selected.shape))

print('отбор на основе модели (model-based selection)')
select = SelectFromModel(RandomForestClassifier(n_estimators=100, random_state=42), threshold="median")
select.fit(X_train, y_train)
draw_selected_indexes(select)
X_train_l1 = select.transform(X_train)
X_test_l1 = select.transform(X_test)
print("форма массива X_train_l1: {}".format(X_train_l1.shape))

print('итеративный отбор (iterative selection)', 'recursive feature elimination, RFE')
select = RFE(RandomForestClassifier(n_estimators=100, random_state=42), n_features_to_select=40)
select.fit(X_train, y_train)
draw_selected_indexes(select)
X_train_rfe, X_test_rfe = transform(select, X_train, X_test)
print("форма массива X_train_rfe: {}".format(X_train_rfe.shape))


methods = [LogisticRegression, DecisionTreeClassifier]
data = {
    'origin': [X_train, X_test],
    'selected': [X_train_selected, X_test_selected],
    'l1': [X_train_l1, X_test_l1],
    'l2': [X_train_rfe, X_test_rfe]
}
for m in methods:
    for label, (x_tr, x_tst) in data.items():
        print(label)
        score(m, x_tr, x_tst, y_train, y_test)

plt.show()
