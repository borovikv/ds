a, b, c, d, e, f = 'abcdef'
example_graph = {
    a: {b: 7, c: 9, f: 14},
    b: {a: 7, c: 10, d: 15},
    c: {a: 9, b: 10, d: 11, f: 2},
    d: {b: 15, c: 11, e: 6},
    e: {d: 6, f: 9},
    f: {a: 14, c: 2, e: 9},
}


def dijkstra(graph, start):
    visited = [start]
    for node in graph:
        neighbors = {k: v for k, v in graph[node].items() if k not in visited}
        if not neighbors:
            break
        n = min(neighbors, key=lambda n: graph[node][n])
        visited.append(n)
    return visited


print(dijkstra(example_graph, a))



