import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
from sklearn.linear_model.base import LinearRegression
from sklearn.tree import DecisionTreeRegressor


def predict_for_methods(ram_prices, *methods):
    # используем исторические данные для прогнозирования цен после 2000 года
    data_train = ram_prices[ram_prices.date < 2000]
    # прогнозируем цены по датам
    X_train = data_train.date[:, np.newaxis]
    # мы используем логпреобразование, что получить простую взаимосвязь между данными и откликом
    y_train = np.log(data_train.price)

    # прогнозируем по всем данным
    X_all = ram_prices.date[:, np.newaxis]

    result = {}
    for method in methods:
        kwargs = {}
        if isinstance(method, tuple):
            method, kwargs = method
        prediction = method(**kwargs).fit(X_train, y_train).predict(X_all)
        # экспоненцируем, чтобы обратить логарифмическое преобразование
        result[method.__name__] = np.exp(prediction)
    return result


def semilogy(ax, date, price, label):
    ax.semilogy(date, price, label=label)
    ax.set_xlabel("Год")
    ax.set_ylabel("Цена $/Мбайт")


def draw_plot(ram_prices, *methods):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3))
    semilogy(axes[0], ram_prices.date, ram_prices.price, label="Оригинальные данные")
    semilogy(axes[1], ram_prices.date, ram_prices.price, label="Обучающие данные")

    predictions = predict_for_methods(ram_prices, *methods)
    for method, predict_price in predictions.items():
        semilogy(axes[1], ram_prices.date, predict_price, label=f'Прогнозы {method}')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    ram_prices = pd.read_csv("ram_price.csv", index_col=0)
    draw_plot(
        ram_prices,
        LinearRegression,
        DecisionTreeRegressor,
        (GradientBoostingRegressor, dict(random_state=0, max_depth=1)),
        (RandomForestRegressor, dict(n_estimators=500, random_state=2))
    )
