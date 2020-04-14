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

    def pre_order_traversal(self, indent=0):
        print('\t' * indent + f'{self.value}')
        indent += 1
        for c in [self.left, self.right]:
            if c:
                c.pre_order_traversal(indent)


def create_binary_tree(a):
    if not a:
        return
    middle = len(a) // 2
    n = Node(a[middle])
    n.left = create_binary_tree(a[:middle])
    n.right = create_binary_tree(a[middle + 1:])
    return n


n = create_binary_tree(list(range(1, 8)))
n.pre_order_traversal()
