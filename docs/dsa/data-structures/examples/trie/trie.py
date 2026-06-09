"""Trie (prefix tree) mapping string keys to optional payloads."""

from __future__ import annotations

from typing import Any


class TrieNode:
    """One node in a trie."""

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False
        self.value: Any | None = None


class Trie:
    """Prefix tree for string keys.

    Empty string ``""`` is a valid key (it marks the root as a word end).
    Re-inserting an existing key updates ``value`` without changing ``len``.
    """

    def __init__(self) -> None:
        self.root = TrieNode()
        self._size = 0

    def __len__(self) -> int:
        """Return the number of distinct keys stored in the trie."""
        return self._size

    def clear(self) -> None:
        """Remove all keys and reset the trie."""
        self.root = TrieNode()
        self._size = 0

    @staticmethod
    def _validate_key(key: str, *, name: str = 'word') -> None:
        """Raise when ``key`` is not a string."""
        if not isinstance(key, str):
            raise TypeError(
                f'{name} must be str, not {type(key).__name__}',
            )

    def insert(self, word: str, value: Any | None = None) -> None:
        """Insert ``word`` and attach ``value`` at its terminal node.

        If ``word`` is already stored, ``_size`` is unchanged and ``value``
        is replaced.

        Args:
            word: Key to insert. ``""`` marks the root as a word end.
            value: Optional payload stored at the terminal node.
        """
        self._validate_key(word)
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        if not node.is_end:
            self._size += 1
        node.is_end = True
        node.value = value

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Return the node reached by ``prefix``, or ``None`` if missing."""
        self._validate_key(prefix, name='prefix')
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> Any | None:
        """Return the value for ``word``, or ``None`` if absent."""
        self._validate_key(word)
        node = self._find_node(word)
        if node is None or not node.is_end:
            return None
        return node.value

    def contains(self, word: str) -> bool:
        """Return ``True`` when ``word`` is stored as a complete key."""
        self._validate_key(word)
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Return ``True`` when any stored key begins with ``prefix``."""
        self._validate_key(prefix, name='prefix')
        return self._find_node(prefix) is not None

    def _delete_from(
        self,
        node: TrieNode,
        word: str,
        depth: int,
    ) -> tuple[bool, bool]:
        """Remove ``word`` from ``node`` and prune dead branches below it.

        Returns:
            A pair ``(removed, should_prune)``. ``removed`` is ``True`` when
            ``word`` was stored and unmarked. ``should_prune`` tells the parent
            to delete the edge to ``node`` when it is a useless leaf.
        """
        if depth == len(word): 
            if not node.is_end:
                return False, False
            node.is_end = False
            node.value = None
            return True, len(node.children) == 0
        ch = word[depth]
        if ch not in node.children:
            return False, False
        child = node.children[ch]
        removed, should_prune = self._delete_from(child, word, depth + 1)
        if should_prune:
            del node.children[ch]
        return removed, len(node.children) == 0 and not node.is_end

    def delete(self, word: str) -> bool:
        """Remove ``word`` from the trie and prune dead branches.

        Args:
            word: Complete key to remove.

        Returns:
            ``True`` when ``word`` was present and removed, else ``False``.
        """
        self._validate_key(word)  # validate the word
        removed, _ = self._delete_from(self.root, word, 0) # delete the word from the trie
        if removed: # if the word was removed
            self._size -= 1 # decrement the size of the trie
            return True # return True if the word was removed
        return False # return False if the word was not removed

    def collect(self, prefix: str = '') -> list[str]: # collect all the words that start with the prefix
        """Return all stored keys that start with ``prefix``, sorted."""
        self._validate_key(prefix, name='prefix') # validate the prefix
        node = self._find_node(prefix) # find the node for the prefix
        if node is None: # if the node is not found
            return [] # return an empty list
        out: list[str] = [] # initialize an empty list to store the words
        parts: list[str] = list(prefix) # initialize a list to store the parts of the prefix
        self._dfs_words(node, parts, out) # recursively collect the words
        return out

    def collect_values(self, prefix: str = '') -> list[Any]:
        """Return payloads for keys under ``prefix`` in DFS order."""
        self._validate_key(prefix, name='prefix') # validate the prefix
        node = self._find_node(prefix) # find the node for the prefix
        if node is None: # if the node is not found
            return [] # return an empty list
        out: list[Any] = [] # initialize an empty list to store the values
        self._dfs_values(node, out) # recursively collect the values
        return out

    def _dfs_words(
        self,
        node: TrieNode,
        parts: list[str],
        out: list[str],
    ) -> None:
        if node.is_end: # if the node is a word end
            out.append(''.join(parts))
        for ch, child in sorted(node.children.items()):
            parts.append(ch) # add the character to the parts
            self._dfs_words(child, parts, out) # recursively collect the words
            parts.pop() # remove the character from the parts

    def _dfs_values(self, node: TrieNode, out: list[Any]) -> None:
        if node.is_end and node.value is not None: # if the node is a word end and the value is not None
            out.append(node.value) # add the value to the list
        for child in (
            child for _, child in sorted(node.children.items())
        ): # iterate through the children of the node
            self._dfs_values(child, out) # recursively collect the values

    def longest_common_prefix(self) -> str:
        """Return the longest shared prefix of all stored keys."""
        node = self.root
        prefix: list[str] = [] # initialize an empty list to store the prefix
        while len(node.children) == 1 and not node.is_end:
            ch, node = next(iter(node.children.items())) # get the first child of the node
            prefix.append(ch) # add the character to the prefix
        return ''.join(prefix) # return the longest shared prefix
