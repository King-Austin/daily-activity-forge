# Algorithm snippet: fenwick_tree
# Timestamp: 2026-10-30 06:54 UTC

class FenwickTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
    def update(self, i, delta):
        i += 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)
    def query(self, i):
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

