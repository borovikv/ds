from collections import defaultdict


def criticalRouters(links):
    return critical_nodes(build_graph(links))


def build_graph(links):
    result = defaultdict(list)
    for a, b in links:
        result[a].append(b)
        result[b].append(a)
    return result


def critical_nodes(graph):
    result = set()
    for i in graph.keys():
        new_graph = dict(graph)
        siblings = new_graph.pop(i)
        result.update(i for sibling in siblings for node in new_graph if not connected(sibling, node, new_graph))
    return result


def connected(start, end, graph, visited=()):
    if start == end:
        return True
    for n in graph.get(start, []):
        if n in visited:
            continue
        if connected(n, end, graph, visited + (start,)):
            return True
    return False


links_1 = [[1, 2], [2, 3], [3, 4], [4, 5], [6, 3], ]
links_2 = [[1, 2], [1, 3], [2, 4], [3, 4], [3, 6], [4, 5], [6, 7], ]

print(criticalRouters(links_1))
print(criticalRouters(links_2))
