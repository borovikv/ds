import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble.forest import RandomForestRegressor
from sklearn.ensemble.gradient_boosting import GradientBoostingRegressor
from sklearn.linear_model.base import LinearRegression
from sklearn.tree import DecisionTreeRegressor

ram_prices = pd.read_csv("ram_price.csv", index_col=0)
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
axes[0].semilogy(ram_prices.date, ram_prices.price)
axes[0].set_xlabel("Год")
axes[0].set_ylabel("Цена $/Мбайт")
plt.semilogy(ram_prices.date, ram_prices.price)

# используем исторические данные для прогнозирования цен после 2000 года
data_train = ram_prices[ram_prices.date < 2000]
plt.semilogy(data_train.date, data_train.price, label="Обучающие данные")

# прогнозируем цены по датам
X_train = data_train.date[:, np.newaxis]
# мы используем логпреобразование, что получить простую взаимосвязь между данными и откликом
y_train = np.log(data_train.price)
# прогнозируем по всем данным
X_all = ram_prices.date[:, np.newaxis]

methods = [
    LinearRegression,
    DecisionTreeRegressor,
    (GradientBoostingRegressor, dict(random_state=0, max_depth=1)),
    (RandomForestRegressor, dict(n_estimators=500, random_state=2))
]
for method in methods:
    kwargs = dict()
    if isinstance(method, tuple):
        method, kwargs = method
    reg = method(**kwargs).fit(X_train, y_train)
    # экспоненцируем, чтобы обратить логарифмическое преобразование
    predict = reg.predict(X_all)
    predict_price = np.exp(predict)
    plt.semilogy(ram_prices.date, predict_price, label=f'Прогнозы {method.__name__}')

plt.legend()
plt.show()
