from collections import deque
from heapq import heappush, heappop 

def shortest_shortest_path(graph, source):
    """
    Params: 
      graph.....a graph represented as a dict where each key is a vertex
                and the value is a set of (vertex, weight) tuples (as in the test case)
      source....the source node
      
    Returns:
      a dict where each key is a vertex and the value is a tuple of
      (shortest path weight, shortest path number of edges). See test case for example.
    """
    dist = {v: float('inf') for v in graph}
    edges = {v: 0 for v in graph}
    dist[source] = 0
    pq = [(0, 0, source)]

    while pq:
        d, e, u = heappop(pq)
        if d > dist[u]:
            continue

        for v, weight in graph[u]:
            new_distance = d + weight
            new_edges = e + 1

            if new_distance < dist[v] or (new_distance == dist[v] and new_edges < edges[v]):
                dist[v] = new_distance
                edges[v] = new_edges
                heappush(pq, (new_distance, new_edges, v))

    return {v: (dist[v], edges[v]) for v in graph}
    
def test_shortest_shortest_path():

    graph = {
                's': {('a', 1), ('c', 4)},
                'a': {('b', 2)}, # 'a': {'b'},
                'b': {('c', 1), ('d', 4)}, 
                'c': {('d', 3)},
                'd': {},
                'e': {('d', 0)}
            }
    result = shortest_shortest_path(graph, 's')
    # result has both the weight and number of edges in the shortest shortest path
    assert result['s'] == (0,0)
    assert result['a'] == (1,1)
    assert result['b'] == (3,2)
    assert result['c'] == (4,1)
    assert result['d'] == (7,2)
    
    
def bfs_path(graph, source):
    """
    Returns:
      a dict where each key is a vertex and the value is the parent of 
      that vertex in the shortest path tree.
    """
    visited = set()
    queue = deque([(source, None)])
    parents = {}

    while queue:
        node, parent = queue.popleft()
        if node not in visited:
            visited.add(node)
            parents[node] = parent
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, node))

    return parents

def get_sample_graph():
     return {'s': {'a', 'b'},
            'a': {'b'},
            'b': {'c'},
            'c': {'a', 'd'},
            'd': {}
            }

def test_bfs_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert parents['a'] == 's'
    assert parents['b'] == 's'    
    assert parents['c'] == 'b'
    assert parents['d'] == 'c'
    
def get_path(parents, destination):
    """
    Returns:
      The shortest path from the source node to this destination node 
      (excluding the destination node itself). See test_get_path for an example.
    """
    path = []
    node = destination

    while node is not None:
        path.append(node)
        node = parents[node]

    path = path[::-1][:-1]
    return ''.join(path)

def test_get_path():
    graph = get_sample_graph()
    parents = bfs_path(graph, 's')
    assert get_path(parents, 'd') == 'sbc'
