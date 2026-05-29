"""
algo_gen.py — adds a new algorithm snippet to the algos/ collection.
Writes to algos/YYYY-MM-DD-HH-<name>.py
"""
import os
import hashlib
from datetime import datetime, timezone

ALGOS = [
    ("binary_search", "Binary Search", """def binary_search(arr: list, target: int) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
"""),
    ("merge_sort", "Merge Sort", """def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
"""),
    ("quicksort", "Quicksort", """def quicksort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)
"""),
    ("bfs", "Breadth-First Search", """from collections import deque

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
"""),
    ("dfs", "Depth-First Search", """def dfs(graph: dict, start, visited=None) -> list:
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbour in graph.get(start, []):
        if neighbour not in visited:
            order.extend(dfs(graph, neighbour, visited))
    return order
"""),
    ("lru_cache", "LRU Cache", """from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)
"""),
    ("trie", "Trie", """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True
"""),
    ("dijkstra", "Dijkstra's Shortest Path", """import heapq

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
"""),
    ("knapsack", "0/1 Knapsack (DP)", """def knapsack(weights: list, values: list, capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][capacity]
"""),
    ("sliding_window", "Sliding Window Max Subarray Sum", """def max_subarray_sum(arr: list, k: int) -> int:
    window = sum(arr[:k])
    best = window
    for i in range(k, len(arr)):
        window += arr[i] - arr[i - k]
        best = max(best, window)
    return best
"""),
    ("two_pointers", "Two Pointers — Pair Sum", """def pair_sum(arr: list, target: int) -> tuple | None:
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        s = arr[lo] + arr[hi]
        if s == target:
            return (arr[lo], arr[hi])
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return None
"""),
    ("union_find", "Union-Find (Disjoint Set)", """class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
"""),
    ("topological_sort", "Topological Sort (Kahn's)", """from collections import deque

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
"""),
    ("segment_tree", "Segment Tree (Range Sum)", """class SegmentTree:
    def __init__(self, arr: list):
        self.n = len(arr)
        self.tree = [0] * (2 * self.n)
        for i, v in enumerate(arr):
            self.tree[self.n + i] = v
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def update(self, i: int, val: int) -> None:
        i += self.n
        self.tree[i] = val
        while i > 1:
            i //= 2
            self.tree[i] = self.tree[2*i] + self.tree[2*i+1]

    def query(self, lo: int, hi: int) -> int:
        res, lo, hi = 0, lo + self.n, hi + self.n
        while lo <= hi:
            if lo % 2 == 1:
                res += self.tree[lo]; lo += 1
            if hi % 2 == 0:
                res += self.tree[hi]; hi -= 1
            lo //= 2; hi //= 2
        return res
"""),
    ("floyd_warshall", "Floyd-Warshall All-Pairs Shortest Path", """def floyd_warshall(n: int, edges: list) -> list:
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
"""),
]

def main():
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    hour_str = now.strftime("%H")
    time_str = now.strftime("%H:%M UTC")

    idx = int(hashlib.md5(f"{date_str}-{hour_str}-algo".encode()).hexdigest(), 16) % len(ALGOS)
    slug, title, code = ALGOS[idx]

    header = f'"""\n{title}\nGenerated: {date_str} {time_str}\n"""\n\n'

    os.makedirs("algos", exist_ok=True)
    out = f"algos/{date_str}-{hour_str}-{slug}.py"
    with open(out, "w") as f:
        f.write(header + code)

    print(f"algo: wrote {out} — {title}")
    return out

if __name__ == "__main__":
    main()
