import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
from sklearn.linear_model.base import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

import warnings

warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

def get_survival_df(file_name):
    raw_data_path = os.path.join(os.path.dirname(__file__), file_name)
    df = pd.read_csv(raw_data_path)
    try:
        df = df[df.top_10]
    except AttributeError:
        pass
    df = pd.pivot_table(df, values='count', index=['tenure'], columns=['country_code'], aggfunc=np.sum)
    df.loc[-1] = df.sum()
    df.index = df.index + 1  # shifting index
    df = df.sort_index()  # sorting by index
    df = df.fillna(0)
    previous_index = 0
    for i in df.index:
        if i > 0:
            df.loc[i] = df.loc[previous_index] - df.loc[i]
        previous_index = i
    return df


def normalize_1(df):
    df = pd.DataFrame(df)
    total = df.loc[0]
    for i in df.index:
        df.loc[i] /= total
    return df


def draw_plot(model_name, X, y, X_train, X_test, y_train, y_test, prediction):
    fig, axes = plt.subplots(1, 3, figsize=(10, 3))
    axes[0].plot(X, y, label="Original data", )
    axes[1].plot(X_train, y_train, '*', label="Learning data")
    axes[1].plot(X_test, y_test, 'o', label="Test data")
    axes[1].plot(X_test, prediction, 's', label='Prediction')
    axes[2].plot(X_test, y_test, 'o', label="Test data")
    axes[2].plot(X_test, prediction, 's', label='Prediction')
    plt.legend()
    fig.suptitle(model_name, fontsize=16)


FILE_NAME = 'CLV Excel Prototype - Training Set - raw data 10-01 to 11-30.csv'
# FILE_NAME = 'validation_set_us.csv'
df = get_survival_df(FILE_NAME)
# df = normalize_1(df)

models = [
    [KNeighborsRegressor, dict(n_neighbors=1)],
    [KNeighborsRegressor, dict(n_neighbors=2)],
    [KNeighborsRegressor, dict(n_neighbors=3)],
    [KNeighborsRegressor, dict(n_neighbors=4)],
    [KNeighborsRegressor, dict(n_neighbors=4)],
    # [KNeighborsRegressor, dict(n_neighbors=5)],
    # [RandomForestRegressor, dict(n_estimators=35, random_state=2)],
    # [GradientBoostingRegressor, dict(random_state=0, max_depth=2)],
    # [LinearRegression, dict()],
    # [DecisionTreeRegressor, dict()],
]
countries = ['AU', 'BR', 'CA', 'CL', 'CO', 'DE', 'FR', 'GB', 'MX', 'US']
countries = ['US']
# countries = ['MX']
countries = ['CO']
for country in countries:
    print(f'Country {country}')
    country_df = df[country]
    country_df = country_df[country_df != 0]
    # country_df = df[country]
    X = np.array(df.index).reshape(-1, 1)  # [[0], [1], ...]
    y = df.US.values
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    y_train_log = np.log(y_train + 1)
    y_test_log = np.log(y_test + 1)

    for cls, kwargs in models:
        model_name = f"Модель: {cls.__name__} {kwargs}"
        print(model_name)

        model1 = cls(**kwargs).fit(X_train, y_train)
        print(f"Правильность на обучающем наборе\t{model1.score(X_train, y_train):.3f}")
        print(f"Правильность на тестовом наборе\t{model1.score(X_test, y_test):.3f}")

        model2 = cls(**kwargs).fit(X_train, y_train_log)
        print(f"Правильность на обучающем наборе [log]\t{model1.score(X_train, y_train_log):.3f}")
        print(f"Правильность на тестовом наборе [log]\t{model1.score(X_test, y_test_log):.3f}")

        prediction1 = model1.predict(X_test)
        prediction2 = model2.predict(X_test)
        draw_plot(model_name, X, y, X_train, X_test, y_train, y_test, prediction1)
        draw_plot(model_name + ' log', X, y,  X_train, X_test, y_train_log, y_test_log, prediction2)

plt.show()
