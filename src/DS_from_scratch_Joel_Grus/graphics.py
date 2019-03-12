from collections import Counter

from matplotlib import pyplot as plt

grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]
decile = lambda g: g // 10 * 10
histogram = Counter(decile(g) for g in grades)

plt.bar([x for x in histogram.keys()], histogram.values(), 8)

print(histogram.keys())
print(histogram.values())

plt.axis([-5, 105, 0, 5])

plt.xticks([10 * i for i in range(11)])

plt.show()
