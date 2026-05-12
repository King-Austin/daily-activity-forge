# Algorithm: Counting Bloom Filter Implementation
# Recorded: 2026-05-12 16:05 UTC

import hashlib

class CountingBloomFilter:
    def __init__(self, size=1024, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.counts = [0] * size
    def _hashes(self, item):
        res = []
        for i in range(self.num_hashes):
            h = int(hashlib.md5(f"{item}:{i}".encode()).hexdigest(), 16)
            res.append(h % self.size)
        return res
    def add(self, item):
        for idx in self._hashes(item):
            self.counts[idx] += 1
    def contains(self, item):
        return all(self.counts[idx] > 0 for idx in self._hashes(item))

