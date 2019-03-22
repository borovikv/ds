import os
from functools import reduce
from operator import ior

import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import train_test_split

DIR = os.path.dirname(__file__)


def resampling(X_train, y_train):
    ros = RandomUnderSampler(random_state=0)
    X_ros, y_ros = ros.fit_sample(X_train, y_train)
    return X_ros, y_ros


def print_stats(clf, X, y, dataset_type='test'):
    print(f'\n{clf.__class__.__name__}')
    print(f"Правильность на {dataset_type} наборе: {clf.score(X, y):.3f}")
    print(f"Confusion matrix {dataset_type}:")
    print(f"F1 score {dataset_type}: {f1_score(y, clf.predict(X))}")
    prediction = clf.predict(X)
    confusion = confusion_matrix(y, prediction)
    d = pd.DataFrame(confusion, index=['not churn', 'churn'], columns=['predicted not churn', 'predicted churn'])
    d = d.div(d.sum(axis=1), axis=0)
    print(d)
    print('average confusion', (d['predicted not churn']['not churn'] + d['predicted churn']['churn']) / 2)


def get_X_y(df, columns):
    selector = reduce(ior, [(df.columns == c) for c in columns])
    X = df.loc[:, selector].values
    y = df.churn.values
    return X, y


# S3://codemobs-datalab/ml/vladimir/data_joined_original_joined.csv/
# df = pd.read_csv(f'{DIR}/original_dataset_20190312.csv')
df = pd.read_csv(f'{DIR}/data/main_dataset_2019-03-13.csv')
columns = [
    'free_seconds',
    'paid_seconds',
    'total_days',
    'avg_iat',
    'skip_ratio',
    'sum_consumption_time',
    'std_iat',
    'total_streams',
    'std_free_seconds',
    'std_paid_seconds',
    'avg_sd',
    'five_or_less',
    'ten_or_less',
    'fifteen_or_less',
    'twenty_or_less',
    'more_than_twenty',
    'std_sd',
]
# columns += [f'f{i}' for i in range(1, 6)]

X, y = get_X_y(df, columns)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
X_train, y_train = resampling(X_train, y_train)
# clf = RandomForestClassifier(n_estimators=56, max_depth=12, random_state=0)
# clf.fit(X_train, y_train)

# print(columns)
# print_stats(clf, X_train, y_train, dataset_type='train')
# print_stats(clf, X_test, y_test, dataset_type='test')

# s3://codemobs-datalab/ml/vladimir/data_joined_v2.csv/
# df_validation = pd.read_csv(f'{DIR}/validation_dataset_3.csv')
# print_stats(clf, *get_X_y(df_validation, columns), dataset_type='validation')

# print('\nFeature importance')
# print(pd.Series(dict(zip(df.loc[:, columns].columns, clf.feature_importances_))).sort_values(ascending=False))


df_values = df.loc[:, reduce(ior, [(df.columns == c) for c in columns])]
for j in range(1, len(df_values.columns) + 1):
    print(j, '*' * 100)
    select = RFE(RandomForestClassifier(n_estimators=56, max_depth=12, random_state=0), n_features_to_select=j)
    select.fit(X_train, y_train)
    X_train_selected = select.transform(X_train)
    X_test_selected = select.transform(X_test)

    clf = RandomForestClassifier(n_estimators=56, max_depth=12, random_state=0)
    clf.fit(X_train_selected, y_train)
    print(list(df_values.columns[select.support_]))
    print_stats(clf, X_test_selected, y_test, dataset_type='test')

['free_seconds', 'paid_seconds', 'total_days', 'avg_iat', 'five_or_less', 'ten_or_less', 'skip_ratio',
 'sum_consumption_time', 'std_iat', 'total_streams', 'std_free_seconds', 'std_paid_seconds']
