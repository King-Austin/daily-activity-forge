# Algorithm: Kahn's Algorithm for DAG Topological Sort
# Recorded: 2026-05-17 12:12 UTC

from collections import deque

def kahn_topo_sort(num_nodes, edges):
    adj = {i: [] for i in range(num_nodes)}
    in_degree = [0] * num_nodes
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1
    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return order if len(order) == num_nodes else []

