import math
from functools import reduce

from clint.textui import cols


def vector_add(v, w):
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def vector_subtract(v, w):
    return [v_i - w_i for v_i, w_i in zip(v, w)]


def scalar_multiply(c, v):
    return [c * v_i for v_i in v]


def vector_sum(vs):
    return reduce(vector_add, vs)


def vector_mean(vectors):
    n = len(vectors)
    scalar_multiply(1 / n, vector_sum(vectors))


def dot(v, w):
    """
    Скаля́рное произведе́ние (иногда внутреннее произведение) — операция над двумя векторами, результатом которой является
    число (когда рассматриваются векторы, числа часто называют скалярами),
    не зависящее от системы координат и характеризующее длины векторов-сомножителей и угол между ними.
    Данной операции соответствует умножение длины вектора x на проекцию вектора y на вектор x.
    (a, b) = |a| * |b| * cos(a, b)
    https://ru.wikipedia.org/wiki/Скалярное_произведение#Геометрическое_определение
    """
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    return dot(v, v)


def magnitude(v):
    return math.sqrt(sum_of_squares(v))


def squared_distance(v, w):
    """ :return (v1 - w1)**2 + ... + (vi - wi)**2 """
    return sum_of_squares(vector_subtract(v, w))


def distance(v, w):
    return math.sqrt(squared_distance(v, w))

#
# def distance(v, w):
#     return magnitude(vector_subtract(v, w))


# Matrix

def shape(A):
    return len(A), len(A[0]) if A else 0


def column(A, j):
    return [row[j] for row in A]


def matrix(rows: int, cols: int, entry_fn: (int, int)):
    return [[entry_fn(i, j) for j in range(cols)] for i in range(rows)]
