import matplotlib.pyplot as plt
import mglearn

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.svm import SVC


def make_forge():
    X, y = mglearn.datasets.make_forge()
    print("форма массива X: {}".format(X.shape))

    fig, axes = plt.subplots(2, 2, figsize=(10, 3))
    for model, ax in zip([LinearSVC(), LogisticRegression()], axes[0]):
        clf = model.fit(X, y)

        mglearn.plots.plot_2d_separator(clf, X, fill=False, eps=0.5, ax=ax, alpha=.7)
        mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
        ax.set_title(f"{clf.__class__.__name__}")
        ax.set_xlabel("Первый признак")
        ax.set_ylabel("Второй признак")

    axes[0, 0].legend()

    # строим график для набора данных
    mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
    plt.legend(["Класс 0", "Класс 1"], loc=4)
    plt.xlabel("Первый признак")
    plt.ylabel("Второй признак")

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    classify(KNeighborsClassifier, X_train, X_test, y_train, y_test, n_neighbors=3)
    classify(LinearSVC, X_train, X_test, y_train, y_test)
    classify(LogisticRegression, X_train, X_test, y_train, y_test)

    svm = SVC(kernel='rbf', C=10, gamma=5).fit(X, y)
    print(f"SVC Правильность на тестовом наборе: {svm.score(X_test, y_test):.2f}")
    mglearn.plots.plot_2d_separator(svm, X, eps=.5, ax=axes[1][0])
    mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=axes[1][0])
    # размещаем на графике опорные векторы
    sv = svm.support_vectors_
    # метки классов опорных векторов определяются знаком дуальных коэффициентов
    sv_labels = svm.dual_coef_.ravel() > 0
    mglearn.discrete_scatter(sv[:, 0], sv[:, 1], sv_labels,
                             s=15, markeredgewidth=3, ax=axes[1][0], markers=['+', 'v'])
    plt.xlabel("Признак 0")
    plt.ylabel("Признак 1")


def classify(method, X_train, X_test, y_train, y_test, **kwargs):
    clf = method(**kwargs)
    clf.fit(X_train, y_train)
    print(f"{method.__name__} Правильность на тестовом наборе: {clf.score(X_test, y_test):.2f}")
    prediction = clf.predict(X_test)
    plt.plot(X_test, prediction, '*')




make_forge()
plt.show()
