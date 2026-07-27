"""
Sliding Window Max Subarray Sum
Generated: 2026-07-24 12:05 UTC
"""

def max_subarray_sum(arr: list, k: int) -> int:
    window = sum(arr[:k])
    best = window
    for i in range(k, len(arr)):
        window += arr[i] - arr[i - k]
        best = max(best, window)
    return best
