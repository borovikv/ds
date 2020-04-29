n = 10

r = []
for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                if a ** 3 + b ** 3 == c ** 3 + d ** 3:
                    r.append((a, b, c, d))
# print(set(r))
print(len(set(r)))
print(r)
x = [[(a, b, a, b), (b, a, b, a)] if a != b else [(a, b, a, b)] for a in range(n) for b in range(n)]
print(x)

# print(len(set(x)))
print(len(r), len(x))


from itertools import product

print(len(list(product(range(n), range(n)))))
