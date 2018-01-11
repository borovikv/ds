import numpy as np
import pydotplus
from matplotlib import pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree.export import export_graphviz
from sklearn.tree.tree import DecisionTreeClassifier


def cancer_dataset():
    cancer = load_breast_cancer()
    print(cancer.data.shape)
    X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, stratify=cancer.target,
                                                        random_state=0)
    # test_neighbors_settings(X_train, X_test, y_train, y_test)
    score(KNeighborsClassifier, X_train, X_test, y_train, y_test, n_neighbors=11)
    score(LogisticRegression, X_train, X_test, y_train, y_test)
    score(LogisticRegression, X_train, X_test, y_train, y_test, C=100)
    score(DecisionTreeClassifier, X_train, X_test, y_train, y_test, random_state=0)
    score(DecisionTreeClassifier, X_train, X_test, y_train, y_test, random_state=0, max_depth=4)
    score(RandomForestClassifier, X_train, X_test, y_train, y_test, n_estimators=100, random_state=0, max_features=2)
    score(GradientBoostingClassifier, X_train, X_test, y_train, y_test, random_state=0, max_depth=1)
    score(GradientBoostingClassifier, X_train, X_test, y_train, y_test, random_state=0, learning_rate=0.01)

    score(SVC, X_train, X_test, y_train, y_test)

    # вычисляем минимальное значение для каждого признака обучающего набора
    min_on_training = X_train.min(axis=0)
    # вычисляем ширину диапазона для каждого признака (max - min) обучающего набора
    range_on_training = (X_train - min_on_training).max(axis=0)
    # вычитаем минимальное значение и затем делим на ширину диапазона
    # min=0 и max=1 для каждого признака
    X_train_scaled = (X_train - min_on_training) / range_on_training
    X_test_scaled = (X_test - min_on_training) / range_on_training

    print("Минимальное значение для каждого признака\n{}".format(X_train_scaled.min(axis=0)))
    print("Максимальное значение для каждого признака\n {}".format(X_train_scaled.max(axis=0)))
    score(SVC, X_train_scaled, X_test_scaled, y_train, y_test, C=1000)

    plot_feature_importances_cancer(cancer.feature_names, GradientBoostingClassifier().fit(X_train, y_train))
    # draw_decision_tree(cancer, X_train, y_train)


def draw_decision_tree(cancer, X_train, y_train):
    dot_data = export_graphviz(
        fit(DecisionTreeClassifier, X_train, y_train, random_state=0, max_depth=4),
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



def plot_feature_importances_cancer(feature_names, model):
    n_features = len(feature_names)
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), feature_names)
    plt.xlabel("Важность признака")
    plt.ylabel("Признак")


cancer_dataset()
plt.show()
