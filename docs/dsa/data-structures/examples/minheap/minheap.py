"""Min heap reference implementation from the min-heap teaching page.

0-based array-backed binary heap with optional satellite data per key.
Matches docs/dsa/data-structures/min-heap/index.md.
"""

from dataclasses import dataclass


@dataclass
class _Entry:
    key: object = None
    value: object = None


class MinHeap:
    """Generic min heap over comparable keys with optional satellite values."""

    def __init__(self, items=None):
        self._data = []
        if items is not None:
            for k in items:
                self._data.append(_Entry(k))
            self.heapify()

    @classmethod
    def from_pairs(cls, pairs):
        h = cls()
        for key, value in pairs:
            h._data.append(_Entry(key, value))
        h.heapify()
        return h

    @classmethod
    def copy_of(cls, other):
        out = cls()
        out._data = [_Entry(e.key, e.value) for e in other._data]
        return out

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def clear(self):
        self._data.clear()

    def peek_min(self):
        if not self._data:
            raise IndexError("peek_min from empty heap")
        return self._data[0].key

    def peek_entry(self):
        if not self._data:
            raise IndexError("peek from empty heap")
        e = self._data[0]
        return e.key, e.value

    def insert(self, key, value=None):
        self._data.append(_Entry(key, value))
        self._sift_up(len(self._data) - 1)

    def extract_min(self):
        key, _ = self.extract_entry()
        return key

    def extract_entry(self):
        if not self._data:
            raise IndexError("extract_min from empty heap")
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return root.key, root.value

    def replace_min(self, key, value=None):
        if not self._data:
            self.insert(key, value)
            return key
        old = self._data[0].key
        self._data[0] = _Entry(key, value)
        self._sift_down(0)
        self._sift_up(0)
        return old

    def decrease_key_at(self, index, new_key):
        if not (0 <= index < len(self._data)):
            raise IndexError(index)
        if new_key > self._data[index].key:
            raise ValueError("new_key must be <= current key for decrease_key")
        self._data[index].key = new_key
        self._sift_up(index)

    def heapify(self):
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    def to_list(self):
        return [e.key for e in self._data]

    def validate(self):
        for i in range(1, len(self._data)):
            p = (i - 1) // 2
            if self._data[p].key > self._data[i].key:
                return False
        return True

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _sift_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self._data[p].key <= self._data[i].key:
                break
            self._data[p], self._data[i] = self._data[i], self._data[p]
            i = p

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            smallest = i
            left = self._left(i)
            right = self._right(i)
            if left < n and self._data[left].key < self._data[smallest].key:
                smallest = left
            if right < n and self._data[right].key < self._data[smallest].key:
                smallest = right
            if smallest == i:
                break
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest

    def __iter__(self):
        for e in self._data:
            yield e.key
