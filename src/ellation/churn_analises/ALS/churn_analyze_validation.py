import os

import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
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


def get_X_y(df):
    X = df.loc[:, flt].values
    y = df.churn.values
    return X, y


# S3://codemobs-datalab/ml/vladimir/data_joined_original_joined.csv/
df = pd.read_csv(f'{DIR}/original_dataset_20190312.csv')
flt = (df.columns != 'dwed_account_key') & (df.columns != 'churn') & (df.columns != 'userId') \
          & (
         (df.columns != 'avg_sd')
         & (df.columns != 'five_or_less')
         & (df.columns != 'ten_or_less')
         & (df.columns != 'fifteen_or_less')
         & (df.columns != 'twenty_or_less')
         & (df.columns != 'more_than_twenty')
         & (df.columns != 'std_sd')
         # & (df.columns != 'free_seconds')
         # & (df.columns != 'paid_seconds')
         # & (df.columns != 'total_days')
         # & (df.columns != 'avg_iat')
         # & (df.columns != 'skip_ratio')
         # & (df.columns != 'sum_consumption_time')
         # & (df.columns != 'std_iat')
         # & (df.columns != 'total_streams')
         # & (df.columns != 'std_free_seconds')
         # & (df.columns != 'std_paid_seconds')
         & (df.columns != 'f1')
         & (df.columns != 'f2')
         & (df.columns != 'f3')
         & (df.columns != 'f4')
         & (df.columns != 'f5')
)

X, y = get_X_y(df)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
X_train, y_train = resampling(X_train, y_train)
clf = RandomForestClassifier(n_estimators=56, max_depth=12, random_state=0)
clf.fit(X_train, y_train)
print_stats(clf, X_train, y_train, dataset_type='train')
print_stats(clf, X_test, y_test, dataset_type='test')
# s3://codemobs-datalab/ml/vladimir/data_joined_v2.csv/
df_validation = pd.read_csv(f'{DIR}/validation_dataset_3.csv')
print_stats(clf, *get_X_y(df_validation), dataset_type='validation')
