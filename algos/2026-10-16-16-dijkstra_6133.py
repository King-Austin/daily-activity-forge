# Algorithm snippet: dijkstra
# Timestamp: 2026-10-16 16:50 UTC

import heapq
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        cur_d, u = heapq.heappop(pq)
        if cur_d > distances[u]:
            continue
        for v, weight in graph[u]:
            d = cur_d + weight
            if d < distances[v]:
                distances[v] = d
                heapq.heappush(pq, (d, v))
    return distances

