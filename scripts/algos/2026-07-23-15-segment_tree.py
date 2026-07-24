"""
Segment Tree (Range Sum)
Generated: 2026-07-23 15:53 UTC
"""

class SegmentTree:
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
