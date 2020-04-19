# import timeit
from collections import deque
from random import randint


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
        self.parent = None

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
        if not other:
            return False
        return self.value == other.value

    def add(self, where, node):
        if where == 'left':
            self.left = node
        else:
            self.right = node
        node.parent = self


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


def check_bst_2(n, min_n=None, max_n=None):
    print(n, min_n, max_n)
    if not n:
        return True
    if min_n and n < min_n or max_n and n >= max_n:
        return False
    if not (check_bst_2(n.left, min_n, n) and check_bst_2(n.right, n, max_n)):
        return False
    return True


# **************************************************************************************************************
# 4.6
def get_next(node):
    # the solution is not correct due to miss understanding acceptance criteria
    if node.parent is None:
        return
    if node.parent and node.parent.right and node.parent.right != node:
        return node.parent.right

    next_parent = get_next(node.parent)
    if next_parent.left:
        return next_parent.left
    elif next_parent.right:
        return next_parent.right
    return next_parent


def left_most_child(n):
    if n is None:
        return
    while n.left:
        n = n.left
    return n


def inorder_succ(n):
    if n is None:
        return
    if n.right:
        return left_most_child(n.right)
    else:
        q = n
        q_parent = q.parent
        while q_parent and q_parent.left != q:
            q = q_parent
            q_parent = q.parent
        return q_parent


# **************************************************************************************************************
# 4.7
def build_dependency(projects):
    result = []
    seen = set()
    for k in projects:
        if k not in result and k not in seen:
            recursive_topological_sort(projects, k, set(), result)

    return result


def recursive_topological_sort(graph, node, seen, result):
    if node in result:
        return True
    if node in seen:
        raise Exception('cycle', )
    seen.add(node)
    for child in graph[node]:
        recursive_topological_sort(graph, child, seen, result)
    result.append(node)
    return True


def build_dependency_2(projects, result=None):
    if result is None:
        result = []
    if not projects:
        return result
    for p, dependencies in projects.items():
        if not dependencies:
            if p not in result:
                result.append(p)
        for d in dependencies:
            if d not in projects:
                dependencies.remove(d)
                if d not in result:
                    result.append(d)
            else:
                if p in projects[d]:
                    raise Exception('Cycle')

    for r in result:
        projects.pop(r, None)
    build_dependency_2(projects, result)
    return result


# **************************************************************************************************************
# 4.8
def find_common_parent(root: Node, n1, n2):
    if not root or root in (n1, n2):
        return root
    n1_on_left = dfs(root.left, n1)
    n2_on_left = dfs(root.left, n2)
    if n1_on_left != n2_on_left:
        return root
    side = root.left if n1_on_left else root.right
    return find_common_parent(side, n1, n2)


def dfs(root: Node, node):
    if not root:
        return False
    if root == node:
        return True
    return dfs(root.left, node) or dfs(root.right, node)


def common_ancestor(root, p, q):
    if not root:
        return
    if root == p or root == q:
        return root

    ancestors = []
    for n in [root.left, root.right]:
        ancestor = common_ancestor(n, p, q)
        if ancestor and ancestor != p and ancestor != q:
            return ancestor
        ancestors.append(ancestor)

    x, y = ancestors
    if x and y:
        return root
    return x or y


# **************************************************************************************************************
# 4.9
def get_initial_dataset(root):
    result = []
    if not root:
        result.append([])
        return result
    left_seq = get_initial_dataset(root.left)
    right_seq = get_initial_dataset(root.right)

    for left in left_seq:
        for right in right_seq:
            weaved = []
            weave(left, right, [root], weaved)
            result += weaved
    return result


def weave(first, second, prefix, results):
    print(first, second, prefix, results)
    if not first or not second:
        results.append(prefix + first + second)
        return

    prefix.append(first[0])
    weave(first[1:], second, prefix, results)
    prefix.pop()

    prefix.append(second[0])
    weave(first, second[1:], prefix, results)
    prefix.pop()


# **************************************************************************************************************
# 4.10
list()


def is_sub_tree(t1, t2):
    if not t2:
        return True
    node = find_first_node(t1, t2)
    if not node:
        return False
    return match_tree(node, t2)
    # if not (node.left == t2.left and node.right == t2.right):
    #     return False
    # return is_sub_tree(node, t2.left) and is_sub_tree(node, t2.right)


def find_first_node(root, node):
    if not root or root == node:
        return root
    return find_first_node(root.left, node) or find_first_node(root.right, node)


def is_sub_tree_2(t1, t2):
    a = pre_order_traversal(t2)
    b = pre_order_traversal(t1)
    return is_sublist(a, b)


def pre_order_traversal(root):
    if not root:
        return [None]
    return [root] + pre_order_traversal(root.left) + pre_order_traversal(root.right)


def is_sublist(l1, l2: list):
    first = l1[0]
    indexes = (i for i, e in enumerate(l2) if e == first)
    for i in indexes:
        if l1 == l2[i:i + len(l1)]:
            return True
    return False


def sub_tree(r1, r2):
    # from book
    if not r1:
        return False
    elif r1 == r2 and match_tree(r1, r2):
        return True
    return sub_tree(r1.left, r2) or sub_tree(r1.right, r2)


def match_tree(r1, r2):
    if not r1 and not r2:
        return True
    elif not r1 or not r2 or r1 != r2:
        return False
    else:
        return match_tree(r1.left, r2.left) and match_tree(r1.right, r2.right)


# **************************************************************************************************************
# 4.11
class NodeWithRandom:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self._left = None
        self._right = None
        self.children = 0

    def pre_order_traversal(self, indent=0):
        print('\t' * indent + f'{self.value}')
        indent += 1
        for c in [self._left, self._right]:
            if c:
                c.pre_order_traversal(indent)

    def __setattr__(self, key, value):
        if key in ['left', 'right']:
            if value is not None:
                self.__dict__[f'_{key}'] = NodeWithRandom(value, self)
                self.children += 1
                if self.parent:
                    self.parent.children += 1
            else:
                self.__dict__[f'_{key}'] = None
                self.children -= 1
                if self.parent:
                    self.parent.children -= 1
        else:
            super(NodeWithRandom, self).__setattr__(key, value)

    def __getattr__(self, item):
        if item in ['left', 'right']:
            return self.__dict__[f'_{item}']
        return self.__dict__[item]

    def get_random_node(self):
        n = randint(0, self.children)
        print(n)
        return breadth_first_search(self, n)

    def __repr__(self):
        return str(self.value)


def breadth_first_search(root, nth):
    queue = deque([root])
    counter = 0
    while queue:
        r = queue.popleft()
        if counter == nth:
            return r
        counter += 1
        for n in [r.left, r.right]:
            if n:
                queue.append(n)


# **************************************************************************************************************
# 4.12
def find_all_path_for_number(root, target_sum):
    if not root:
        return 0
    paths = path_with_sum_from_node(root, target_sum, 0)
    paths_on_left = find_all_path_for_number(root.left, target_sum)
    paths_on_right = find_all_path_for_number(root.right, target_sum)
    return paths + paths_on_left + paths_on_right


def path_with_sum_from_node(root, target_sum, current=0):
    if not root:
        return 0
    current += root.value
    total_paths = 0
    if current == target_sum:
        total_paths += 1
    total_paths += path_with_sum_from_node(root.left, target_sum, current)
    total_paths += path_with_sum_from_node(root.right, target_sum, current)
    return total_paths


r = create_binary_tree([-3, -2, -1, 5, 6, 7, 8])
r.pre_order_traversal()
print(find_all_path_for_number(r, 2))
