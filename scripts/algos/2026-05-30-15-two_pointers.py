"""
Two Pointers — Pair Sum
Generated: 2026-05-30 15:59 UTC
"""

def pair_sum(arr: list, target: int) -> tuple | None:
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
