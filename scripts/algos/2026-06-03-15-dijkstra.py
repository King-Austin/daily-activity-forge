"""
Dijkstra's Shortest Path
Generated: 2026-06-03 15:06 UTC
"""

import heapq

def dijkstra(graph: dict, start) -> dict:
    dist = {start: 0}
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float('inf')):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
