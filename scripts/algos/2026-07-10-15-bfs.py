"""
Breadth-First Search
Generated: 2026-07-10 15:03 UTC
"""

from collections import deque

def bfs(graph: dict, start) -> list:
    visited, queue, order = set(), deque([start]), []
    visited.add(start)
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.get(node, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return order
