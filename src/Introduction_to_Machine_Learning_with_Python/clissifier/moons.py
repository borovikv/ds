from functools import partial

import mglearn
from matplotlib import pyplot as plt
from sklearn.datasets import make_moons
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from Introduction_to_Machine_Learning_with_Python.utils import score, scale_std


def moons():
    X, y = make_moons(n_samples=100, noise=0.25, random_state=3)

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)
    forest = score(
        RandomForestClassifier, X_train, X_test, y_train, y_test, plot=False, n_estimators=5, random_state=2)
    # plot(forest, X_train, y_train)

    mlp_classifier1 = partial(score, MLPClassifier, X_train, X_test, y_train, y_test, plot=False, random_state=0)

    X_train_scaled, X_test_scaled = scale_std(X_train, X_test)
    mlp_classifier2 = partial(score, MLPClassifier, X_train_scaled, X_test_scaled, y_train, y_test, plot=False, random_state=0)

    kwargs = [
        {'solver': 'lbfgs'},
        {'solver': 'lbfgs', 'hidden_layer_sizes': [10]},
        {'solver': 'lbfgs', 'hidden_layer_sizes': [100, 10]},
        {'solver': 'lbfgs', 'hidden_layer_sizes': [100, 10], 'alpha': 0.01},
        {'solver': 'lbfgs', 'hidden_layer_sizes': [100, 5]},
        {'solver': 'lbfgs', 'hidden_layer_sizes': [100, 5], 'alpha': 0.01},
    ]
    for kw in kwargs:
        mlp = mlp_classifier1(**kw)
        print('scaled')
        mlp = mlp_classifier2(**kw)
        # plot_mlp(mlp, X_train, y_train)



def plot(forest, X_train, y_train):
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))
    for i, (ax, tree) in enumerate(zip(axes.ravel(), forest.estimators_)):
        ax.set_title(f'Дерево {i}')
        mglearn.plots.plot_tree_partition(X_train, y_train, tree, ax=ax)
    mglearn.plots.plot_2d_separator(forest, X_train, fill=True, ax=axes[-1, -1], alpha=.4)
    axes[-1, -1].set_title('Случайный лес')
    mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)


def plot_mlp(mlp, X_train, y_train):
    mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=.3)
    mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)
    plt.xlabel("Признак 0")
    plt.ylabel("Признак 1")


moons()
plt.show()
