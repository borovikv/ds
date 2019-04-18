import math
from collections import Counter

import DS_from_scratch_Joel_Grus.linear_algebra as la


# Показатели центра распределения

def mean(x: list):
    return sum(x) / len(x)


def median(v: list):
    """
    медиана не зависит от каждого значения в наборе данных
    """
    n = len(v)
    midpoint = n // 2
    sorted_v = sorted(v)

    if n % 2 == 1:
        return sorted_v[midpoint]
    else:
        lo = midpoint - 1
        hi = midpoint
        return mean([sorted_v[lo], sorted_v[hi]])


def quantile(v: list, p: float):
    """
    Квантиль - значение, меньше которого расположен определенный процентиль данных,
    т.е. значение в упорядоченной выборке ниже которого расположен заданный процент данных
    """
    p_index = int(p * len(v))
    return sorted(v)[p_index]


def mode(v):
    """
    Мода - значение или значения, которые встречаются наиболее часто
    """
    counts = Counter(v)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.items() if count == max_count]


# Показатели вариации

def data_range(v):
    # размах
    return max(v) - min(v)


def variance(v):
    n = len(v)
    deviations = de_mean(v)
    return la.sum_of_squares(deviations) / (n - 1)


def de_mean(v):
    # вектор отклонения от среднего
    x_bar = mean(v)
    return [x_i - x_bar for x_i in v]


def standart_deviation(v):
    return math.sqrt(variance(v))


def interquartile_range(v):
    # этот показатель позволяет простым образом исключить влияние небольшого числа выбросов
    return quantile(v, 0.75) - quantile(v, 0.25)


# Корреляция
def covariance(x, y):
    n = len(x)
    return la.dot(de_mean(x), de_mean(y)) / (n - 1)


def correlation(x, y):
    stdev_x = standart_deviation(x)
    stdev_y = standart_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0


