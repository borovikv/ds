from collections import Counter

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
