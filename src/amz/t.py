import re
from collections import Counter


def popularNToys(numToys, topToys, toys, numQuotes, quotes):
    pattern = '|'.join(map('({})'.format, toys))
    toy_pattern = re.compile(pattern)
    counter = Counter()
    for quote in quotes:
        for toy in getToys(quote, toy_pattern):
            counter[toy] += 1
    most_common = counter.most_common(topToys)
    return [t for t, _ in sorted(most_common, key=lambda x: (-x[1], x[0]))]


def getToys(quote, toy_pattern):
    finds = toy_pattern.findall(quote)
    return set(t for m in finds for t in m if t)


print(
    popularNToys(
        5,
        2,
        ['ab', 'ac', 'ad', 'xy', 'xz'],
        3,
        [
            'bla bla ab asjdf',
            'bla bla xy xz asjdf',
            'bla bla ac asjdf',
        ]
    )
)
