import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree.tree import DecisionTreeClassifier


def cancer_dataset():
    cancer = load_breast_cancer()
    print(cancer.data.shape)
    X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target,
                                                        random_state=42)
    # test_neighbors_settings(X_train, X_test, y_train, y_test)
    score(KNeighborsClassifier, X_train, X_test, y_train, y_test, n_neighbors=11)
    score(LogisticRegression, X_train, X_test, y_train, y_test)
    score(LogisticRegression, X_train, X_test, y_train, y_test, C=100)
    score(DecisionTreeClassifier, X_train, X_test, y_train, y_test, random_state=0)
    score(DecisionTreeClassifier, X_train, X_test, y_train, y_test, random_state=0, max_depth=4)
    score(RandomForestClassifier, X_train, X_test, y_train, y_test, n_estimators=100, random_state=0, max_features=2)

    # dot_data = export_graphviz(
    #     fit(DecisionTreeClassifier, X_train, y_train, random_state=0, max_depth=4),
    #     out_file=None,
    #     class_names=["malignant", "benign"],
    #     feature_names=cancer.feature_names,
    #     impurity=False,
    #     filled=True
    # )
    # graph = pydotplus.graph_from_dot_data(dot_data)
    # graph.write_pdf("cancer.pdf")


def test_neighbors_settings(X_train, X_test, y_train, y_test):
    neighbors = range(1, 11)
    accuracy = np.array(
        [score(KNeighborsClassifier, X_train, X_test, y_train, y_test, n_neighbors=i) for i in neighbors]
    )
    plt.plot(neighbors, accuracy[:, 0], label="правильность на обучающем наборе")
    plt.plot(neighbors, accuracy[:, 1], label="правильность на тестовом наборе")
    plt.ylabel("Правильность")
    plt.xlabel("количество соседей")
    plt.legend()


def fit(method, X_train, y_train, **kwargs):
    return method(**kwargs).fit(X_train, y_train)


def score(method, X_train, X_test, y_train, y_test, **kwargs):
    clf = fit(method, X_train, y_train, **kwargs)
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)

    print(f"{method.__name__} {kwargs or ''} Правильность на обучающем наборе: {train_score:.3f}")
    print(f"{method.__name__} {kwargs or ''} Правильность на тестовом наборе: {test_score:.3f}")
    return train_score, test_score


cancer_dataset()

plt.show()
