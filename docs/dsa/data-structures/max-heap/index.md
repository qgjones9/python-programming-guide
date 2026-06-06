# Max heap

A **complete binary tree** stored in an array where each **parent’s key is ≥ every key in its subtrees** (the **max-heap property**). The largest element always sits at index `0`.

| | |
| --- | --- |
| **What it is** | A binary tree with no gaps in the last level, usually represented as a Python `list` with index formulas instead of child pointers. |
| **Core operations** | `insert`, `extract_max`, `peek_max`, `heapify`—each touches at most tree height O(log n). |
| **When to use** | Top-k temp anomalies, scheduling by priority, building blocks for [heap sort](../heap-sort/index.md) and [priority queues](../priority-queue/index.md). |
| **Trade-off** | No sorted order across the whole array—only the root is guaranteed maximal; `heapq` in Python is a **min-heap** by default. |

In **daily weather data analysis**, a max heap is the right mental model for **“always pull the highest-priority item next”**: the **largest temp anomaly** in a batch review queue, the **highest projected anomaly** among remaining station alerts, or the **largest precipitation deficit** when trimming a forecast simulation window. You will still rank full season tables with **pandas** `sort_values` or **`heapq.nlargest`** in production scripts—implement **`MaxHeap`** here to learn the structure and to pass interviews.

This page is your **ready reference**: array indexing, a complete Python `MaxHeap` class, every way to create a heap, every operation with daily weather examples, and **time and space complexity** on each. For Big-O notation and weather-scale *n*, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How a max heap fits daily weather analysis

| Weather analysis idea | Heap view | Why max at root |
| --- | --- | --- |
| **Top anomaly in a batch** | Root = highest temp anomaly among queued readings | O(1) peek, O(log n) extract |
| **Alert desk urgency** | Priority = severity × station coverage | Always process worst case first |
| **Forecast trim simulation** | Key = precipitation deficit | Repeatedly extract max deficit |
| **Live “most extreme so far”** | Single-element peek while streaming | Compare new reading vs root in O(1) |
| **Heap sort warm-up** | Same array + `sift_down` | [Heap sort](../heap-sort/index.md) drains max to sorted suffix |

**Use `heapq.nlargest` or pandas** when you need top-k from a million-row daily table once. **Use a max heap** when you **interleave inserts and extracts** on a **moderate** in-memory set (simulation, one-month window, teaching).

```mermaid
flowchart TB
  subgraph heap["Max heap as array A"]
    R["A[0] = 3.1 °C anomaly max"]
    R --> L["A[1] = 2.5"]
    R --> RC["A[2] = 2.2"]
    L --> LL["A[3]"]
    L --> LR["A[4]"]
    RC --> RL["A[5]"]
    RC --> RR["A[6]"]
  end
```

Throughout this page, **n** is the number of elements in the heap (e.g. readings in one review batch). **h** = ⌊log₂ n⌋ is tree height. In production weather pipelines, **n** per heap is often moderate while multi-year archives live in tables.

---

## Max heap vs min heap vs sorted list vs `heapq`

| | **Max heap** | **Min heap** | **Sorted `list`** | **`heapq` (stdlib)** |
| --- | --- | --- | --- | --- |
| **Extreme at top** | Maximum | Minimum | Min at `[0]`, max at `[-1]` | Minimum |
| **`insert`** | O(log n) | O(log n) | O(n) insert + keep sorted | O(log n) |
| **`extract_best`** | O(log n) max | O(log n) min | O(1) pop end; O(n) pop front | O(log n) min |
| **`peek`** | O(1) max | O(1) min | O(1) either end | O(1) min |
| **Full order visible** | No | No | Yes | No |
| **Weather default in Python** | Teach / custom | Dijkstra, schedules | Climatology export | `nlargest` via negated keys |

```mermaid
sequenceDiagram
  participant Analyst
  participant H as max heap
  Analyst->>H: insert(anomaly 1.8)
  Analyst->>H: insert(anomaly 3.1)
  Analyst->>H: peek_max → 3.1 O(1)
  Analyst->>H: extract_max → 3.1 O(log n)
  H-->>Analyst: root now next-largest
```

---

## Mental model: complete tree in an array

A **complete** binary tree fills levels left to right—no gaps until the last row. Store it in array `A`:

| Index relation | Formula (0-based) |
| --- | --- |
| **Parent of `i`** | `(i - 1) // 2` for `i > 0` |
| **Left child of `i`** | `2 * i + 1` |
| **Right child of `i`** | `2 * i + 2` |
| **Last parent** | `(n // 2) - 1` when `n > 0` |

**Max-heap property:** for every node `i` (except root’s children logic), `A[parent(i)] ≥ A[i]`.

```mermaid
flowchart LR
  subgraph indices["Array indices"]
    direction TB
    I0["0: 3.1"]
    I1["1: 2.5"]
    I2["2: 2.2"]
    I3["3: 1.8"]
    I4["4: 2.0"]
  end
  I0 --> I1
  I0 --> I2
  I1 --> I3
  I1 --> I4
```

| Step | Cost driver |
| --- | --- |
| One `sift_up` / `sift_down` | O(log n) comparisons/swaps |
| `heapify` all nodes | O(n) — not O(n log n) |

---

## Daily weather data types for examples

```python
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(order=True, slots=True)
class PrioritizedReading:
    neg_anomaly: float
    reading_id: int = field(compare=False)
    summary: str = field(compare=False, default="")


@dataclass(frozen=True, slots=True)
class DailyReading:
    reading_id: int
    month: int
    temp_anomaly: float
    summary: str


@dataclass(frozen=True, slots=True)
class Station:
    name: str
    mean_anomaly: float
    region: str
```

---

## Ways to create a max heap

### 1. Empty `MaxHeap`

```python
heap = MaxHeap()
assert heap.is_empty()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Insert one-by-one (online build)

Each `insert` sift-up—O(log n) per item → **O(n log n)** total for n inserts.

```python
h = MaxHeap()
for reading in window_readings:
    h.insert(reading.temp_anomaly, reading)
```

| | |
| --- | --- |
| **Time** | O(n log n) for n items |
| **Space** | O(n) |

### 3. `heapify` from existing array (offline build)

Floyd’s method: sift-down from last parent to root—**O(n)**.

```python
anomalies = [1.8, 3.1, 2.2, 2.5, 2.0]
h = MaxHeap.from_iterable(anomalies)
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) copy if you keep original |

### 4. Build from list literal inside wrapper

```python
h = MaxHeap([3.1, 2.5, 2.2, 1.8])
```

| | |
| --- | --- |
| **Time** | O(n) after `heapify` |
| **Space** | O(n) |

### 5. Copy from another `MaxHeap`

```python
h2 = MaxHeap.copy_of(h)
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) |

### 6. `heapq` min-heap with negated keys (production idiom)

Python stdlib has **min-heap** only; negate scores for “max” behavior.

```python
import heapq

min_heap: list[tuple[float, DailyReading]] = []
heapq.heappush(min_heap, (-reading.temp_anomaly, reading))
best = heapq.heappop(min_heap)[1]
```

| | |
| --- | --- |
| **Time** | Same O(log n) per op |
| **Space** | O(n) |

```mermaid
flowchart TD
  Q([Need max-heap in Python?])
  Q --> T{Learning / interview?}
  T -->|yes| MH["MaxHeap class on this page"]
  T -->|no| HQ["heapq + negated key or nlargest"]
  Q --> B{Batch build once?}
  B -->|yes| FY["heapify O(n)"]
  B -->|no| INS["insert each O(log n)"]
```

---

## Reference implementation: `MaxHeap`

Generic max heap over comparable keys with optional satellite data (e.g. attach `DailyReading` at each anomaly).

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Entry(Generic[K, V]):
    key: K
    value: V | None = None


class MaxHeap(Generic[K, V]):
    def __init__(self, items: Iterable[K] | None = None) -> None:
        self._data: list[_Entry[K, V]] = []
        if items is not None:
            for k in items:
                self._data.append(_Entry(k))
            self.heapify()

    @classmethod
    def from_pairs(cls, pairs: Iterable[tuple[K, V]]) -> MaxHeap[K, V]:
        h: MaxHeap[K, V] = cls()
        for key, value in pairs:
            h._data.append(_Entry(key, value))
        h.heapify()
        return h

    @classmethod
    def copy_of(cls, other: MaxHeap[K, V]) -> MaxHeap[K, V]:
        out: MaxHeap[K, V] = cls()
        out._data = [_Entry(e.key, e.value) for e in other._data]
        return out

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def clear(self) -> None:
        self._data.clear()

    def peek_max(self) -> K:
        if not self._data:
            raise IndexError("peek_max from empty heap")
        return self._data[0].key

    def peek_entry(self) -> tuple[K, V | None]:
        if not self._data:
            raise IndexError("peek from empty heap")
        e = self._data[0]
        return e.key, e.value

    def insert(self, key: K, value: V | None = None) -> None:
        self._data.append(_Entry(key, value))
        self._sift_up(len(self._data) - 1)

    def extract_max(self) -> K:
        key, _ = self.extract_entry()
        return key

    def extract_entry(self) -> tuple[K, V | None]:
        if not self._data:
            raise IndexError("extract_max from empty heap")
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return root.key, root.value

    def replace_max(self, key: K, value: V | None = None) -> K:
        if not self._data:
            self.insert(key, value)
            return key
        old = self._data[0].key
        self._data[0] = _Entry(key, value)
        self._sift_down(0)
        self._sift_up(0)
        return old

    def increase_key_at(self, index: int, new_key: K) -> None:
        if not (0 <= index < len(self._data)):
            raise IndexError(index)
        if new_key < self._data[index].key:
            raise ValueError("new_key must be >= current key for increase_key")
        self._data[index].key = new_key
        self._sift_up(index)

    def heapify(self) -> None:
        n = len(self._data)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    def to_list(self) -> list[K]:
        return [e.key for e in self._data]

    def validate(self) -> bool:
        for i in range(1, len(self._data)):
            p = (i - 1) // 2
            if self._data[p].key < self._data[i].key:
                return False
        return True

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = self._parent(i)
            if self._data[p].key >= self._data[i].key:
                break
            self._data[p], self._data[i] = self._data[i], self._data[p]
            i = p

    def _sift_down(self, i: int) -> None:
        n = len(self._data)
        while True:
            largest = i
            left = self._left(i)
            right = self._right(i)
            if left < n and self._data[left].key > self._data[largest].key:
                largest = left
            if right < n and self._data[right].key > self._data[largest].key:
                largest = right
            if largest == i:
                break
            self._data[i], self._data[largest] = self._data[largest], self._data[i]
            i = largest

    def __iter__(self) -> Iterator[K]:
        for e in self._data:
            yield e.key
```

| | |
| --- | --- |
| **Time** | See per-operation table below |
| **Space** | O(n) for n stored keys |

---

## Core helpers: `sift_up` and `sift_down`

### `sift_up(i)` — after insert at leaf

Bubble node at `i` toward root while it is larger than its parent.

```python
h = MaxHeap()
h.insert(1.8)
h.insert(3.1)
assert h.peek_max() == 3.1
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

```mermaid
sequenceDiagram
  participant A as array
  Note over A: new 3.1 at leaf
  A->>A: compare with parent, swap up
  A->>A: repeat until parent >= 3.1
```

---

### `sift_down(i)` — after extract or heapify step

Push node at `i` down by swapping with larger child until both children ≤ it.

```python
h = MaxHeap([3.1, 2.5, 2.2, 1.8])
h.extract_max()
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

---

### `heapify()` — O(n) build

```python
anomalies = [0.4, -1.2, 0.8, 0.1, 0.9, -0.3]
h = MaxHeap(anomalies)
assert h.validate()
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) auxiliary |

**Why O(n)?** Most nodes are near leaves; few sift-down steps reach full height. Sum of work is linear (CLRS aggregate analysis).

---

## All operations (with examples and complexity)

```mermaid
flowchart TB
  subgraph o1["O(1)"]
    peek["peek_max"]
    len_op["len / is_empty"]
  end
  subgraph olog["O(log n)"]
    insert
    extract["extract_max"]
    replace["replace_max"]
    increase["increase_key_at"]
  end
  subgraph on["O(n)"]
    heapify
    validate
    copy["copy_of"]
  end
```

### `insert(key, value=None)`

```python
review = MaxHeap.from_pairs([])
review.insert(0.42, DailyReading(101, 2, 0.42, "partly cloudy"))
review.insert(0.91, DailyReading(102, 2, 0.91, "cold front"))
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) aux; O(1) amortized array growth |

Stream readings into a “most extreme so far” structure during a live anomaly recap.

---

### `peek_max()` / `peek_entry()`

```python
best_anomaly = review.peek_max()
key, reading = review.peek_entry()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

Does not remove—safe to inspect before committing extract in a UI.

---

### `extract_max()` / `extract_entry()`

```python
while not review.is_empty():
    anomaly, reading = review.extract_entry()
    print(reading.summary, anomaly)
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

Drain queue from highest anomaly downward—same order as repeated max selection; n extracts total O(n log n).

---

### `replace_max(key, value=None)`

Pop-max + push combined—one sift-up and sift-down path from root.

```python
stream = MaxHeap([0.5])
old = stream.replace_max(0.9, DailyReading(1, 1, 0.9, "heat spike"))
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

Useful when sliding window max changes by one new candidate per step.

---

### `increase_key_at(index, new_key)`

Decrease-key is harder without extra indirection; increase-key is O(log n) sift-up.

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

Production heaps often store **`(key, id)`** with a **`id → index`** map for arbitrary delete/decrease—see [Priority queue](../priority-queue/index.md).

---

### `heapify()` / `MaxHeap(iterable)`

```python
week_anomalies = [0.12, 0.44, 0.31, 0.08, 0.55]
h = MaxHeap(week_anomalies)
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) storage |

Prefer **`heapify`** over n separate **`insert`** calls when all data is known upfront.

---

### `len(heap)` / `is_empty()` / `clear()`

| Operation | Time | Space |
| --- | --- | --- |
| `len` / `is_empty` | O(1) | O(1) |
| `clear` | O(1) drop refs | O(1) |

---

### `validate()` — debug heap property

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

---

### `to_list()` — unordered key snapshot

Array is **not** sorted; only root is max.

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) |

---

## Daily weather patterns with max heaps

### Top-k temp anomalies without full sort

```python
import heapq


def top_k_anomalies(readings: list[DailyReading], k: int) -> list[DailyReading]:
    heap: list[tuple[float, DailyReading]] = []
    for r in readings:
        if len(heap) < k:
            heapq.heappush(heap, (r.temp_anomaly, r))
        elif r.temp_anomaly > heap[0][0]:
            heapq.heapreplace(heap, (r.temp_anomaly, r))
    return [r for _, r in sorted(heap, reverse=True)]


def top_k_maxheap(readings: list[DailyReading], k: int) -> list[DailyReading]:
    h = MaxHeap.from_pairs((r.temp_anomaly, r) for r in readings)
    out: list[DailyReading] = []
    for _ in range(min(k, len(h))):
        _, reading = h.extract_entry()
        out.append(reading)
    return out
```

| Approach | Time | Space |
| --- | --- | --- |
| **`heapq` size-k min-heap** | O(n log k) | O(k) |
| **Extract k from max heap** | O(n + k log n) | O(n) |
| **`nlargest(k, readings, key=lambda r: r.temp_anomaly)`** | O(n log k) | O(k) |

For large *n*, prefer **`nlargest`**. For streaming with unknown length, size-k heap wins.

---

### Merge two sorted monthly anomaly lists (heap merge)

When merging many sorted streams, a min-heap of stream heads is classic—max-heap if you want descending merge.

```python
def merge_desc(list_a: list[float], list_b: list[float]) -> list[float]:
    h = MaxHeap(list_a + list_b)
    out: list[float] = []
    while not h.is_empty():
        out.append(h.extract_max())
    return out
```

| | |
| --- | --- |
| **Time** | O(n log n) naive one-heap |
| **Space** | O(n) |

---

### Running station-priority simulation

```python
def select_top_stations(stations: list[Station], keep: int) -> list[Station]:
    h = MaxHeap.from_pairs((s.mean_anomaly, s) for s in stations)
    kept: list[Station] = []
    for _ in range(min(keep, len(h))):
        _, station = h.extract_entry()
        kept.append(station)
    return kept
```

| | |
| --- | --- |
| **Time** | O(n log n) |
| **Space** | O(n) |

---

## Array max heap vs pointer-based tree

| | **Array heap** | **Explicit tree nodes** |
| --- | --- | --- |
| **Memory** | Compact; no child pointers | Extra `left`/`right` refs |
| **Index math** | Required | Follow pointers |
| **Cache** | Better locality | Pointer chasing |
| **Interview / CLRS** | Default | Rare |
| **Weather scripts** | `heapq` uses array | Custom tree almost never |

```mermaid
flowchart LR
  subgraph arr["Array (used here)"]
    A0["0"] --- A1["1"] --- A2["2"]
  end
  subgraph tree["Same tree logically"]
    R --> L
    R --> R2["right"]
  end
```

---

## Python stdlib: `heapq` patterns

| Need | API |
| --- | --- |
| K smallest times | `heapq.nsmallest(k, xs)` |
| K largest anomalies | `heapq.nlargest(k, readings, key=lambda r: r.temp_anomaly)` |
| Max via min-heap | Push `(-anomaly, reading)` |
| In-place min-heapify | `heapq.heapify(lst)` |
| Push / pop | `heappush`, `heappop` |

```python
import heapq

h: list[tuple[float, DailyReading]] = []
heapq.heappush(h, (-reading.temp_anomaly, reading))
neg_anomaly, best = heapq.heappop(h)
actual_anomaly = -neg_anomaly
```

**Rule of thumb:** ship **`heapq`** in production weather notebooks; implement **`MaxHeap`** to learn and debug heap property.

---

## Master complexity table

Let **n** = heap size, **k** = number of extracts.

| Operation | Time | Space (auxiliary) | Notes |
| --- | --- | --- | --- |
| Create empty | O(1) | O(1) | |
| `insert` | O(log n) | O(1) | sift-up |
| `extract_max` | O(log n) | O(1) | sift-down |
| `peek_max` | O(1) | O(1) | |
| `replace_max` | O(log n) | O(1) | |
| `increase_key_at` | O(log n) | O(1) | |
| `heapify` n items | O(n) | O(1) | Floyd |
| n inserts (online) | O(n log n) | O(n) | |
| Extract all n | O(n log n) | O(1) per step | |
| `validate` | O(n) | O(1) | |
| `copy_of` | O(n) | O(n) | |
| Top-k via size-k heap | O(n log k) | O(k) | stdlib pattern |

**Storage:** Θ(n) array entries.

---

## When to pick which tool (weather context)

```mermaid
flowchart TD
  Q([What is the job?])
  Q --> F{Full sorted export?}
  F -->|yes| SORT["sort_values / sorted"]
  F -->|no| K{Only top k?}
  K -->|yes| NL["heapq.nlargest"]
  K -->|no| S{Streaming insert+extract?}
  S -->|yes| HEAP["MaxHeap / heapq"]
  S -->|no| LIST["scan once O(n)"]
```

| Scenario | Best tool |
| --- | --- |
| Season anomaly leaderboard CSV | pandas sort |
| Top 10 readings one month | `nlargest(10, ...)` |
| Interactive priority queue | [Priority queue](../priority-queue/index.md) |
| Guaranteed in-place O(n log n) sort | [Heap sort](../heap-sort/index.md) |
| Learn heap property | `MaxHeap` on this page |

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Confusing min-heap and max-heap | Wrong extrema | Python `heapq` is min; negate or use this class |
| Assuming array is sorted | Only root is max | Full sort is different algorithm |
| Off-by-one in child indices | Corrupt tree | Use `2*i+1`, `2*i+2`, check bounds |
| `extract_max` on empty | `IndexError` | Check `is_empty()` |
| n inserts when `heapify` possible | O(n log n) vs O(n) | Batch `heapify` |
| Decrease-key without index map | O(n) search | Locator map in priority queue |
| Using heap for one-shot full sort | Constants worse than Timsort | `list.sort` in apps |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Priority queue](../priority-queue/index.md) | ADT backed by heap |
| [Linked list](../linked-list/index.md) | Pointer structures vs array heap |
| [Circularly linked list](../circularly-linked-list/index.md) | Ring buffers vs heap priority |
| [Heap sort (data structures)](../heap-sort/index.md) | Sort via heap |
| [Heap sort (algorithms)](../../algorithms/heap-sort/index.md) | Algorithm-focused page |
| [Treaps](../treaps/index.md) | BST + heap priority |
| [Binary search tree](../binary-search-tree/index.md) | Full ordering |
| [Complexity analysis](../../complexity/index.md) | Big-O reference |

---

## Quick reference card

```python
h = MaxHeap()
h = MaxHeap([3.1, 2.5, 2.2])
h = MaxHeap.from_pairs((r.temp_anomaly, r) for r in readings)

h.insert(0.91, reading)
anomaly = h.extract_max()
_, reading = h.extract_entry()

best = h.peek_max()

h.heapify()

import heapq
heapq.nlargest(10, readings, key=lambda r: r.temp_anomaly)
```

Use a **max heap** when you need **repeated access to the current maximum** with **interleaved inserts**—anomaly review queues, simulation priorities, and the foundation of **heap sort**. Reach for **`heapq.nlargest`** and **pandas** when the job is **one-shot analytics** on big tables.

**Weather pipeline checklist**

1. **One-shot top-k** — `heapq.nlargest` or `df.nlargest`.
2. **Streaming priority** — max heap or [priority queue](../priority-queue/index.md).
3. **Batch known set** — `heapify` O(n), not n inserts.
4. **Python default** — min-heap; negate keys for max behavior.
5. **Full ordering** — sort, not heap drain.
