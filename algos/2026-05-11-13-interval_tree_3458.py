# Algorithm: Segment Interval Overlap Search
# Recorded: 2026-05-11 13:58 UTC

class IntervalNode:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.max = high
        self.left = None
        self.right = None

def insert_interval(root, low, high):
    if not root:
        return IntervalNode(low, high)
    if low < root.low:
        root.left = insert_interval(root.left, low, high)
    else:
        root.right = insert_interval(root.right, low, high)
    root.max = max(root.max, high)
    return root

