"""
Topological Sort (Kahn's)
Generated: 2026-07-07 15:17 UTC
"""

from collections import deque

def topo_sort(graph: dict, nodes: list) -> list:
    indegree = {n: 0 for n in nodes}
    for u in nodes:
        for v in graph.get(u, []):
            indegree[v] = indegree.get(v, 0) + 1
    queue = deque(n for n in nodes if indegree[n] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return order if len(order) == len(nodes) else []
