def dijkstra(graph, start):
    graph = dict(graph)
    predecessor = {}
    shortest_distance = {node: float('inf') for node in graph}
    shortest_distance[start] = 0

    while graph:
        current_node = min(graph, key=lambda node: shortest_distance[node])
        child_nodes = graph.pop(current_node)

        for child_node, weight in child_nodes.items():
            weight_to_child_node = weight + shortest_distance[current_node]
            if weight_to_child_node < shortest_distance[child_node]:
                shortest_distance[child_node] = weight_to_child_node
                predecessor[child_node] = current_node

    return shortest_distance, predecessor


def find_shortest_distance(start, goal, predecessor, shortest_distance):
    path = reversed(get_path(start, goal, predecessor))
    print('Shortest distance is ' + str(shortest_distance[goal]))
    print('And the path is ' + ' -> '.join(path))


def get_path(start, goal, predecessor):
    if start == goal:
        return [start]
    return [goal] + get_path(start, predecessor[goal], predecessor)


a, b, c, d, e, f = 'abcdef'

graph = {
    a: {b: 7, c: 9, f: 14},
    b: {a: 7, c: 10, d: 15},
    c: {a: 9, b: 10, d: 11, f: 2},
    d: {b: 15, c: 11, e: 6},
    e: {d: 6, f: 9},
    f: {a: 14, c: 2, e: 9},
}

shortest_path, predecessor = dijkstra(graph, 'a')
print([shortest_path, predecessor])
find_shortest_distance('a', 'd', predecessor, shortest_path)
