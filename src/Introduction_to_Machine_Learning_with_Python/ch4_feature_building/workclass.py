import os

import pandas as pd
from sklearn.linear_model.base import LinearRegression
from sklearn.linear_model.logistic import LogisticRegression

from Introduction_to_Machine_Learning_with_Python.utils import split_score

base_dir = '~/workspace/DS/'

df = pd.read_csv(os.path.join(base_dir, 'resources/introduction_to_ml_with_python-master/data/adult.data'),
                 header=None,
                 index_col=False,
                 names=['age', 'workclass', 'fnlwgt', 'education', 'education-num',
                        'marital-status', 'occupation', 'relationship', 'race', 'gender', 'capital-gain',
                        'capital-loss',
                        'hours-per-week', 'native-country', 'income'])

df = df[['age', 'workclass', 'education', 'gender', 'hours-per-week', 'occupation', 'income']]

dummies = pd.get_dummies(df)
features = dummies.ix[:, 'age':'occupation_ Transport-moving']
x = features.values
y = dummies['income_ >50K'].values

split_score(LinearRegression, x, y)
split_score(LogisticRegression, x, y)
