# import mglearn
import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_digits
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_recall_curve
from sklearn.metrics.ranking import average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def print_metrics(X, y, *methods):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    is_binary = len(np.bincount(y)) == 2
    for method in methods:
        print('-' * 20, method.__class__.__name__, '-' * 20)
        method.fit(X_train, y_train)
        pred_method = method.predict(X_test)
        print('Score:', method.score(X_test, y_test))
        print("Confusion matrix:\n", confusion_matrix(y_test, pred_method))
        print(classification_report(y_test, pred_method))
        if is_binary:
            print("f1_score", f1_score(y_test, pred_method))
        print("f1_score micro", f1_score(y_test, pred_method, average="micro"))
        print("f1_score macro", f1_score(y_test, pred_method, average="macro"))
        print("accuracy_score", accuracy_score(y_test, pred_method))
        if is_binary and hasattr(method, 'decision_function'):
            print('Average precision score:', average_precision_score(y_test, method.decision_function(X_test)))


def plot_precision_recall_curve(X, y, *methods):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    markers = ["o", "v", "^", "<", ">", "s", "p"]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for marker, color, method in zip(markers, colors, methods):
        method_pred = method.fit(X_train, y_train)
        if hasattr(method, 'decision_function'):
            precision, recall, thresholds = precision_recall_curve(y_test, method_pred.decision_function(X_test))
        else:
            precision, recall, thresholds = precision_recall_curve(y_test, method_pred.predict_proba(X_test)[:, 1])
        close_zero = np.argmin(np.abs(thresholds))
        plt.plot(precision[close_zero], recall[close_zero],
                 marker, c=color, markersize=10, label="Порог 0", fillstyle="none", mew=2)
        plt.plot(precision, recall, label="Кривая точноси полнонты %s" % method.__class__.__name__, c=color)
    plt.xlabel("Точность")
    plt.ylabel("Полнота")
    plt.legend(loc="best")


logreg = LogisticRegression(C=0.1)
svc = SVC(gamma=.05)

digits = load_digits()
X = digits.data
y = digits.target == 9

# print_metrics(X, y, logreg, svc, DummyClassifier())
# plot_precision_recall_curve(X, y, svc, logreg)

# X, y = make_blobs(n_samples=(4000, 500), centers=2, cluster_std=[7.0, 2], random_state=22)
# rf = RandomForestClassifier(n_estimators=100, random_state=0, max_features=2)
# plot_precision_recall_curve(X, y, svc, logreg, rf)

# mglearn.plots.plot_confusion_matrix_illustration()



print_metrics(digits.data, digits.target, logreg, svc, DummyClassifier())


plt.show()
