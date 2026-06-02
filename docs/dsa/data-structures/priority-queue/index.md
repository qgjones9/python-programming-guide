# Priority queue

An **abstract data type (ADT)** that always returns the element with the **highest priority** next—regardless of arrival order. It is **not** a FIFO [queue](../queue/index.md); it is a **bag ordered by priority**.

| | |
| --- | --- |
| **What it is** | `insert` any time; `extract_best` removes and returns the highest-priority item; optional `peek`, `decrease_priority`, `merge`. |
| **Core operations** | `push` / `insert`, `pop` / `extract_best`, `peek`—typically O(log n) with a binary heap. |
| **When to use** | Injury urgency, play-review scheduling, Dijkstra on stadium graphs, A* on route trees, event simulation. |
| **Trade-off** | No time-order fairness; two items with equal priority need a tie-break policy. |

In **NFL data analysis**, a priority queue models **“work the most important item next”**: queue **challenge reviews** by win-probability swing, schedule **film-cut exports** by coach urgency, or drive **Dijkstra** on a **stadium concourse graph** for fan walk-time estimates. Live play ingestion order stays FIFO ([Queue](../queue/index.md)); priority queues reorder by **score**, not **clock**.

This page is your **ready reference**: ADT contract, heap-backed and `heapq` implementations, every way to create a PQ, every operation with NFL examples, and **time and space complexity**. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How a priority queue fits NFL-shaped problems

| NFL idea | Priority key | Operation |
| --- | --- | --- |
| **Challenge review queue** | Absolute WPA swing | `extract_best` = most impactful |
| **Injury desk** | Severity × snap share | Highest risk first |
| **Waiver wire alerts** | Projected PPR delta | Pop best add |
| **Graph: shortest path** | Tentative distance | Min-priority queue in Dijkstra |
| **Live “next clip to render”** | Coach star rating | Push new; pop best |

**Use a FIFO queue** when fairness is **first submitted, first processed**. **Use a priority queue** when **importance** dominates **arrival time**.

```mermaid
flowchart TB
  subgraph pq["Priority queue — not FIFO"]
    IN1["push: review A prio 3"] --> HEAP
    IN2["push: review B prio 9"] --> HEAP
    IN3["push: review C prio 5"] --> HEAP
    HEAP["internal heap"]
    HEAP --> OUT["pop → B (9)"]
  end
```

Throughout this page, **n** is the number of items in the queue.

---

## Priority queue vs queue vs max heap vs sorted list

| | **Priority queue (ADT)** | [Queue (FIFO)](../queue/index.md) | [Max heap](../max-heap/index.md) | **Sorted list** |
| --- | --- | --- | --- | --- |
| **Next out** | Best priority | Oldest | Max key | Either end |
| **Arrival order** | Ignored for order | Sacred | Ignored | Ignored |
| **Implementation** | Often binary heap | deque / linked | Concrete structure | list |
| **`insert`** | O(log n) typical | O(1) | O(log n) | O(n) |
| **`extract_best`** | O(log n) | O(1) dequeue | O(log n) | O(1) pop |
| **NFL fit** | Review urgency | Play stream | Same as PQ backend | Static leaderboard |

```mermaid
sequenceDiagram
  participant Coach
  participant PQ as priority queue
  Coach->>PQ: push(review, prio=2)
  Coach->>PQ: push(review, prio=8)
  Coach->>PQ: pop → prio 8 first
  Note over Coach,PQ: FIFO queue would pop prio 2 first
```

---

## Mental model: ADT vs implementation

The **ADT** is the contract:

- **`push(item, priority)`** — add without specifying position.
- **`pop()`** — remove and return highest-priority item.
- **`peek()`** — inspect best without removing.
- Optional: **`decrease_priority(id, new_prio)`**, **`remove(id)`**, **`merge(other)`**.

The **implementation** is usually a **[max heap](../max-heap/index.md)** (max-priority) or **min heap** (min-priority for Dijkstra). Python **`heapq`** implements a **min-heap**; store negated priorities for max behavior.

```mermaid
flowchart LR
  ADT["PriorityQueue ADT"] --> IMPL["Binary heap array"]
  IMPL --> SU["sift_up on push"]
  IMPL --> SD["sift_down on pop"]
```

| Step | Cost driver |
| --- | --- |
| Push | O(log n) sift-up |
| Pop | O(log n) sift-down |
| Peek | O(1) at root |

---

## NFL data types for examples

```python
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(order=True, slots=True)
class ReviewTask:
    """Lower priority value = more urgent if using min-heap; we use negated WPA for max-heap demos."""
    neg_wpa_swing: float
    play_id: int = field(compare=False)
    coach: str = field(compare=False, default="")


@dataclass(frozen=True, slots=True)
class Snap:
    play_id: int
    epa: float
    description: str


@dataclass(frozen=True, slots=True)
class InjuryReport:
    player: str
    severity: int  # 1–10
    snap_pct: float
```

---

## Ways to create a priority queue

### 1. Empty heap-backed `PriorityQueue`

```python
pq = PriorityQueue()
assert pq.is_empty()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. From iterable of `(priority, item)` pairs

```python
tasks = [(8.0, ReviewTask(-8.0, 101)), (3.0, ReviewTask(-3.0, 102))]
pq = PriorityQueue.from_pairs(tasks, max_queue=True)
```

| | |
| --- | --- |
| **Time** | O(n) heapify |
| **Space** | O(n) |

### 3. `heapq` list as min-priority queue

```python
import heapq

pq: list[tuple[float, int, Snap]] = []
counter = 0  # tie-break for stable-ish order

def push(snap: Snap, priority: float) -> None:
    global counter
    heapq.heappush(pq, (priority, counter, snap))
    counter += 1
```

| | |
| --- | --- |
| **Time** | O(log n) per push |
| **Space** | O(n) |

### 4. `queue.PriorityQueue` (thread-safe, blocking)

```python
from queue import PriorityQueue as ThreadSafePQ

tpq: ThreadSafePQ[tuple[float, Snap]] = ThreadSafePQ()
tpq.put((7.5, snap))
item = tpq.get()
```

| | |
| --- | --- |
| **Time** | O(log n) typical |
| **Space** | O(n) |

### 5. Lazy deletion heap (handles arbitrary remove)

Store `(priority, id, item)`; mark ids deleted in a set; pop until valid top.

| | |
| --- | --- |
| **Time** | O(log n) amortized push/pop |
| **Space** | O(n) + deleted set |

```mermaid
flowchart TD
  Q([Create priority queue?])
  Q --> T{Thread-safe?}
  T -->|yes| TPQ["queue.PriorityQueue"]
  T -->|no| L{Max or min priority?}
  L -->|max| MH["MaxHeap / negated heapq"]
  L -->|min| HQ["heapq min-heap"]
  Q --> D{Need decrease-key?}
  D -->|yes| IDX["heap + id→index map"]
  D -->|no| SIMPLE["simple heap"]
```

---

## Reference implementation: `PriorityQueue` (max-priority)

Wraps the same array heap as [Max heap](../max-heap/index.md) with ADT naming and tie-break counter for stable ordering among equal priorities.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


@dataclass
class _PQEntry(Generic[T]):
    priority: float
    seq: int  # tie-break: lower seq first among equal priority
    item: T


class PriorityQueue(Generic[T]):
    """Max-priority queue: highest priority pops first."""

    def __init__(self, max_queue: bool = True) -> None:
        self._heap: list[_PQEntry[T]] = []
        self._seq = 0
        self._max_queue = max_queue

    @classmethod
    def from_pairs(
        cls, pairs: Iterable[tuple[float, T]], *, max_queue: bool = True
    ) -> PriorityQueue[T]:
        pq: PriorityQueue[T] = cls(max_queue=max_queue)
        for prio, item in pairs:
            pq.push(item, prio)
        return pq

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return not self._heap

    def clear(self) -> None:
        self._heap.clear()
        self._seq = 0

    def push(self, item: T, priority: float) -> None:
        entry = _PQEntry(priority, self._seq, item)
        self._seq += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> T:
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        self._swap(0, len(self._heap) - 1)
        entry = self._heap.pop()
        if self._heap:
            self._sift_down(0)
        return entry.item

    def peek(self) -> T:
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0].item

    def peek_priority(self) -> float:
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0].priority

    def merge(self, other: PriorityQueue[T]) -> None:
        """Merge all items from other into self — O(n log n) naive."""
        while not other.is_empty():
            item = other.pop()
            prio = other._heap[0].priority if other._heap else 0.0  # wrong after pop
        # Correct merge: drain with peek_priority before pop
        temp: list[tuple[float, T]] = []
        while not other.is_empty():
            temp.append((other.peek_priority(), other.pop()))
        for prio, item in temp:
            self.push(item, prio)

    def _better(self, a: _PQEntry[T], b: _PQEntry[T]) -> bool:
        if self._max_queue:
            if a.priority != b.priority:
                return a.priority > b.priority
        else:
            if a.priority != b.priority:
                return a.priority < b.priority
        return a.seq < b.seq

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = self._parent(i)
            if self._better(self._heap[p], self._heap[i]):
                break
            self._swap(p, i)
            i = p

    def _sift_down(self, i: int) -> None:
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

    def __iter__(self) -> Iterator[T]:
        for e in self._heap:
            yield e.item
```

| | |
| --- | --- |
| **Time** | See operation table |
| **Space** | O(n) |

---

## Indexed priority queue (decrease-key)

For Dijkstra and schedulers that **improve** a vertex’s distance, keep **`id → heap index`** and sift after update.

```python
class IndexedMinPQ:
    """Min-priority queue with decrease-key. Keys are distances; ids are vertex ints."""

    def __init__(self, n: int) -> None:
        self._pq: list[int] = []  # heap of vertex ids
        self._qp: list[int] = [-1] * n  # id -> index in _pq, -1 absent
        self._keys: list[float] = [float("inf")] * n

    def insert(self, i: int, key: float) -> None:
        self._keys[i] = key
        self._qp[i] = len(self._pq)
        self._pq.append(i)
        self._sift_up(self._qp[i])

    def decrease_key(self, i: int, key: float) -> None:
        if key >= self._keys[i]:
            return
        self._keys[i] = key
        self._sift_up(self._qp[i])

    def pop_min(self) -> tuple[int, float]:
        if not self._pq:
            raise IndexError("empty")
        root = self._pq[0]
        self._swap(0, len(self._pq) - 1)
        self._qp[root] = -1
        self._pq.pop()
        if self._pq:
            self._sift_down(0)
        return root, self._keys[root]

    def _better(self, i: int, j: int) -> bool:
        return self._keys[i] < self._keys[j]

    def _swap(self, a: int, b: int) -> None:
        i, j = self._pq[a], self._pq[b]
        self._pq[a], self._pq[b] = j, i
        self._qp[i], self._qp[j] = b, a

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, j: int) -> None:
        while j > 0:
            p = self._parent(j)
            if self._better(self._pq[p], self._pq[j]):
                break
            self._swap(p, j)
            j = p

    def _sift_down(self, j: int) -> None:
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
```

| Operation | Time | Space |
| --- | --- | --- |
| `insert` | O(log n) | O(1) |
| `decrease_key` | O(log n) | O(1) |
| `pop_min` | O(log n) | O(1) |

**NFL graph example:** stadium nodes = gates; edge weight = walk seconds; Dijkstra pops min distance next.

---

## All operations (with examples and complexity)

```mermaid
flowchart TB
  subgraph o1["O(1)"]
    peek
    len_op["len / is_empty"]
  end
  subgraph olog["O(log n)"]
    push
    pop
    decrease["decrease_key"]
  end
```

### `push(item, priority)`

```python
reviews = PriorityQueue[ReviewTask]()
reviews.push(ReviewTask(-9.0, 4021, "Reid"), priority=9.0)
reviews.push(ReviewTask(-3.0, 4018, "Reid"), priority=3.0)
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) aux |

---

### `pop()` — extract highest priority

```python
urgent = reviews.pop()  # WPA swing 9.0 task first
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

```mermaid
sequenceDiagram
  participant PQ as priority queue
  PQ->>PQ: swap root with last
  PQ->>PQ: sift_down root
  PQ-->>Analyst: return best item
```

---

### `peek()` / `peek_priority()`

```python
next_review = reviews.peek()
prio = reviews.peek_priority()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

---

### `decrease_key` / `increase_key` (indexed PQ)

When a play’s WPA estimate improves, update its priority without re-inserting duplicate.

| | |
| --- | --- |
| **Time** | O(log n) with index map |
| **Space** | O(n) for `qp` array |

Plain heap without locator: **O(n)** find + delete + insert.

---

### `merge(other)`

Combine two queues—naive: pop all from `other` and push into `self`.

| | |
| --- | --- |
| **Time** | O(n log n) naive; O(n) with mergeable heaps (advanced) |
| **Space** | O(1) aux per item moved |

---

### `len(pq)` / `is_empty()` / `clear()`

| Operation | Time | Space |
| --- | --- | --- |
| `len` / `is_empty` | O(1) | O(1) |
| `clear` | O(1) | O(1) |

---

## Min-priority vs max-priority

| Variant | Root holds | Typical algorithm |
| --- | --- | --- |
| **Max-priority** | Largest key | Challenge urgency, `nlargest` streaming |
| **Min-priority** | Smallest key | Dijkstra, A*, `nsmallest` |

```python
# Min-priority with heapq (distance, node_id)
import heapq

dist_pq: list[tuple[float, int]] = []
heapq.heappush(dist_pq, (0.0, start_node))
d, u = heapq.heappop(dist_pq)
```

Toggle `max_queue=False` on `PriorityQueue` or negate priorities for max behavior on min-heap.

---

## NFL patterns with priority queues

### Challenge review desk

```python
def process_reviews(tasks: list[tuple[float, ReviewTask]]) -> list[ReviewTask]:
    pq = PriorityQueue.from_pairs(tasks)
    done: list[ReviewTask] = []
    while not pq.is_empty():
        done.append(pq.pop())
    return done
```

| | |
| --- | --- |
| **Time** | O(n log n) |
| **Space** | O(n) |

---

### Dijkstra on concourse graph (min-priority)

```python
def dijkstra(adj: dict[int, list[tuple[int, float]]], start: int, n: int) -> list[float]:
    dist = [float("inf")] * n
    dist[start] = 0.0
    pq = IndexedMinPQ(n)
    pq.insert(start, 0.0)
    while True:
        try:
            u, du = pq.pop_min()
        except IndexError:
            break
        if du > dist[u]:
            continue
        for v, w in adj.get(u, []):
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if pq._qp[v] < 0:
                    pq.insert(v, nd)
                else:
                    pq.decrease_key(v, nd)
    return dist
```

| | |
| --- | --- |
| **Time** | O((V + E) log V) with binary heap |
| **Space** | O(V) |

**NFL:** nodes = gates/sections; weights = walk time—**not** play data, but same PQ machinery in venue apps.

---

### Top-k waiver targets (max-priority, size cap)

Same as [Max heap](../max-heap/index.md) size-k pattern—PQ language emphasizes **pop best** repeatedly.

```python
import heapq


def best_waiver_adds(candidates: list[tuple[float, str]], k: int) -> list[str]:
    """Min-heap of size k holding negated PPR — O(n log k)."""
    heap: list[tuple[float, str]] = []
    for ppr, name in candidates:
        if len(heap) < k:
            heapq.heappush(heap, (ppr, name))
        elif ppr > heap[0][0]:
            heapq.heapreplace(heap, (ppr, name))
    return [name for _, name in sorted(heap, reverse=True)]
```

| | |
| --- | --- |
| **Time** | O(n log k) |
| **Space** | O(k) |

---

### Event simulation (kickoff timeline)

```python
@dataclass(order=True)
class Event:
    time: float
    kind: str = field(compare=False)

events = PriorityQueue[Event](max_queue=False)  # min on time
events.push(Event(0.0, "kickoff"), priority=0.0)
events.push(Event(900.0, "halftime"), priority=900.0)
next_ev = events.pop()
```

| | |
| --- | --- |
| **Time** | O(log n) per event |
| **Space** | O(n) |

---

## Implementation comparison

| Backend | push | pop | decrease-key | Notes |
| --- | --- | --- | --- | --- |
| **Binary heap** | O(log n) | O(log n) | O(log n) indexed | Default |
| **Sorted list** | O(n) | O(1) | O(n) | Small n only |
| **Fibonacci heap** | O(1) amortized | O(log n) | O(1) amortized | Theory; rare in Python |
| **`heapq` + lazy delete** | O(log n) | O(log n) amortized | O(1) mark | Simple invalidation |

```mermaid
flowchart TD
  Q([n items, m operations?])
  Q --> S{n < 50?}
  S -->|yes| SL["sorted list OK"]
  S -->|no| H["binary heap"]
  H --> D{decrease-key heavy?}
  D -->|yes| IDX["indexed heap"]
  D -->|no| HQ["heapq"]
```

---

## Python stdlib: what to use

| Need | API |
| --- | --- |
| Min-priority in scripts | `heapq.heappush` / `heappop` |
| Thread-safe PQ | `queue.PriorityQueue` |
| Max-priority | Negate key or custom `PriorityQueue` |
| Top-k only | `heapq.nlargest` |
| Async scheduling | `asyncio.PriorityQueue` |

```python
import asyncio

async def schedule():
    apq: asyncio.PriorityQueue[tuple[int, str]] = asyncio.PriorityQueue()
    await apq.put((1, "snap transcode"))
```

---

## Master complexity table

| Operation | Binary heap | Indexed heap | Sorted list |
| --- | --- | --- | --- |
| `push` | O(log n) | O(log n) | O(n) |
| `pop` | O(log n) | O(log n) | O(1) |
| `peek` | O(1) | O(1) | O(1) |
| `decrease_key` | — | O(log n) | O(n) |
| Build from n pairs | O(n) heapify | O(n log n) inserts | O(n²) |
| Dijkstra | O((V+E) log V) | Same | Impractical |

**Storage:** Θ(n) for n queued items.

---

## When to pick which structure (NFL context)

```mermaid
flowchart TD
  Q([Process order?])
  Q --> F{Fair arrival order?}
  F -->|yes| FIFO["Queue / deque"]
  F -->|no| P{By score / distance?}
  P -->|yes| PQ["Priority queue"]
  P -->|no| L["list scan"]
```

| Scenario | Best tool |
| --- | --- |
| Live play feed | [Queue](../queue/index.md) |
| Challenge urgency | Priority queue |
| Shortest path in graph | Min indexed PQ |
| Static season ranks | pandas sort |
| Top 10 only | `nlargest` |

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Using PQ for FIFO plays | Starvation of early items | Use [Queue](../queue/index.md) |
| Equal priorities undefined | Non-deterministic pop order | Tie-break with `seq` counter |
| `heapq` max without negation | Pops minimum | Negate or `max_queue=True` |
| Stale entries after decrease-key | Wrong pop | Indexed PQ or lazy deletion |
| Comparing non-orderable items | TypeError | Store `(priority, seq, item)` |
| Fibonacci heap in Python | Over-engineering | Binary heap + `heapq` |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Max heap](../max-heap/index.md) | Typical implementation |
| [Queue](../queue/index.md) | FIFO, not priority |
| [Heap sort](heap-sort/index.md) | Repeated extract |
| [Graphs](../graphs/index.md) | Dijkstra uses min-PQ |
| [Complexity analysis](../../complexity/index.md) | Big-O reference |

---

## Quick reference card

```python
# max-priority ADT
pq = PriorityQueue[ReviewTask]()
pq.push(task, priority=9.0)
best = pq.pop()
top = pq.peek()

# min-priority (Dijkstra)
import heapq
heapq.heappush(pq_list, (dist, node))

# indexed decrease-key
ipq = IndexedMinPQ(n_vertices)
ipq.insert(v, key)
ipq.decrease_key(v, new_key)
v, d = ipq.pop_min()

# production top-k
heapq.nlargest(10, players, key=lambda p: p.ppr)
```

Use a **priority queue** when **importance or distance** determines **who goes next**—challenge desks, graph algorithms, and schedulers. Use a **FIFO queue** for **play streams**; use **sort** for **full static leaderboards**.

**NFL pipeline checklist**

1. **Live ingest order** — [Queue](../queue/index.md), not PQ.
2. **Urgent reviews** — max-priority queue with WPA key.
3. **Graph walk times** — min indexed priority queue.
4. **Tie equal priorities** — monotonic sequence counter.
5. **Top-k only** — `heapq.nlargest`, not full PQ drain.
