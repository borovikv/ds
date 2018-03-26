import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
import numpy as np
from sklearn.preprocessing.data import OneHotEncoder, PolynomialFeatures

from Introduction_to_Machine_Learning_with_Python.utils import resource_path


def load_citibike():
    data_mine = pd.read_csv(resource_path("data", "citibike.csv"))
    data_mine['one'] = 1
    data_mine['starttime'] = pd.to_datetime(data_mine.starttime)
    data_starttime = data_mine.set_index("starttime")
    data_resampled = data_starttime.resample("3h").sum().fillna(0)
    return data_resampled.one


citibike = load_citibike()
print(citibike.head(10))

y = citibike.values
X = citibike.index.astype("int64").values.reshape(-1, 1) // 10 ** 9
X_hour = citibike.index.hour.values.reshape(-1, 1)
X_day = citibike.index.dayofweek.values.reshape(-1, 1)
X_day_hour = np.hstack([X_day, X_hour])

n_train = 184


def eval_on_features(features, target, regressor):
    # plt.figure()
    X_train, X_test = features[:n_train], features[n_train:]
    y_train, y_test = target[:n_train], target[n_train:]
    regressor.fit(X_train, y_train)
    print("R^2 for test data: {:.2f}".format(regressor.score(X_test, y_test)))

    y_pred = regressor.predict(X_test)
    y_pred_train = regressor.predict(X_train)

    plt.figure(figsize=(10, 3))
    plt.plot(range(n_train), y_train, label="train")
    plt.plot(range(n_train, len(y_test) + n_train), y_test, '-', label="test")
    plt.plot(range(n_train), y_pred_train, '--', label="prediction")
    plt.plot(range(n_train, len(y_test) + n_train), y_pred, '--', label="prediction test")

    plt.legend(loc=(1.01, 0))
    xticks = pd.date_range(start=citibike.index.min(), end=citibike.index.max(), freq='D')
    plt.xticks(range(0, len(X), 8), xticks.strftime("%a %m-%d"), rotation=90, ha="left")
    plt.xlabel("date")
    plt.ylabel("frequency")


regressor = RandomForestRegressor(n_estimators=100, random_state=0)

# eval_on_features(X, y, regressor)
# eval_on_features(X_hour, y, Ridge())
# eval_on_features(X_day, y, Ridge())
# eval_on_features(X_day_hour, y, Ridge())

eval_on_features(X_hour, y, regressor)
eval_on_features(X_day, y, regressor)
eval_on_features(X_day_hour, y, regressor)

enc = OneHotEncoder()
X_day_hour_onehot = enc.fit_transform(X_day_hour).toarray()
lr = Ridge()
eval_on_features(X_day_hour_onehot, y, lr)

poly_transformer = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_hour_week_onehot_poly = poly_transformer.fit_transform(X_day_hour_onehot)
eval_on_features(X_hour_week_onehot_poly, y, lr)


hour = ["%02d:00" % i for i in range(0, 24, 3)]
day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
features = day + hour
features_poly = poly_transformer.get_feature_names(features)
print(features_poly)
features_nonzero = np.array(features_poly)[lr.coef_ != 0]
print(features_nonzero)
coef_nonzero = lr.coef_[lr.coef_ != 0]
# print(coef_nonzero)


plt.show()
