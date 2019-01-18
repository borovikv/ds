import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import neural_network
from sklearn.neighbors import KNeighborsRegressor
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

raw_data_path = os.path.join(os.path.dirname(__file__), 'tenure_by_country_and_started.csv')
df = pd.read_csv(raw_data_path)

df = df[df.country == 'MX']
df = df.drop('country', axis=1)
total_by_month = df[['month', 'count']].groupby('month').sum().reset_index()
df = df.merge(total_by_month, on='month')
df['lost'] = df.groupby('month').count_x.cumsum().shift()
df.loc[df.tenure == 0, 'lost'] = 0
df['total_survival'] = df.count_y - df.lost
df['survival'] = df.total_survival / df.count_y
# df = df[df.survival >= 0.2]
df = df[df.month < 15]


features = df[['tenure', 'month']]
X_train = features[features.month <= 8].values
X_test = features[features.month > 8].values
y_train = df[df.month <= 8].survival.values.ravel()
y_test = df[df.month > 8].survival.values.ravel()

model = neural_network.MLPRegressor(max_iter=750, alpha=7, random_state=0).fit(X_train, y_train)
model = KNeighborsRegressor(n_neighbors=3).fit(X_train, y_train)
# model = linear_model.LinearRegression().fit(X_train, y_train)

print(f"Correctness on train set {model.__class__.__name__}: {model.score(X_train, y_train):.3f}")
print(f"Correctness on test set {model.__class__.__name__}: {model.score(X_test, y_test):.3f}")

y_train_log = np.log(y_train + 1)
y_test_log = np.log(y_test + 1)
# model = KNeighborsRegressor().fit(X_train, y_train_log)
model = linear_model.LinearRegression().fit(X_train, y_train_log)
print(f"Correctness on train set {model.__class__.__name__}: {model.score(X_train, y_train):.3f}")
print(f"Correctness on test set {model.__class__.__name__}: {model.score(X_test, y_test_log):.3f}")

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
for month in set(df.month):
    x = df[df.month == month].tenure.values
    y = df[df.month == month].survival.values.ravel()
    axes[0].plot(x, y, '*', label=month, )
    axes[0].legend()
    y = np.log(y + 1)
    axes[1].plot(x, y, '*', label=month)
    break

plt.show()
df.to_csv('output.csv', index=False)
