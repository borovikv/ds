# import timeit
from collections import deque


def find_path_breadth(graph, start, end):
    queue = deque([start])
    visited = {start}
    result = []
    path = []
    while queue:
        v = queue.popleft()
        path.append(v)
        siblings = graph.get(v, [])
        for v1 in siblings:
            if v1 == end:
                path.append(v1)
                result.append(path)
                path = [start]
                break
            if v1 not in visited:
                queue.append(v1)
                visited.add(v1)
    return result


def find_path_depth(graph, start, end, paths=None, path=()):
    if not paths:
        paths = []

    if start == end:
        paths.append(path + (end,))
        return

    for v in graph.get(start, []):
        find_path_depth(graph, v, end, paths, path + (start,))

    return paths


# 4.2 input = 1, 2, 3, 4, 5, 6, 7
# output
"""
        4
      /   \
      2   6
    /  \ / \
    1  3 5  7
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.value)

    def pre_order_traversal(self, indent=0):
        print('\t' * indent + f'{self.value}')
        indent += 1
        for c in [self.left, self.right]:
            if c:
                c.pre_order_traversal(indent)
            else:
                print('\t' * indent + '*')

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value


def create_binary_tree(a):
    if not a:
        return
    middle = len(a) // 2
    n = Node(a[middle])
    n.left = create_binary_tree(a[:middle])
    n.right = create_binary_tree(a[middle + 1:])
    return n


def create_binary_tree_2(a, start=0, stop=None):
    if stop is None:
        stop = len(a) - 1
    if stop < start:
        return
    middle = (start + stop) // 2
    n = Node(a[middle])
    n.left = create_binary_tree_2(a, start, middle - 1)
    n.right = create_binary_tree_2(a, middle + 1, stop)
    return n


# n = create_binary_tree_2(list(range(1, 8)))
# n.pre_order_traversal()
#
# t = timeit.timeit('create_binary_tree(list(range(1, 8000)))', "from __main__ import create_binary_tree", number=1)
# print(t)
# t = timeit.timeit('create_binary_tree_2(list(range(1, 8000)))', "from __main__ import create_binary_tree_2", number=1)
# print(t)


# 4.3
def get_level_nodes(root, level):
    if level == 0:
        return [root]
    result = []
    for n in get_level_nodes(root, level - 1):
        result += [n.left, n.right]
    return result


# print(get_level_nodes(n, 0))
# print(get_level_nodes(n, 1))
# print(get_level_nodes(n, 2))


def get_levels(root, level=0, levels=None):
    if not root:
        return
    if not levels:
        levels = []
    if level == len(levels):
        levels.append([])
    levels[level].append(root)
    get_levels(root.left, level + 1, levels)
    get_levels(root.right, level + 1, levels)
    return levels


# print(get_levels(n))


# 4.4
def is_balanced(root):
    if root is None:
        return True
    if abs(get_height(root.left) - get_height(root.right)) > 1:
        return False
    return is_balanced(root.left) and is_balanced(root.right)


def get_height(root):
    if not root:
        return 0
    return max(get_height(root.left), get_height(root.right)) + 1


def check_height(root):
    if root is None:
        return 0
    left_height = check_height(root.left)
    right_height = check_height(root.right)
    if abs(left_height - right_height) > 1:
        raise RuntimeError(f'tree is not balanced {root}')
    return max(left_height, right_height) + 1


def is_balanced_2(root):
    try:
        check_height(root)
    except RuntimeError as e:
        print(e)
        return False
    return True


# 4.5
def is_binary_search_tree(root):
    if root is None:
        return True
    if root.left and find(max, root.left) >= root or root.right and root > find(min, root.right):
        return False
    return is_binary_search_tree(root.left) and is_binary_search_tree(root.right)


def find(f, root):
    if not root:
        return
    return f(filter(bool, (root, find(f, root.left), find(f, root.right))))


# ---------------------------------------------------------------------------------------------------------

def is_binary_search_tree_2(root):
    if root is None:
        return True
    if is_ge(root.left, root) or is_lt(root.right, root):
        return False
    return is_binary_search_tree(root.left) and is_binary_search_tree(root.right)


def is_ge(root, current):
    if not root:
        return False
    if root >= current:
        return True
    return is_ge(root.left, current) or is_ge(root.right, current)


def is_lt(root, current):
    if not root:
        return False
    if root < current:
        return True
    return is_lt(root.left, current) or is_lt(root.right, current)


# ---------------------------------------------------------------------------------------------------------

def check_bst(root):
    def check_bst_inner(n, last=None):
        if n is None:
            return True, last

        is_bst, last = check_bst_inner(n.left, last)
        if not is_bst:
            return False, None

        if last is not None and n <= last:
            return False, None

        is_bst, last = check_bst_inner(n.right, n)
        if not is_bst:
            return False, None

        return True, last

    return check_bst_inner(root)[0]
