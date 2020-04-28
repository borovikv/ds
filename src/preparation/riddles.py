def sieve_of_eratosthenes(n):
    limit = n + 1
    a = list(range(limit))
    a[1] = 0
    primes = []

    for i in range(2, limit):
        if a[i] != 0:
            primes.append(a[i])
            for j in range(i, limit, i):
                a[j] = 0
    return primes


print(sieve_of_eratosthenes(100))


l = [False] * 100
for i in range(1, 100):
    for j in range(i, 100, i + 1):
        l[j] = not l[j]

print(sum(1 for k in l if k))
