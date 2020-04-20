def insert(m, n, i, j):
    low_mask = (1 << i) - 1
    top_mask = ~0 << j
    mask = low_mask | top_mask
    return n & mask | m << i


def to_b(n):
    result = '{0:031b}'.format(n)
    return result


def print_binary(num):
    if not (0 <= num < 1):
        raise ValueError()

    frac = 0.5
    result = '.'
    while num > 1e-3:
        if len(result) > 32:
            raise ValueError('not enough space')
        if num >= frac:
            result += '1'
            num -= frac
        else:
            result += '0'
        frac /= 2
    return result


def number_of_ones(n):
    count = 0
    while n > 0:
        count = count + 1
        n = n & (n - 1)
    return count


# 5.3
def longest_sequence(a):
    """
    Имеется целое число, в котором можно изменить ровно один бит из 0 в 1.
    Напишите код для определения длины самой длинной последовательности единиц,
    которая может быть при этом получена.”
    """
    print(a)
    result = []
    c = 0
    while a != 0:
        if a & 1 == 1:
            c += 1
        else:
            result.append(c)
            result.append(0)
            c = 0
        a = a >> 1
    result.append(c)

    max_val = 1
    for i, n in enumerate(result):
        if n != 0:
            if len(result) > i + 2 and result[i + 2] != 0:
                max_val = max(max_val, n + result[i + 2] + 1)
            else:
                max_val = max(max_val, n + 1)
    return max_val


print(longest_sequence(int('111101101', 2)))
print(longest_sequence(int('10001001100', 2)))
