# Algorithm snippet: kmp_matcher
# Timestamp: 2026-10-17 04:24 UTC

def kmp_search(pattern, text):
    pi = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    res = []
    j = 0
    for i, c in enumerate(text):
        while j > 0 and c != pattern[j]:
            j = pi[j - 1]
        if c == pattern[j]:
            j += 1
            if j == len(pattern):
                res.append(i - j + 1)
                j = pi[j - 1]
    return res

