"""
Depth-First Search
Generated: 2026-06-12 12:33 UTC
"""

def dfs(graph: dict, start, visited=None) -> list:
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbour in graph.get(start, []):
        if neighbour not in visited:
            order.extend(dfs(graph, neighbour, visited))
    return order
