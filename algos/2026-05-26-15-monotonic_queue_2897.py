# Algorithm: Sliding Window Maximum Monotonic Queue
# Recorded: 2026-05-26 15:14 UTC

from collections import deque

class MonotonicQueue:
    def __init__(self):
        self.q = deque()
    def push(self, val):
        while self.q and self.q[-1] < val:
            self.q.pop()
        self.q.append(val)
    def max(self):
        return self.q[0] if self.q else None
    def pop(self, val):
        if self.q and self.q[0] == val:
            self.q.popleft()

