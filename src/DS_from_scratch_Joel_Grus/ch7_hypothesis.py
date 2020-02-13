import math

from DS_from_scratch_Joel_Grus.probability import inverse_normal_cdf, normal_cdf


# аппроксимация биномиально случайной величины нормальным распределение


def normal_approximation_to_binomial(n, p):
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


# вероятность, что значение нормальной случайной величины лежит ниже порогового значения
normal_probability_below = normal_cdf


def normal_probability_above(lo, mu=0, sigma=1.0):
    return 1 - normal_cdf(lo, mu, sigma)


def normal_probability_between(lo, hi, mu=0, sigma=1.0):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


def normal_probability_outside(lo, hi, mu=0, sigma=1.0):
    return 1 - normal_probability_between(lo, hi, mu, sigma)


def normal_upper_bound(probability, mu=0, sigma=1.0):
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability, mu=0, sigma=1.0):
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability, mu=0, sigma=1.0):
    tail_probability = (1 - probability) / 2
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)
    return lower_bound, upper_bound


# mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
# print(mu_0, sigma_0)


#
#
# lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
# print(lo, hi)
#
# mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
# print(mu_1, sigma_1)
#
# type_2_prob = normal_probability_between(lo, hi, mu_1, sigma_1)
# print(type_2_prob)


def two_sided_p_value(x, mu=0, sigma: float = 1):
    if x >= mu:
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        return 2 * normal_probability_below(x, mu, sigma)


# print(two_sided_p_value(529.5, mu_0, sigma_0))
#
# count = 0
# i = 10000
# for _ in range(i):
#     num_heads = sum(1 if random.random() < 0.5 else 0 for _ in range(1000))
#     if num_heads >= 530 or num_heads <= 470:
#         count += 1
# print(count / i)


def estimated_parameters(N, n):
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma


def a_b_test_statistic(N_A, n_A, N_B, n_B):
    p_A, sigma_A = estimated_parameters(N_A, n_A)
    p_B, sigma_B = estimated_parameters(N_B, n_B)
    return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigma_B ** 2)


z = a_b_test_statistic(1000, 10, 1000, 2)
print(z)
p_eq = two_sided_p_value(z)
print(p_eq)
