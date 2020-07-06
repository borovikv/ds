import math
from collections import Counter
from random import random

from matplotlib import pyplot as plt

from DS_from_scratch_Joel_Grus.probability import inverse_normal_cdf


def bucketize(point, bucket_size):
    return bucket_size * math.floor(point / bucket_size)


def make_histogram(points, bucket_size):
    return Counter(bucketize(p, bucket_size) for p in points)


def plot_histogram(points, bucket_size, title=''):
    histogram = make_histogram(points, bucket_size)
    plt.bar(list(histogram.keys()), histogram.values(), width=bucket_size)
    plt.title(title)
    plt.show()


def random_normal():
    return inverse_normal_cdf(random())

def plot_scatter():
    xs = [random_normal() for _ in range(1000)]
    ys1 = [x + random_normal() / 2 for x in xs]
    ys2 = [-x + random_normal() / 2 for x in xs]
    plt.scatter(xs, ys1, marker='*', label='ys1')
    plt.scatter(xs, ys2, marker='^', label='ys2')
    plt.xlabel('xs')
    plt.ylabel('ys')
    plt.legend(loc=9)
    plt.show()

# plot_histogram(range(10), 3)
plot_scatter()
