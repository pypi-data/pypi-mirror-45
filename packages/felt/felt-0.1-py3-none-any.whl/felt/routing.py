
class NoPath(Exception):
    pass


def shortest_path(graph, source, sink):

    unvisited = set(node.name for node in graph.nodes())
    prev = { n: None for n in unvisited }
    dist = { n: float('inf') for n in unvisited }
    dist[source] = 0

    while unvisited:

        current_node = min([(dist[n], n) for n in unvisited])[1]

        unvisited.remove(current_node)

        if current_node == sink:
            break

        for neighbor in unvisited.intersection(
                node.name for node in graph.neighbors(current_node)):
            new_dist = dist[current_node] + \
                graph.links[current_node][neighbor].length()
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = current_node

    nodes = []

    current_node = sink
    while current_node is not None:
        nodes.append(current_node)
        current_node = prev[current_node]

    nodes = nodes[::-1]

    if not nodes:
        raise NoPath(source, sink)

    if nodes[0] != source:
        raise NoPath(source, sink)

    if nodes[-1] != sink:
        raise NoPath(source, sink)

    return nodes

        

        
