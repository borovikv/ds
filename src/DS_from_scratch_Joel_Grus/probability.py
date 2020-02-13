"""
Непрерывное распределение расстояния вероятностей представляют плотностью распределения вероятностей
(probability density function) (дифференциальной функцией распределения),
такой что наблюдать значение в определенном интервале равна интегралу от дифференциальной функции,
взятому в этих пределах.
"""
import math


def uniform_pdf(x):
    """
    Probability density function равномерного распределения
    """
    return 1 if 0 <= x < 1 else 0


def uniform_cdf(x):
    """
    Интегральная функциея распределения:
        определяет вероятность, что случаная величина меньше или равана некоторому значению
    """
    if x < 0:
        return 0
    elif x < 1:
        return x
    else:
        return 1


def normal_pdf(x, mu=0, sigma=1):
    """
    :param x:
    :param mu: μ — математическое ожидание (среднее значение), медиана и мода распределения
    :param sigma: σ — среднеквадратическое отклонение (σ ² — дисперсия) распределения
    """
    sqrt_2_pi = math.sqrt(2 * math.pi)
    return math.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * sqrt_2_pi)


def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / (sigma * math.sqrt(2)))) / 2


def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = - 10.0, 0  # normal_cdf(-10) ~ 0
    hi_z, hi_p = 10.0, 1  # normal_cdf(10) ~ 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2
        mid_p = normal_cdf(mid_z)
        if mid_p < p:
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z
