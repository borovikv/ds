from collections import defaultdict
from functools import reduce


def contains_not_unique_symbols(line):
    return len(line) == len(set(line))


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def add(self, value):
        if value == self.value:
            raise Exception()
        elif value < self.value and self.left:
            self.left.add(value)
        elif value > self.value and self.right:
            self.right.add(value)
        elif value < self.value:
            self.left = Node(value)
        elif value > self.value:
            self.right = Node(value)

    def to_str(self, level=1):
        result = self.value if level == 1 else ''
        for child in self.children:
            result += '\n' + '\t' * level + str(child.value)
            result += child.to_str(level=level + 1)
        return result

    @property
    def children(self):
        return list(filter(bool, [self.left, self.right]))


def contains_not_unique_symbols_2(line):
    root = Node(line[0])
    for s in line[1:]:
        try:
            root.add(s)
        except:
            print(root.to_str())
            return False
    print(root.to_str())
    return True


# ab ba
# abc bac bca cba cab acb

def permutation(s):
    # O(N2)
    if len(s) == 1:
        return s
    head, *tail = s
    permutations = permutation(tail)
    result = []
    for p in permutations:
        for i in range(len(p) + 1):
            result.append(p[:i] + head + p[i:])
    return result


def is_permutation(s1, s2):
    if len(s1) != len(s2):
        return False
    return s1 in permutation(s2)


def is_permutation_2(s1, s2):
    return count_letters(s1) == count_letters(s2)


def count_letters(line):
    result = defaultdict(int)
    for l in line:
        result[l] += 1
    return result


def replace_space(input):
    # return input.replace(' ', '%20')
    return ''.join([l if l != ' ' else '%20' for l in input])


def is_one_simbol_behind_1_5(a, b):
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False

    pattern, check = (a, b) if len(a) >= len(b) else (b, a)

    for i, l in enumerate(pattern):
        is_not_end_of_check = i < len(check)
        if is_not_end_of_check and check[i] != l:
            if pattern not in (replace(check, i, l), insert(check, i, l)):
                return False
            else:
                return True
    return True


def insert(string, position, letter):
    return string[:position] + letter + string[position:]


def replace(string, position, letter):
    return string[:position] + letter + string[position + 1:]


def compress_string(s):
    # 1.7
    if not s:
        return s
    result = []
    counter = 0
    previous_letter = s[0]
    for i, l in enumerate(s):
        if previous_letter != l:
            result += [previous_letter, str(counter)]
            counter = 0
        counter += 1
        previous_letter = l
    result = ''.join(result + [previous_letter, str(counter)])
    return result if len(result) < len(s) else s


def compress_string_2(s):
    return ''.join(map(str, reduce(fold, zip(s, [1] * len(s)), [])))


def fold(accumulator, e):
    accumulator = list(accumulator)
    if accumulator and e[0] == accumulator[-2]:
        accumulator[-1] += 1
    else:
        accumulator += list(e)
    return accumulator


def set_0(matrix):
    nullable_indexes = [(i, j) for i, row in enumerate(matrix) for j, e in enumerate(row) if e == 0]
    for i, j in nullable_indexes:
        set_row_to_0(matrix, i)
        set_col_to_0(matrix, j)
    return matrix


def set_row_to_0(matrix, row_index):
    row = matrix[row_index]
    for i in range(len(row)):
        row[i] = 0


def set_col_to_0(matrix, col_index):
    for row in matrix:
        row[col_index] = 0
