# Circularly linked list

A linked list where the **last node’s `next` points back to the first**—there is no `None` at the “end” in the forward direction. The structure is a **ring**: one pointer walk eventually returns to where you started.

| | |
| --- | --- |
| **What it is** | A chain that closes on itself: singly circular (`last.next → head`) or doubly circular (`head.prev → tail` and `tail.next → head`). |
| **Core operations** | Rotate the “current” pointer, iterate with a stop at `head`, insert/delete with careful predecessor logic. |
| **When to use** | Round-robin scheduling, ring buffers, “infinite” carousel iteration, or any cycle where you advance a cursor without reallocating. |
| **Trade-off** | Easy to loop forever if you forget a stop condition; no O(1) random access by index; extra pointer discipline vs a Python `list` modulo index. |

In **NFL data analysis**, a circular list is a natural model for **repeating cycles with no true end**: rotating through **bye-week slots** in a fantasy schedule, stepping **32 teams** in a fixed order for a dashboard carousel, or a **fixed-size ring buffer** of the last *k* plays in a live feed where the oldest slot is overwritten when the ring wraps. You still store season play-by-play in **pandas** or a **`list`**—the ring is for **bounded, repeating** order on small *n*.

This page is your **ready reference**: singly and doubly circular variants, every way to create them in Python, a complete implementation, operation-by-operation examples with **time and space complexity**, and when to prefer stdlib tools. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How a circular list differs from linear linked lists

| | **Singly circular** | [Singly linked](../linked-list/index.md) | [Doubly circular](../doubly-linked-list/index.md) + ring |
| --- | --- | --- | --- |
| **End of chain** | `tail.next == head` | `tail.next == None` | `tail.next == head`, `head.prev == tail` |
| **Empty list** | `head is None` | `head is None` | `head is None` |
| **Traverse all *n*** | Stop when back at start | Stop at `None` | Stop when back at start; can walk backward |
| **Rotate “current”** | O(1) advance `cur = cur.next` | N/A (linear end) | O(1) forward or backward |
| **Delete tail (singly)** | O(n) — need predecessor | O(n) | O(1) with `prev` |
| **NFL fit** | Round-robin team cursor, ring of week slots | Drive chain with clear end | Bidirectional film scrubber on a loop |

```mermaid
flowchart LR
  subgraph linear["Singly linked (linear)"]
    H1["head"] --> A1["A"] --> B1["B"] --> NIL["None"]
  end
  subgraph circ["Singly circular"]
    H2["head"] --> A2["A"] --> B2["B"] --> C2["C"]
    C2 --> H2
  end
```

Throughout this page, **n** is the number of nodes in the ring (e.g. teams in a rotation, or buffer capacity). **i** is a zero-based index from an arbitrary start (usually `head`).

---

## NFL data analysis: what a circular list models

| NFL idea | Circular view | Typical *n* |
| --- | --- | --- |
| **Bye-week round-robin** | Each node = team; advance `current` each week | 32 |
| **Division rotation** | Fixed order of opponents; wrap after last team | 4–8 |
| **Live EPA ring buffer** | Fixed *k* slots; overwrite oldest on wrap | *k* = 10–100 |
| **Replay carousel** | Cycle highlight clips; no “end” in UI | clips in session |
| **Scheduler tick** | Advance pointer through time windows | windows per quarter |

**Reach for `list` + modulo** (`teams[i % 32]`) when you only need index math on a static table. **Reach for a circular linked list** when the ADT is **cursor + splice** (insert after current, rotate, delete current) or you are learning pointer cycles. **Reach for `collections.deque(maxlen=k)`** when you need a production ring buffer without hand-rolled nodes.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Team:
    """Minimal team record for examples on this page."""
    abbr: str
    name: str
    conference: str


@dataclass(frozen=True)
class WeekSlot:
    """One slot in a rotating bye / opponent schedule."""
    week: int
    team: Team
    is_bye: bool = False
```

---

## Mental model: head, tail, and the closing link

**Singly circular (non-empty):**

- `head` — entry point (convention; any node can serve as “head”).
- `tail` — last node in insertion order; **`tail.next is head`**.
- **Empty:** `head is None` (and usually `tail is None`).

**Doubly circular (non-empty):**

- `head.prev is tail` and `tail.next is head`.
- **Empty:** `head is None`.

```mermaid
sequenceDiagram
  participant Analyst
  participant Ring as circular teams
  Analyst->>Ring: current = head
  Ring-->>Analyst: current.data = "KC"
  Analyst->>Ring: rotate_forward()
  Ring-->>Analyst: current.data = "BUF"
  Note over Analyst,Ring: After n steps you return to start — stop with a counter or visited flag
```

| Kind | What you pay for | Circular examples | NFL-flavored example |
| --- | --- | --- | --- |
| **Rotate cursor** | O(1) one `next` hop | `rotate_forward()` | Next team in bye-week display |
| **Traverse all** | O(n) with stop at head | `__iter__` | List all 32 teams once |
| **Insert after cursor** | O(1) if you hold cursor | splice | Insert traded player node after “current” team |
| **Find by value** | O(n) worst case | `index_of` | Locate `Team("SF", ...)` in ring |

---

## Node definitions

### Singly circular node

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Iterator


@dataclass
class CNode:
    """Singly linked node (used in circular list)."""
    data: Any
    next: CNode | None = None
```

| | |
| --- | --- |
| **Time** | O(1) to construct |
| **Space** | O(1) per node |

### Doubly circular node

```python
@dataclass
class DCNode:
    """Doubly linked node for circular doubly linked list."""
    data: Any
    prev: DCNode | None = None
    next: DCNode | None = None
```

| | |
| --- | --- |
| **Time** | O(1) to construct |
| **Space** | O(1) per node (two links) |

```mermaid
flowchart TB
  subgraph snode["CNode (singly)"]
    D1["data"]
    N1["next → … or head"]
  end
  subgraph dnode["DCNode (doubly)"]
    P["prev"]
    D2["data"]
    N2["next"]
  end
```

---

## Ways to create a circularly linked list

### 1. Empty list

```python
head: CNode | None = None
tail: CNode | None = None
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Empty `SinglyCircularLinkedList` wrapper

```python
class SinglyCircularLinkedList:
    def __init__(self) -> None:
        self.head: CNode | None = None
        self.tail: CNode | None = None
        self._size = 0

ring = SinglyCircularLinkedList()
assert ring.is_empty()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 3. Single-node ring (degenerate circle)

```python
node = CNode(Team("KC", "Chiefs", "AFC"))
node.next = node  # points to itself
head = tail = node
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 4. Build from iterable — append at tail, close ring

Preserves input order; after the loop, `tail.next = head`.

```python
def ring_from_iterable(items: Iterable[Any]) -> SinglyCircularLinkedList:
    ring = SinglyCircularLinkedList()
    for item in items:
        ring.append(item)
    return ring

afc_north = [
    Team("BAL", "Ravens", "AFC"),
    Team("CIN", "Bengals", "AFC"),
    Team("CLE", "Browns", "AFC"),
    Team("PIT", "Steelers", "AFC"),
]
rotation = ring_from_iterable(afc_north)
```

| | |
| --- | --- |
| **Time** | O(k) for *k* items |
| **Space** | O(k) nodes |

### 5. Build by linking last to first manually

```python
nodes = [CNode(t) for t in afc_north]
for i in range(len(nodes) - 1):
    nodes[i].next = nodes[i + 1]
nodes[-1].next = nodes[0]
head, tail = nodes[0], nodes[-1]
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(k) |

### 6. `collections.deque` as a practical ring buffer

Not a linked list, but the NFL tool for fixed windows:

```python
from collections import deque

epa_window: deque[float] = deque(maxlen=10)
epa_window.append(0.42)
epa_window.append(-1.1)
# When len == maxlen, oldest is dropped automatically
```

| | |
| --- | --- |
| **Time** | O(1) append |
| **Space** | O(maxlen) |

### 7. Python `list` + modulo index (static rotation table)

```python
teams = ["KC", "BUF", "SF", "PHI"]
i = 0
current = teams[i % len(teams)]
i += 1  # next week
```

| | |
| --- | --- |
| **Time** | O(1) index |
| **Space** | O(n) array |

```mermaid
flowchart TD
  Q([Need a ring structure?])
  Q --> F{Fixed capacity overwrite?}
  F -->|yes| DQ["collections.deque(maxlen=k)"]
  F -->|no| R{Pointer / splice teaching?}
  R -->|yes| CL["SinglyCircularLinkedList"]
  R -->|no| L["list + modulo index"]
```

---

## Reference implementation: `SinglyCircularLinkedList`

Complete class with head, tail, cached size, and safe iteration.

```python
class SinglyCircularLinkedList:
    """Singly circular linked list. Empty: head is None."""

    def __init__(self, items: Iterable[Any] | None = None) -> None:
        self.head: CNode | None = None
        self.tail: CNode | None = None
        self._size = 0
        if items is not None:
            self.extend(items)

    def _close_ring(self) -> None:
        if self.tail is not None and self.head is not None:
            self.tail.next = self.head

    def is_empty(self) -> bool:
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def append(self, data: Any) -> None:
        node = CNode(data)
        if self.head is None:
            self.head = self.tail = node
            node.next = node
        else:
            assert self.tail is not None
            node.next = self.head
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, data: Any) -> None:
        node = CNode(data)
        if self.head is None:
            self.head = self.tail = node
            node.next = node
        else:
            assert self.tail is not None
            node.next = self.head
            self.tail.next = node
            self.head = node
        self._size += 1

    def insert_after(self, pivot_data: Any, data: Any) -> None:
        pivot = self._find_node(pivot_data)
        if pivot is None:
            raise ValueError(f"{pivot_data!r} not in ring")
        node = CNode(data, next=pivot.next)
        pivot.next = node
        if pivot is self.tail:
            self.tail = node
        self._size += 1

    def insert_at(self, index: int, data: Any) -> None:
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        if index == 0:
            self.prepend(data)
            return
        prev = self._node_at(index - 1)
        node = CNode(data, next=prev.next)
        prev.next = node
        if prev is self.tail:
            self.tail = node
        self._size += 1

    def remove_first(self, data: Any) -> bool:
        if self.head is None:
            return False
        if self._size == 1 and self.head.data == data:
            self.clear()
            return True
        if self.head.data == data:
            assert self.tail is not None
            self.head = self.head.next
            self.tail.next = self.head
            self._size -= 1
            return True
        cur = self.head
        for _ in range(self._size - 1):
            assert cur.next is not None
            nxt = cur.next
            if nxt.data == data:
                cur.next = nxt.next
                if nxt is self.tail:
                    self.tail = cur
                self._size -= 1
                return True
            cur = nxt
        return False

    def remove_at(self, index: int) -> Any:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        if self._size == 1:
            data = self.head.data
            self.clear()
            return data
        if index == 0:
            return self.pop_head()
        prev = self._node_at(index - 1)
        assert prev.next is not None
        victim = prev.next
        data = victim.data
        prev.next = victim.next
        if victim is self.tail:
            self.tail = prev
        self._size -= 1
        return data

    def pop_head(self) -> Any:
        if self.head is None:
            raise IndexError("pop from empty ring")
        data = self.head.data
        if self._size == 1:
            self.clear()
            return data
        assert self.tail is not None
        self.head = self.head.next
        self.tail.next = self.head
        self._size -= 1
        return data

    def get(self, index: int) -> Any:
        return self._node_at(index).data

    def set(self, index: int, data: Any) -> None:
        self._node_at(index).data = data

    def index_of(self, data: Any) -> int:
        for i, item in enumerate(self):
            if item == data:
                return i
        raise ValueError(f"{data!r} not in ring")

    def contains(self, data: Any) -> bool:
        return self._find_node(data) is not None

    def clear(self) -> None:
        self.head = self.tail = None
        self._size = 0

    def rotate_forward(self, steps: int = 1) -> None:
        """Move head forward (counter-clockwise in pointer diagram). O(steps)."""
        if self.head is None or steps == 0:
            return
        steps %= self._size
        for _ in range(steps):
            assert self.head is not None
            self.head = self.head.next
            self.tail = self.tail.next if self.tail else None

    def rotate_backward(self, steps: int = 1) -> None:
        """Singly circular: walk forward n - steps (no prev). O(steps)."""
        if self.head is None:
            return
        self.rotate_forward(self._size - (steps % self._size))

    def to_list(self) -> list[Any]:
        return list(self)

    def extend(self, items: Iterable[Any]) -> None:
        for item in items:
            self.append(item)

    def __iter__(self) -> Iterator[Any]:
        if self.head is None:
            return
        cur = self.head
        for _ in range(self._size):
            yield cur.data
            assert cur.next is not None
            cur = cur.next

    def _node_at(self, index: int) -> CNode:
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        cur = self.head
        for _ in range(index):
            assert cur is not None and cur.next is not None
            cur = cur.next
        assert cur is not None
        return cur

    def _find_node(self, data: Any) -> CNode | None:
        cur = self.head
        for _ in range(self._size):
            if cur is None:
                break
            if cur.data == data:
                return cur
            assert cur.next is not None
            cur = cur.next
        return None
```

**Note:** `_find_node` in the listing walks from `head`; for clarity in teaching docs the walk matches `__iter__`. Optimize hot paths by fusing search with one pass.

---

## All operations (with examples and complexity)

```mermaid
flowchart TB
  subgraph fast["O(1) typical"]
    append
    prepend
    pop_head
    rotate1["rotate_forward(1)"]
    len_op["len / is_empty"]
  end
  subgraph linear["O(n)"]
    get
    insert_at
    remove_at
    index_of
    find
  end
```

### `is_empty()` / `len(ring)`

```python
ring = SinglyCircularLinkedList()
assert ring.is_empty()
ring.append(Team("KC", "Chiefs", "AFC"))
assert len(ring) == 1
```

| | |
| --- | --- |
| **Time** | O(1) with cached `_size` |
| **Space** | O(1) |

---

### `append(data)` — add after current tail, close ring

```python
ring = SinglyCircularLinkedList()
ring.append(Team("BAL", "Ravens", "AFC"))
ring.append(Team("CIN", "Bengals", "AFC"))
assert len(ring) == 2
assert ring.tail.next is ring.head
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) one node |

```mermaid
sequenceDiagram
  participant R as ring
  participant New as new node
  participant H as head
  participant T as tail
  R->>New: create node
  New->>H: next = head
  T->>New: tail.next = new
  R->>R: tail = new
```

---

### `prepend(data)` — insert before head

```python
ring = SinglyCircularLinkedList([Team("CIN", "Bengals", "AFC")])
ring.prepend(Team("BAL", "Ravens", "AFC"))
assert ring.get(0).abbr == "BAL"
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

---

### `insert_after(pivot_data, data)` — splice after a known value

**NFL use:** Insert a **replacement bye slot** after a specific team node in a custom scheduler sketch.

```python
ring = SinglyCircularLinkedList([
    Team("KC", "Chiefs", "AFC"),
    Team("LAC", "Chargers", "AFC"),
])
ring.insert_after(Team("KC", "Chiefs", "AFC"), WeekSlot(5, Team("BYE", "Bye", ""), is_bye=True))
```

| | |
| --- | --- |
| **Time** | O(n) find pivot + O(1) splice |
| **Space** | O(1) |

---

### `insert_at(index, data)`

Index `0` → `prepend`; otherwise walk to predecessor.

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

---

### `get(index)` / `set(index, data)`

| | |
| --- | --- |
| **Time** | O(n) worst case |
| **Space** | O(1) |

---

### `pop_head()` / `remove_at(index)` / `remove_first(value)`

Always repair `tail.next = head` after head changes.

```python
ring = SinglyCircularLinkedList(["A", "B", "C"])
assert ring.pop_head() == "A"
assert len(ring) == 2
```

| Operation | **Time** | **Space** |
| --- | --- | --- |
| `pop_head` | O(1) | O(1) |
| `remove_at` | O(n) | O(1) |
| `remove_first` | O(n) | O(1) |

---

### `rotate_forward(steps)` / `rotate_backward(steps)`

**NFL use:** Advance **current week’s featured team** without rebuilding the list.

```python
ring = SinglyCircularLinkedList(["KC", "BUF", "SF"])
ring.rotate_forward(1)
assert ring.get(0) == "BUF"
ring.rotate_forward(3)
assert ring.get(0) == "KC"
```

| | |
| --- | --- |
| **Time** | O(steps) singly; O(1) for one step |
| **Space** | O(1) |

```mermaid
flowchart LR
  H1["head: KC"] --> B1["BUF"] --> S1["SF"]
  S1 --> H1
  H2["after rotate 1"] --> S2["SF"]
  S2 --> H2b["KC"]
  H2b --> B2["BUF"]
  B2 --> H2
```

---

### `contains` / `index_of`

| | |
| --- | --- |
| **Time** | O(n) — at most one lap |
| **Space** | O(1) |

---

### `clear()` / `extend` / `to_list` / iteration

```python
for team in ring:
    print(team.abbr)  # exactly len(ring) lines, not infinite
```

| | |
| --- | --- |
| **Time** | O(n) full traverse |
| **Space** | O(n) for `to_list` output |

**Critical:** Never `while cur: cur = cur.next` without counting—on a ring you loop forever.

---

## Doubly circular linked list (sketch)

When you need **O(1) step backward**, use `prev`:

```python
class DoublyCircularLinkedList:
    def __init__(self) -> None:
        self.head: DCNode | None = None
        self._size = 0

    def append(self, data: Any) -> None:
        node = DCNode(data)
        if self.head is None:
            node.next = node.prev = node
            self.head = node
        else:
            tail = self.head.prev
            assert tail is not None
            node.next = self.head
            node.prev = tail
            tail.next = node
            self.head.prev = node
        self._size += 1

    def rotate_backward(self, steps: int = 1) -> None:
        if self.head is None:
            return
        steps %= self._size
        for _ in range(steps):
            self.head = self.head.prev
```

| Operation (doubly circular) | **Time** | **Space** |
| --- | --- | --- |
| `append` / `prepend` | O(1) | O(1) |
| `rotate_backward(1)` | O(1) | O(1) |
| `remove node with ref` | O(1) | O(1) |
| `index_of` | O(n) | O(1) |

See [Doubly linked list](../doubly-linked-list/index.md) for full doubly linked operations; add `tail.next = head` and `head.prev = tail` when closing the ring.

---

## Master complexity table

Let **n** = `len(ring)`.

| Operation | Time | Space (auxiliary) | Notes |
| --- | --- | --- | --- |
| Create empty | O(1) | O(1) | |
| Build from *k* items | O(k) | O(k) | tail append + close |
| `append` / `prepend` | O(1) | O(1) | maintain `tail.next → head` |
| `insert_after` (known pivot node) | O(1) | O(1) | O(n) if search by value |
| `insert_at(i)` | O(n) | O(1) | |
| `get` / `set` at *i* | O(n) | O(1) | |
| `pop_head` | O(1) | O(1) | |
| `remove_at` / `remove_first` | O(n) | O(1) | |
| `rotate_forward(1)` | O(1) | O(1) | move head pointer |
| `rotate_forward(k)` | O(k) | O(1) | |
| `contains` / `index_of` | O(n) | O(1) | one lap max |
| Traverse / `to_list` | O(n) | O(n) output | must use counter |
| Doubly `rotate_backward(1)` | O(1) | O(1) | needs `prev` |

**Storage:** Θ(n) nodes; singly circular pays one `next` per node; doubly pays `next` + `prev`.

---

## Classic patterns

### Floyd cycle detection (linear list vs ring)

On a **circular** structure, every traverse must stop after **n** steps. Floyd’s algorithm applies when a **broken** linear list accidentally points backward and forms a hidden cycle.

```python
def has_cycle_floyd(head: CNode | None) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

### Round-robin fair scheduler

```python
def next_team(ring: SinglyCircularLinkedList) -> Team:
    team = ring.pop_head()
    ring.append(team)
    return team
```

Rotating by moving head to tail after serving is O(1) per tick.

| | |
| --- | --- |
| **Time** | O(1) per tick |
| **Space** | O(1) |

### Ring buffer vs circular linked list

| Need | Structure |
| --- | --- |
| Overwrite oldest at fixed capacity | `deque(maxlen=k)` or array + write index |
| Variable-size ring with splices | Circular linked list |
| Index `i % n` on static table | `list` |

---

## Python stdlib: what to use instead

| Need | Prefer | Why |
| --- | --- | --- |
| Fixed play EPA window | `collections.deque(maxlen=k)` | C-speed, no pointer bugs |
| Rotate static team order | `list` + `% len` | Simple, cache-friendly |
| Round-robin without splices | `itertools.cycle` on a tuple | O(1) per yield, read-only |
| Season play-by-play | pandas / `list` | Not a ring |
| Learning pointer cycles | `SinglyCircularLinkedList` | Interview / ADT clarity |

```python
from itertools import cycle

teams = ("KC", "BUF", "SF", "PHI")
rot = cycle(teams)
next(rot)  # KC
next(rot)  # BUF
```

---

## Circular vs linear — decision flow

```mermaid
flowchart TD
  Q([Ordering problem?])
  Q --> E{Explicit end?}
  E -->|yes| LIN["Singly / doubly linked"]
  E -->|no, wrap| CIRC{Circular linked or deque?}
  CIRC --> O{Overwrite at capacity?}
  O -->|yes| DQ["deque(maxlen)"]
  O -->|no| CL["Circular linked list"]
```

---

## Common pitfalls

| Pitfall | Why it hurts | Better approach |
| --- | --- | --- |
| Infinite `while cur = cur.next` | Never terminates on ring | Loop `for _ in range(len(ring))` or use `__iter__` |
| Forgetting `tail.next = head` after edit | Ring breaks | Centralize `_close_ring()` |
| Single-node ring not self-linked | `tail.next` is None | On first insert: `node.next = node` |
| Using circular list for season table | O(n) per lookup | `dict` / DataFrame |
| `rotate_backward` on singly list | Needs O(n) workaround | Doubly circular or forward `n-1` steps |
| Confusing `itertools.cycle` with mutable ring | `cycle` does not splice | Custom class for insert/delete |
| Deep copy of nodes | Shared `data` objects | `copy.deepcopy` if needed |

---

## Related structures in this guide

| Structure | Relationship |
| --- | --- |
| [Linked list](../linked-list/index.md) | Linear chain; open end |
| [Doubly linked list](../doubly-linked-list/index.md) | `prev` + optional ring close |
| [Queue](../queue/index.md) | FIFO; not cyclic |
| [Dequeue (deque)](../dequeue-deque/index.md) | Practical ring buffer |
| [Array-based lists](../array-based-lists/index.md) | `i % n` rotation on arrays |

---

## Quick reference card

```python
ring = SinglyCircularLinkedList([Team("KC", "Chiefs", "AFC"), Team("BUF", "Bills", "AFC")])

# O(1) — grow ring, maintain close link
ring.append(Team("SF", "49ers", "NFC"))
ring.prepend(Team("PHI", "Eagles", "NFC"))

# O(1) — round-robin cursor
ring.rotate_forward(1)

# O(n) — search / index (one lap only)
ring.index_of(Team("BUF", "Bills", "AFC"))
ring.get(2)

# O(n) — export once
teams = ring.to_list()

# Iterate safely
for t in ring:
    ...
```

Use a **circularly linked list** when the problem is literally a **cycle**: round-robin, rotating cursor, or variable-size ring with pointer splices. Use **`deque(maxlen=k)`**, **`itertools.cycle`**, or **`list` + modulo** for most NFL pipelines where the ring is just “wrap the index.”

**NFL pipeline checklist**

1. **Default** — Tabular data in pandas; rotation via index math or `cycle`.
2. **Bounded live window** — `deque(maxlen=k)` for last *k* EPA values.
3. **Custom scheduler with splices** — Circular linked list (small *n*).
4. **Traverse** — Always bound steps to `len(ring)`; never unbounded `next` walk.
