"""Priority queue reference implementation from the priority-queue teaching page.

Heap-backed max- or min-priority queue with stable tie-breaking, plus an
indexed min-priority queue for decrease-key (Dijkstra).
Matches docs/dsa/data-structures/priority-queue/index.md.
"""

from dataclasses import dataclass


@dataclass
class _PQEntry:
    priority: object = 0.0
    seq: int = 0
    item: object = None


class PriorityQueue:
    """Heap-backed priority queue with optional max- or min-priority ordering."""

    def __init__(self, max_queue=True):
        self._heap = []
        self._seq = 0
        self._max_queue = max_queue

    @classmethod
    def from_pairs(cls, pairs, *, max_queue=True):
        pq = cls(max_queue=max_queue)
        for prio, item in pairs:
            pq.push(item, prio)
        return pq

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return not self._heap

    def clear(self):
        self._heap.clear()
        self._seq = 0

    def push(self, item, priority):
        entry = _PQEntry(priority, self._seq, item)
        self._seq += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        self._swap(0, len(self._heap) - 1)
        entry = self._heap.pop()
        if self._heap:
            self._sift_down(0)
        return entry.item

    def peek(self):
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0].item

    def peek_priority(self):
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0].priority

    def merge(self, other):
        temp = []
        while not other.is_empty():
            temp.append((other.peek_priority(), other.pop()))
        for prio, item in temp:
            self.push(item, prio)

    def _better(self, a, b):
        if self._max_queue:
            if a.priority != b.priority:
                return a.priority > b.priority
        else:
            if a.priority != b.priority:
                return a.priority < b.priority
        return a.seq < b.seq

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self._better(self._heap[p], self._heap[i]):
                break
            self._swap(p, i)
            i = p

    def _sift_down(self, i):
        n = len(self._heap)
        while True:
            best = i
            left = self._left(i)
            right = self._right(i)
            if left < n and self._better(self._heap[left], self._heap[best]):
                best = left
            if right < n and self._better(self._heap[right], self._heap[best]):
                best = right
            if best == i:
                break
            self._swap(i, best)
            i = best

    def __iter__(self):
        for entry in self._heap:
            yield entry.item


class IndexedMinPQ:
    """Min-priority queue with O(log n) decrease-key via id-to-index mapping."""

    def __init__(self, n):
        self._pq = []
        self._qp = [-1] * n
        self._keys = [float("inf")] * n

    def insert(self, i, key):
        self._keys[i] = key
        self._qp[i] = len(self._pq)
        self._pq.append(i)
        self._sift_up(self._qp[i])

    def decrease_key(self, i, key):
        if key >= self._keys[i]:
            return
        self._keys[i] = key
        self._sift_up(self._qp[i])

    def pop_min(self):
        if not self._pq:
            raise IndexError("empty")
        root = self._pq[0]
        self._swap(0, len(self._pq) - 1)
        self._qp[root] = -1
        self._pq.pop()
        if self._pq:
            self._sift_down(0)
        return root, self._keys[root]

    def _better(self, i, j):
        return self._keys[i] < self._keys[j]

    def _swap(self, a, b):
        i, j = self._pq[a], self._pq[b]
        self._pq[a], self._pq[b] = j, i
        self._qp[i], self._qp[j] = b, a

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _sift_up(self, j):
        while j > 0:
            p = self._parent(j)
            if self._better(self._pq[p], self._pq[j]):
                break
            self._swap(p, j)
            j = p

    def _sift_down(self, j):
        n = len(self._pq)
        while True:
            best = j
            left = self._left(j)
            right = self._right(j)
            if left < n and self._better(self._pq[left], self._pq[best]):
                best = left
            if right < n and self._better(self._pq[right], self._pq[best]):
                best = right
            if best == j:
                break
            self._swap(j, best)
            j = best
