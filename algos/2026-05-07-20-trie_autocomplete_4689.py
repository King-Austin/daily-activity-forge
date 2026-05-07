# Algorithm: Prefix Tree Autocomplete
# Recorded: 2026-05-07 20:22 UTC

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
        self.words = []

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
            if len(node.words) < 5:
                node.words.append(word)
        node.is_word = True
    def query(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        return node.words

