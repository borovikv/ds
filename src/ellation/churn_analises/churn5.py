import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def resampling(X_train, y_train):
    ros = RandomUnderSampler(random_state=0)
    X_ros, y_ros = ros.fit_sample(X_train, y_train)
    return X_ros, y_ros


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


def print_confusion_matrix(clf, X, y):
    prediction = clf.predict(X)
    confusion = confusion_matrix(y, prediction)
    d = pd.DataFrame(confusion, index=['not churn', 'churn'], columns=['predicted not churn', 'predicted churn'])
    d = d.div(d.sum(axis=1), axis=0)
    print(d)
    print(classification_report(y, prediction, target_names=['not churn', 'churn']))


def get_df():
    df = pd.read_csv('features_17_2018.csv').fillna(0)
    return df


df = get_df()
X = df.loc[:, (df.columns != 'dwed_account_key') & (df.columns != 'churn')].values

y = df.churn.values
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

X_train, y_train = resampling(X_train, y_train)

select = RFE(RandomForestClassifier(n_estimators=50, random_state=0), n_features_to_select=30)
select.fit(X_train, y_train)
X_train = select.transform(X_train)
X_test = select.transform(X_test)
clfs = [
    RandomForestClassifier(n_estimators=50, random_state=0),
    # RandomForestClassifier(n_estimators=100, random_state=0),
    # RandomForestClassifier(n_estimators=50, max_depth=10, random_state=0),
    # RandomForestClassifier(n_estimators=50, max_depth=20, random_state=0),
    GradientBoostingClassifier(),
    KNeighborsClassifier(n_neighbors=12),
    DecisionTreeClassifier(max_depth=10, random_state=0),
    LogisticRegression(),
    # LinearSVC(C=0.01),
    # LogisticRegression(),
]
#
for i, clf in enumerate(clfs):
    print(i, '-' * 100)
    print_stats(clf, X_train, y_train, X_test, y_test)
