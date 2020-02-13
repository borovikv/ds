import random
from typing import Callable

from DS_from_scratch_Joel_Grus.linear_algebra import distance, sum_of_squares


def difference_quotient(f, x, h):
    return (f(x + h) - f(x)) / h


def partial_difference_quotient(f: Callable, v: list, i: int, h: 'float "приращение"'):  # вычислить i-ю производную
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)]
    return (f(w) - f(v)) / h


def estimate_gradient(f, v, h=0.00001):
    return [partial_difference_quotient(f, v, i, h) for i in range(len(v))]


def step(v, direction, step_size):
    return [v_i + step_size * direction_i for v_i, direction_i in zip(v, direction)]


def sum_of_squares_gradient(v):
    return [2 * v_i for v_i in v]  # estimate_gradient(sum_of_squares, v)


def safe(f):
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return float('inf')

    return safe_f


v = [random.randint(-10, 10) for i in range(3)]
tolerance = 1e-7

print(sum_of_squares_gradient(v))
print(estimate_gradient(sum_of_squares, v))

while True:
    gradient = sum_of_squares_gradient(v)
    next_v = step(v, gradient, -0.01)
    print(next_v)
    if distance(next_v, v) < tolerance:
        break
    v = next_v
print(v)
