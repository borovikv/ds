from functools import partial

import numpy as np
import pydotplus
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree.export import export_graphviz
from sklearn.tree.tree import DecisionTreeClassifier

import Introduction_to_Machine_Learning_with_Python.utils as u


def cancer_dataset():
    cancer = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target,
                                                        random_state=0)
    # test_neighbors_settings(X_train, X_test, y_train, y_test)
    score = u.curry(X_train, X_test, y_train, y_test)

    score(KNeighborsClassifier, n_neighbors=11)
    score(LogisticRegression)
    score(LogisticRegression, C=100)
    score(DecisionTreeClassifier, random_state=0)
    score(DecisionTreeClassifier, random_state=0, max_depth=4)
    # draw_decision_tree(cancer, X_train, y_train)

    score(RandomForestClassifier, n_estimators=100, random_state=0, max_features=2)
    score(GradientBoostingClassifier, random_state=0, max_depth=1)
    score(GradientBoostingClassifier, random_state=0, learning_rate=0.01)

    score(SVC)
    u.score(SVC, *u.scale_range(X_train, X_test), y_train, y_test, C=1000)
    # plot_feature_importances_cancer(cancer.feature_names, GradientBoostingClassifier().fit(X_train, y_train))

    score(MLPClassifier, random_state=0)
    score(MLPClassifier, random_state=0, solver='lbfgs', hidden_layer_sizes=[100, 10, 5], alpha=0.001)

    mlp_score = partial(u.score, MLPClassifier, *u.scale_std(X_train, X_test), y_train, y_test, random_state=0)
    mlp_score(max_iter=1000)
    mlp_score(solver='lbfgs', hidden_layer_sizes=[100, 10, 5], alpha=0.001)
    mlpc = mlp_score(solver='lbfgs', hidden_layer_sizes=[100, 10, 5], alpha=0.1)
    u.draw_mlp_map(mlpc, feature_names=cancer.feature_names)




def draw_decision_tree(cancer, X_train, y_train):
    dot_data = export_graphviz(
        DecisionTreeClassifier(random_state=0, max_depth=4).fit(X_train, y_train),
        out_file=None,
        class_names=["malignant", "benign"],
        feature_names=cancer.feature_names,
        impurity=False,
        filled=True
    )
    graph = pydotplus.graph_from_dot_data(dot_data)
    graph.write_pdf("cancer.pdf")


def test_neighbors_settings(X_train, X_test, y_train, y_test):
    neighbors = range(1, 11)
    accuracy = np.array(
        [u.score(KNeighborsClassifier, X_train, X_test, y_train, y_test, n_neighbors=i) for i in neighbors]
    )
    plt.plot(neighbors, accuracy[:, 0], label="правильность на обучающем наборе")
    plt.plot(neighbors, accuracy[:, 1], label="правильность на тестовом наборе")
    plt.ylabel("Правильность")
    plt.xlabel("количество соседей")
    plt.legend()


def plot_feature_importances_cancer(feature_names, model):
    n_features = len(feature_names)
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), feature_names)
    plt.xlabel("Важность признака")
    plt.ylabel("Признак")


cancer_dataset()
plt.show()
