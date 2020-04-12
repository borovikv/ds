def remove_dub(input):
    result = list(input)
    removed = 0
    for i, e1 in enumerate(input):
        for j, e2 in enumerate(input):
            if j <= i:
                continue
            if e2 == e1:
                result.pop(j - removed)
                removed += 1
    return result


def access(l, k):
    length = 0
    for _ in l:
        length += 1
    pos = 0
    for e in l:
        if pos == length - k:
            return e
        pos += 1


def reorder(l, k):
    l1 = []
    l2 = []
    for e in l:
        if e < k:
            l1.append(e)
        else:
            l2.append(e)
    return l1 + l2


def sum_l(a_1, a_2):
    if not a_1 or not a_2:
        return a_1 + a_2
    s = a_1[0] + a_2[0]
    if s > 9:
        return [s - 10] + sum_l(sum_l([1], a_1[1:]), a_2[1:])
    return [s] + sum_l(a_1[1:], a_2[1:])


def sum_l_straight(a, b):
    if not a or not b:
        return a + b
    a, b = align(a, b)

    if len(a) == 1 and len(b) == 1:
        return to_array(a[0] + b[0])
    else:
        bh, *bt = b
        ah, *at = a
        partial_sum = sum_l_straight(at, bt)
        if len(partial_sum) > 1:
            res_h, *res_t = partial_sum
        else:
            res_h, res_t = 0, partial_sum

        return to_array(res_h + bh + ah) + res_t


def align(a, b):
    dif = [0] * abs(len(a) - len(b))
    a, b = (a, dif + b) if len(a) > len(b) else (dif + a, b)
    return a, b


def to_array(s):
    return [1, s - 10] if s > 9 else [s]
