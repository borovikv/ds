import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree.tree import DecisionTreeClassifier


def get_df():
    df = pd.read_csv('churn4_1.csv')
    df = pd.pivot_table(
        df, index=['dwed_account_key', 'churn'], columns=['week_no', 'type'], values='seconds', aggfunc=np.sum
    )
    df = df.fillna(0)
    df = (df - df.mean()) / df.std(ddof=0).pow(2)
    for i in range(12):
        # df[i,'paid_ratio'] = (df[i]['free'] - df[i]['paid'])/df[i]['paid']
        # df[i,'free_ratio'] = (df[i]['free'] - df[i]['paid'])/df[i]['free']
        df[i,'paid_ratio_2'] = df[i]['paid'] / (df[i]['free'] + df[i]['paid'])
        df[i,'free_ratio_2'] = df[i]['free']/ (df[i]['free'] + df[i]['paid'])
        df[i,'diff_1'] = df[i]['free'] - df[i]['paid']

    df = df.fillna(0)

    # df = df.iloc[:, df.columns.get_level_values(1) == 'paid_ratio_2']
    # df = df.iloc[:, df.columns.get_level_values(1) == 'free_ratio_2']
    # df = df.iloc[:, df.columns.get_level_values(1) == 'diff_1']
    # df.sort_index(axis=1, inplace=True)
    return df


def test_classifiers():
    df = get_df()
    X = df.values
    y = np.array([j for i, j in df.index.values])
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    X_not_churn = X_train[y_train == 0]
    X_churn = X_train[y_train == 1]
    X_not_churn_trimmed = X_not_churn[np.random.randint(X_not_churn.shape[0], size=len(X_churn)), :]
    X_train = np.concatenate((X_not_churn_trimmed, X_churn))
    y_train = np.array([0] * len(X_not_churn_trimmed) + [1] * len(X_churn))
    # X_test = X_test.reshape(-1, 1)
    # X_train = X_train.reshape(-1, 1)
    clfs = [
        RandomForestClassifier(n_estimators=50, random_state=0),
        GradientBoostingClassifier(),
        # KNeighborsClassifier(n_neighbors=12),
        # DecisionTreeClassifier(max_depth=10, random_state=0),
        # LogisticRegression(),
        # LinearSVC(C=0.01),
    ]
    #
    for clf in clfs:
        print_stats(clf, X_train, y_train, X_test, y_test)


def plot():
    # X = np.array(df.index).reshape(-1, 1)  # [[0], [1], ...]
    # y = df.values
    # print(y)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    #
    # df = df[:1]
    # X = [[i, i] for i in range(12)]
    # y = df.values.reshape(-1, 2)
    # # #
    # print(X)
    # print(y)
    # df_churn = df.iloc[df.index.get_level_values('churn') == 0][:5]
    # print(df_churn)
    # for i in range(len(df_churn)):
    #     plt.plot([[i] for i in range(12)], df_churn.iloc[i].values.reshape(-1, 1))
    plt.show()


def print_stats(clf, X_train, y_train, X_test, y_test):
    clf.fit(X_train, y_train)
    print(f'\n{clf.__class__.__name__}')
    print(f"Правильность на обучающем наборе: {clf.score(X_train, y_train):.3f}")
    print(f"Правильность на тестовом наборе: {clf.score(X_test, y_test):.3f}")
    print(f"Confusion matrix test:")
    print_confusion_matrix(clf, X_test, y_test)
    print(f"Confusion matrix train:")
    print_confusion_matrix(clf, X_train, y_train)
    print(f"F1 score test: {f1_score(y_test, clf.predict(X_test))}")
    print(f"F1 score train: {f1_score(y_train, clf.predict(X_train))}")
    print('-' * 100)


def print_confusion_matrix(clf, X, y):
    prediction = clf.predict(X)
    confusion = confusion_matrix(y, prediction)
    template = '{:>5}{:>5}'
    print(template.format('TN', 'FP'))
    print(template.format(*confusion[0]))
    print(template.format('FN', 'TP'))
    print(template.format(*confusion[1]))
    print(classification_report(y, prediction, target_names=['not churn', 'churn']))


test_classifiers()
