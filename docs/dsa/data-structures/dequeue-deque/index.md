# Dequeue (deque)

A **double-ended queue** (“deck”): insert and remove at **both** front and back in O(1) time with a high-quality implementation. It generalizes both a [stack](../stacks/index.md) (LIFO at one end) and a [queue](../queue/index.md) (FIFO when you use opposite ends consistently).

| | |
| --- | --- |
| **What it is** | Push/pop at left and right; in Python, `collections.deque` is the standard realization. |
| **Core operations** | `append`, `appendleft`, `pop`, `popleft`, plus `extend`, `rotate`, `maxlen`. |
| **When to use** | Sliding anomaly windows, palindrome checks, BFS with push-front, steal-from-both-ends algorithms, bounded live buffers. |
| **Note** | Pronounced “deck.” Not the verb *dequeue* alone—that usually means remove from a [queue](../queue/index.md). |

In **daily weather data analysis**, `deque` is the workhorse for **bounded memory**: last *k* days’ temp anomalies, rolling precipitation windows, a **queue** of export jobs at the back while high-priority backfills `appendleft`, or rotating a small list of **station candidates** on a dashboard. You get O(1) at both ends without implementing a [doubly linked list](../doubly-linked-list/index.md) in pure Python.

This page is your **ready reference**: full `collections.deque` API with weather examples, hand-rolled deque ADT, complexity on every operation, and when deque beats `list`. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## Deque vs list vs linked structures

| | **`collections.deque`** | **Python `list`** | **Doubly linked list** |
| --- | --- | --- | --- |
| **Append left/right** | O(1) | O(1) right; **O(n) left** `insert(0)` | O(1) with pointers |
| **Pop left/right** | O(1) | O(1) right; **O(n) left** `pop(0)` | O(1) |
| **Index `d[i]`** | O(n) | O(1) | O(n) |
| **Slice** | No | Yes | No |
| **maxlen ring** | Built-in | Manual | Manual |
| **Weather default** | Live windows, FIFO | Column access, stats | Teaching / interviews |

```mermaid
flowchart LR
  LF["left front"] <--> D["deque blocks"]
  D <--> RR["right rear"]
  AL["appendleft"] --> LF
  AR["append"] --> RR
  PL["popleft"] --> LF
  PR["pop"] --> RR
```

Throughout this page, **n** is `len(d)`.

---

## Daily weather analysis: what a deque models

| Weather idea | Deque pattern | API sketch |
| --- | --- | --- |
| **Last 10 days anomaly** | `deque(maxlen=10)` | auto-drop oldest on `append` |
| **FIFO reading queue** | `append` + `popleft` | [Queue](../queue/index.md) |
| **Undo at stack end** | `append` + `pop` | [Stack](../stacks/index.md) |
| **Insert urgent backfill front** | `appendleft` | priority front without full heap |
| **Rotate station list** | `rotate(1)` | climatology UI carousel |
| **Palindrome condition sequence** | pop both ends | `"dry-wet-wet-dry"` style checks |

```python
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class DailyReading:
    reading_id: int
    temp_anomaly: float
    summary: str


@dataclass(frozen=True)
class Station:
    station_id: str
    name: str
```

---

## Ways to create a deque in Python

### 1. Empty `deque`

```python
from collections import deque

d: deque[DailyReading] = deque()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) empty |

### 2. From iterable (readings in chronological order)

```python
d = deque([
    DailyReading(1, 0.1, "light rain"),
    DailyReading(2, 0.8, "partly cloudy"),
])
```

| | |
| --- | --- |
| **Time** | O(k) for k items |
| **Space** | O(k) |

### 3. Bounded `maxlen` — ring buffer

```python
anomaly_last_5: deque[float] = deque(maxlen=5)
for anomaly in [0.1, -0.3, 0.9, 0.2, 1.1, 0.0]:
    anomaly_last_5.append(anomaly)
```

| | |
| --- | --- |
| **Time** | O(1) per `append` (drops left when full) |
| **Space** | O(maxlen) |

### 4. With `maxlen=0` or invalid — avoid

`maxlen` must be `None` or positive; use `maxlen=None` for unbounded.

### 5. Copy constructor

```python
d2 = deque(d, maxlen=10)
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) |

### 6. Hand-rolled `Deque` ADT (teaching)

See [Reference implementation](#reference-implementation-dequeadt) — wraps `collections.deque`.

```mermaid
flowchart TD
  C([Create deque])
  C --> B{Bounded window?}
  B -->|yes| M["deque(maxlen=k)"]
  B -->|no| U["deque() or deque(iterable)"]
```

---

## `collections.deque` — full API reference

Official docs: [collections.deque](https://docs.python.org/3/library/collections.html#collections.deque).

### Adding elements

| Method | Side | Time | Weather example |
| --- | --- | --- | --- |
| `append(x)` | right | O(1) | New reading enters processing queue |
| `appendleft(x)` | left | O(1) | Urgent backfill inserted at front |
| `extend(iterable)` | right | O(k) | Bulk enqueue k readings |
| `extendleft(iterable)` | left | O(k) | Note: reverses order of iterable |

```python
jobs: deque[str] = deque()
jobs.append("export_STN01_anomaly")
jobs.appendleft("backfill_4021_now")
jobs.extend(["export_STN02", "export_STN03"])
```

```python
d = deque()
d.extendleft([1, 2, 3])
list(d)
```

| `extendleft` | **Time** | **Space** |
| --- | --- | --- |
| k items | O(k) | O(1) aux |

---

### Removing elements

| Method | Side | Time | Raises if empty |
| --- | --- | --- | --- |
| `pop()` | right | O(1) | `IndexError` |
| `popleft()` | left | O(1) | `IndexError` |
| `clear()` | all | O(n) | — |

```python
reading = jobs.popleft()
last = jobs.pop()
```

| | |
| --- | --- |
| **Time** | O(1) per pop |
| **Space** | O(1) |

---

### Inspecting without removal

```python
d = deque([DailyReading(1, 0.0, "clear"), DailyReading(2, 0.1, "overcast")])
assert d[0].reading_id == 1
assert d[-1].reading_id == 2
len(d)
```

| `d[i]` | **Time** | Notes |
| --- | --- | --- |
| index access | O(n) | both ends faster in C implementation but still linear in theory for middle |

Use `d[0]` and `d[-1]` for peek front/rear in O(1) in practice for ends.

---

### Rotation

```python
stations: deque[str] = deque(["STN01", "STN02", "STN03", "STN04"])
stations.rotate(1)
stations.rotate(-1)
```

| `rotate(k)` | **Time** | **Space** |
| --- | --- | --- |
| | O(k) or O(min(k, n-k)) in CPython | O(1) |

**Weather:** Rotate **featured station** in a sidebar without rebuilding the list.

```mermaid
sequenceDiagram
  participant D as deque stations
  D->>D: rotate(1)
  Note over D: right end becomes left — carousel step
```

---

### `maxlen` behavior

When full, `append` drops left; `appendleft` drops right.

```python
window: deque[float] = deque(maxlen=3)
window.append(1.0)
window.append(2.0)
window.append(3.0)
window.append(4.0)
list(window)
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(maxlen) |

**Weather:** Rolling **temp anomaly** or precipitation rate for the last *k* days in a month window.

---

### Thread safety

`deque` is **not** fully thread-safe for all compound operations, but:

- `append` and `popleft` are atomic in CPython due to GIL for single-bytecode ops.
- For producer/consumer across threads, prefer `queue.Queue`.

| Scenario | Recommendation |
| --- | --- |
| Single-threaded ETL | `deque` |
| Multi-thread workers | `queue.Queue` |

---

### Iteration and copying

```python
for reading in d:
    ...
reversed_d = deque(reversed(d))
d_copy = deque(d)
```

| Operation | **Time** | **Space** |
| --- | --- | --- |
| iterate | O(n) | O(1) |
| `deque(reversed(d))` | O(n) | O(n) |

---

### `remove(value)` and `count(value)`

```python
d.remove(DailyReading(2, 0.1, "overcast"))
d.count(DailyReading(2, 0.1, "overcast"))
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

Equality must match; frozen `DailyReading` dataclasses work if same fields.

---

## Reference implementation: `DequeADT`

Wrapper documenting both-end semantics for learners.

```python
from __future__ import annotations

from collections import deque
from typing import Any, Iterable, Iterator


class DequeADT:
    def __init__(self, items: Iterable[Any] | None = None, maxlen: int | None = None) -> None:
        self._d: deque[Any] = deque(items, maxlen=maxlen)

    def __len__(self) -> int:
        return len(self._d)

    def is_empty(self) -> bool:
        return len(self._d) == 0

    def push_back(self, item: Any) -> None:
        self._d.append(item)

    def push_front(self, item: Any) -> None:
        self._d.appendleft(item)

    def pop_back(self) -> Any:
        if not self._d:
            raise IndexError("pop from empty deque")
        return self._d.pop()

    def pop_front(self) -> Any:
        if not self._d:
            raise IndexError("popleft from empty deque")
        return self._d.popleft()

    def peek_back(self) -> Any:
        if not self._d:
            raise IndexError("peek back empty")
        return self._d[-1]

    def peek_front(self) -> Any:
        if not self._d:
            raise IndexError("peek front empty")
        return self._d[0]

    def rotate(self, n: int = 1) -> None:
        self._d.rotate(n)

    def clear(self) -> None:
        self._d.clear()

    def __iter__(self) -> Iterator[Any]:
        yield from self._d

    def to_list(self) -> list[Any]:
        return list(self._d)
```

---

## Map deque methods to stack and queue

| ADT | Push | Pop | Peek |
| --- | --- | --- | --- |
| Stack (top = right) | `append` | `pop` | `d[-1]` |
| Queue (FIFO) | `append` | `popleft` | `d[0]` |
| Stack (top = left) | `appendleft` | `popleft` | `d[0]` |

Pick one convention per module and document it.

```mermaid
flowchart TB
  subgraph fifo["FIFO queue"]
    A1["append → rear"] --> PL["popleft ← front"]
  end
  subgraph lifo["LIFO stack"]
    A2["append → top"] --> P2["pop ← top"]
  end
```

---

## Weather patterns with deque

### Rolling anomaly window (maxlen)

```python
def rolling_mean(anomalies: Iterable[float], k: int) -> list[float]:
    window: deque[float] = deque(maxlen=k)
    means: list[float] = []
    for x in anomalies:
        window.append(x)
        means.append(sum(window) / len(window))
    return means
```

| | |
| --- | --- |
| **Time** | O(n · k) naive sum; O(n) with running sum |
| **Space** | O(k) |

### BFS with deque (grid or graph)

```python
def bfs_zero(grid: list[list[int]], start: tuple[int, int]) -> int:
    rows, cols = len(grid), len(grid[0])
    q: deque[tuple[int, int]] = deque([start])
    grid[start[0]][start[1]] = 1
    dist = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if grid[r][c] == 9:
                return dist
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc))
        dist += 1
    return -1
```

| | |
| --- | --- |
| **Time** | O(rows · cols) |
| **Space** | O(frontier) |

### Palindrome condition sequence (both ends)

```python
def is_palindrome_conditions(conditions: deque[str]) -> bool:
    while len(conditions) > 1:
        if conditions.popleft() != conditions.pop():
            return False
    return True

d = deque(["dry", "wet", "wet", "dry"])
assert is_palindrome_conditions(d)
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) extra |

### Monotonic deque — sliding window maximum anomaly

```python
def sliding_max(anomalies: list[float], k: int) -> list[float]:
    dq: deque[int] = deque()
    out: list[float] = []
    for i, x in enumerate(anomalies):
        while dq and anomalies[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(anomalies[dq[0]])
    return out
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(k) |

---

## Master complexity table

| Operation | Time | Space (aux) |
| --- | --- | --- |
| `append` / `appendleft` | O(1) | O(1) |
| `pop` / `popleft` | O(1) | O(1) |
| `extend` / `extendleft` | O(k) | O(1) |
| `rotate(k)` | O(k)* | O(1) |
| `maxlen` append | O(1) | O(1) |
| `d[i]` middle | O(n) | O(1) |
| `d[0]`, `d[-1]` | O(1) | O(1) |
| `remove` / `count` | O(n) | O(1) |
| iterate | O(n) | O(1) |
| copy `deque(d)` | O(n) | O(n) |

**Storage:** Θ(n) or Θ(maxlen) when bounded.

---

## Python stdlib vs custom doubly linked list

| Need | Use |
| --- | --- |
| Production weather scripts | `collections.deque` |
| Interview “implement deque” | Doubly linked nodes + head/tail |
| Random access by index in hot loop | `list` |
| Sorted archive table | pandas |

---

## When to use deque vs list vs queue.Queue

```mermaid
flowchart TD
  Q([Both ends active?])
  Q -->|yes| DQ["collections.deque"]
  Q -->|no, index i| L["list"]
  Q -->|threads blocking| PQ["queue.Queue"]
```

| Pitfall | Fix |
| --- | --- |
| `insert(0)` on list | `appendleft` on deque |
| `pop(0)` on list | `popleft` |
| `extendleft` order surprise | Remember reversal |
| Huge `rotate(n)` | `n %= len(d)` mentally |
| Storing archive in deque | Use DataFrame; deque for windows |

---

## Worked example: month replay buffer

Model the last **20** readings of a month window with automatic eviction:

```python
from collections import deque

month_replay: deque[DailyReading] = deque(maxlen=20)

def on_new_reading(reading: DailyReading) -> None:
    month_replay.append(reading)

def last_k_anomaly(k: int) -> list[float]:
    return [r.temp_anomaly for r in list(month_replay)[-k:]]
```

| Step | `len` | Oldest retained |
| --- | --- | --- |
| append 21st reading | 20 | 2nd reading dropped |

```mermaid
sequenceDiagram
  participant Feed
  participant D as deque maxlen=20
  Feed->>D: append(reading_21)
  D->>D: drop reading_1 from left
  Note over D: O(1) — no manual index
```

---

## `DequeADT` — full method map

| Method | `deque` equivalent | Time |
| --- | --- | --- |
| `push_back` | `append` | O(1) |
| `push_front` | `appendleft` | O(1) |
| `pop_back` | `pop` | O(1) |
| `pop_front` | `popleft` | O(1) |
| `peek_back` | `[-1]` | O(1) |
| `peek_front` | `[0]` | O(1) |
| `rotate` | `rotate` | O(k) |
| `clear` | `clear` | O(n) drop refs |
| `to_list` | `list(d)` | O(n) |

---

## Chaining two bounded windows

Precipitation-condition window plus anomaly window:

```python
conditions: deque[str] = deque(maxlen=50)
anomalies: deque[float] = deque(maxlen=50)

def ingest(reading: DailyReading) -> None:
    conditions.append("wet" if "rain" in reading.summary.lower() else "dry")
    anomalies.append(reading.temp_anomaly)

def wet_rate() -> float:
    if not conditions:
        return 0.0
    return sum(1 for c in conditions if c == "wet") / len(conditions)
```

| | |
| --- | --- |
| **Time** | O(maxlen) per rate call if recomputed |
| **Space** | O(maxlen) each |

Maintain running counts if you need O(1) rate after each ingest.

---

## `extend` vs loop `append`

```python
d: deque[DailyReading] = deque()
d.extend(readings_from_month)
for r in readings_from_month:
    d.append(r)
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(1) aux |

---

## Internal model (CPython, conceptual)

`collections.deque` uses a **block array of pointers**—not a pure linked list in Python space. That is why both ends are O(1) with good constants and why **middle index** is still slow.

| Structure | Implementation level | Both-end O(1) |
| --- | --- | --- |
| `list` | contiguous dynamic array | No (left) |
| `deque` | block deque in C | Yes |
| hand-rolled doubly linked | Python objects | Yes, slower constants |

---

## Weather export job deque with `maxlen` on pending

Cap pending charts so a slow renderer does not exhaust RAM:

```python
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class ExportJob:
    station_id: str
    year: int
    chart: str

pending: deque[ExportJob] = deque(maxlen=100)
pending.append(ExportJob("STN05", 2024, "precip_anomaly"))
```

| Policy | Behavior |
| --- | --- |
| Drop oldest | `maxlen` deque |
| Block producer | `Queue(maxsize=100)` |
| Unbounded | Risk OOM |

---

## Side-by-side: `list` vs `deque` for weather ingest

| Action | `list` | `deque` |
| --- | --- | --- |
| Add newest reading at end | `append` O(1) | `append` O(1) |
| Process oldest first | `pop(0)` **O(n)** | `popleft` O(1) |
| Insert urgent at front | `insert(0, x)` **O(n)** | `appendleft` O(1) |
| Index `readings[i]` in loop | O(1) | O(n) at ends only fast |
| Slice `readings[10:20]` | Yes | No slice on deque |

```python
def drain_list_bad(q: list[DailyReading]) -> None:
    while q:
        process(q.pop(0))

def drain_deque_good(q: deque[DailyReading]) -> None:
    while q:
        process(q.popleft())
```

---

## `rotate` and station carousel (detailed)

```python
station_rotation: deque[str] = deque(
    ["STN01", "STN02", "STN03", "STN04"]
)
station_rotation.rotate(1)
station_rotation.rotate(-1)
```

| `rotate(n)` | Effect |
| --- | --- |
| `n > 0` | Right rotation: tail moves toward head |
| `n < 0` | Left rotation |
| `n == 0` | No-op |

For **n** stations, `rotate(k)` is O(k); use `k %= len(d)` mentally when k can be huge.

```mermaid
flowchart LR
  A["STN01"] --> B["STN02"] --> C["STN03"] --> D["STN04"]
  D --> A
  rotate1["rotate(1)"] --> A2["STN04"] --> B2["STN01"] --> C2["STN02"] --> D2["STN03"]
  D2 --> A2
```

---

## Combining stack and queue on one deque

Document your convention in module docstring:

```python
history: deque[LabelEdit] = deque()
history.append(edit)
history.pop()

fifo: deque[DailyReading] = deque()
fifo.append(reading)
fifo.popleft()
```

Mixing both patterns on the **same** deque without discipline causes subtle bugs.

---

## `__getitem__` and slicing limitations

```python
d = deque([DailyReading(i, 0.0, "overcast") for i in range(5)])
assert d[0].reading_id == 0
assert d[-1].reading_id == 4
middle = list(d)[1:3]
```

| Access | Time |
| --- | --- |
| `d[0]`, `d[-1]` | O(1) at ends in practice |
| `d[i]` middle | O(n) |
| slice | Not supported — materialize `list(d)` |

For weather replay UIs that need **random access** to reading index *i* in a month window, keep a **`list`** alongside a `deque` window, or use only `list` for the month.

---

## Official documentation

Python’s deque is documented in the standard library: [collections.deque](https://docs.python.org/3/library/collections.html#collections.deque). Prefer that page for edge cases (thread safety notes, version changes) alongside this guide’s weather-oriented patterns.

| Doc topic | Why read it |
| --- | --- |
| `maxlen` | Exact drop behavior on both ends |
| `rotate` | Sign of *n* and empty deque |
| Thread safety | Which ops are atomic under GIL |

---

## Related structures in this guide

| Structure | Link |
| --- | --- |
| [Queue](../queue/index.md) | FIFO via `append` + `popleft` |
| [Stacks](../stacks/index.md) | LIFO via `append` + `pop` |
| [Doubly linked list](../doubly-linked-list/index.md) | Conceptual basis for deque |
| [Circularly linked list](../circularly-linked-list/index.md) | Ring buffers |

---

## Quick reference card

```python
from collections import deque

q: deque[DailyReading] = deque()
q.append(reading)
p = q.popleft()

w: deque[float] = deque(maxlen=10)
w.append(reading.temp_anomaly)

d = deque(["STN01", "STN02"])
d.appendleft("STN03")
d.rotate(1)

st: deque[DailyReading] = deque()
st.append(reading)
st.pop()
```

Use **`collections.deque`** whenever you need **O(1) at both ends**—queues, stacks, rolling weather windows, rotations, and BFS. Avoid **`list.pop(0)`** and **`list.insert(0, ...)`** in performance-sensitive ingest paths.

**Weather pipeline checklist**

1. **Rolling metrics** — `deque(maxlen=k)`.
2. **Reading queue** — `append` + `popleft`.
3. **Urgent front insert** — `appendleft` once, not `list.insert(0)`.
4. **Carousel** — `rotate` on small station deques.
