import datetime
import math

import matplotlib.pyplot as plt
import numpy as np
from pandas_datareader import data

T = 252  # Number of trading days
# download Apple price data into DataFrame
apple = data.DataReader('AAPL', 'yahoo', start=datetime.datetime(2000, 1, 1))
apple['Returns'] = apple['Adj Close'].pct_change().fillna(0)


# Среднегодовой темп роста
# calculate the compound annual growth rate (CAGR) which
# will give us our mean return input (mu)
def cagr():
    years = (apple.index[-1] - apple.index[0]).days / 365
    increasing_stock_price = stock_price(-1) / stock_price(1)
    return increasing_stock_price ** (1 / years) - 1


# create a series of percentage returns and calculate
# the annual volatility of returns
# Изменчивость
def volatility():
    return apple['Returns'].std() * math.sqrt(T)


def stock_price(day):
    return apple['Adj Close'][day]


def daily_returns():
    """
    :return: list of daily returns using random normal distribution
    """
    return np.random.normal(cagr() / T, apple['Returns'].std(), T) + 1


def simulation(times):
    result = []
    for i in range(times):
        # set starting price and create price series generated by above random daily returns
        # starting stock price (i.e. last available real stock price)
        price_list = [stock_price(-1)]
        for x in daily_returns():
            price_list.append(price_list[-1] * x)
        plt.subplot(1, 2, 1)
        plt.plot(price_list)
        result.append(price_list[-1])

    print("mean price =", round(np.mean(result), 2))
    # значение, которое заданная случайная величина не превышает с фиксированной вероятностью.
    #  So we now know that there is a 5% chance that our stock price will end up below around $63.52
    #  and a 95% chance it will finish above $258.44.
    print("5% quantile =", np.percentile(result, 5))
    print("95% quantile =", np.percentile(result, 95))
    # show the plot of multiple price series created above
    plt.subplot(1, 2, 2)
    plt.hist(result)
    plt.axvline(np.percentile(result, 5), color='r', linestyle='dashed', linewidth=2)
    plt.axvline(np.percentile(result, 95), color='r', linestyle='dashed', linewidth=2)
    plt.show()


import pandas_montecarlo
import pandas as pd
mc = apple['Returns'].montecarlo(sims=100, bust=-0.1, goal=1)
# mc = pd.Series(range(5)).montecarlo(sims=10, bust=-0.1, goal=1)
# print(mc.data)
mc.plot(title="SPY Returns Monte Carlo Simulations")

print('CAGR =', str(round(cagr(), 4) * 100) + "%")
print("Annual Volatility =", str(round(volatility(), 4) * 100) + "%")
simulation(100)