"""
Floyd-Warshall All-Pairs Shortest Path
Generated: 2026-05-30 12:58 UTC
"""

def floyd_warshall(n: int, edges: list) -> list:
    INF = float('inf')
    dist = [[INF]*n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
