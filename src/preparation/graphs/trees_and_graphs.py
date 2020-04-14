from collections import deque

a, b, c, d, e, f = 'abcdef'
g = dict(
    a=[b, e, f],
    b=[d, e],
    d=[c],
)


def flatten(l):
    return [e for l1 in l for e in l1]


def nodes_without_entrance():
    return g.keys() - set(flatten(g.values()))


def depth_first_search(g, root, visited):
    print(root)
    children = g.get(root, [])
    visited.add(root)
    for n in children:
        if n not in visited:
            depth_first_search(g, n, visited)


def breadth_first_search(g, root):
    queue = deque([root])
    visited = {root}
    while queue:
        r = queue.popleft()
        print(r)
        children = g.get(r, [])
        for n in children:
            if n not in visited:
                visited.add(n)
                queue.append(n)


depth_first_search(g, 'a', set())
print('breadth_first_search')
breadth_first_search(g, 'a')
print('nodes_without_entrance')
print(nodes_without_entrance())


def recursive_topological_sort(graph, node, seen, result):
    for neighbor in graph.get(node, []):
        if neighbor not in seen:
            seen.add(neighbor)
            recursive_topological_sort(graph, neighbor, seen, result)
    result.insert(0, node)
    return result


print('recursive_topological_sort')

g = {
    1: [4],
    4: [2, 3],
    3: [2]
}
print(recursive_topological_sort(g, 1, set(), []))
