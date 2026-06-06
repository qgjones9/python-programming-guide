# Linked list

A linear collection stored as **nodes** that point to the next item—unlike a contiguous array, there is no index-based address arithmetic. You reach the *i*-th element only by following links from the **head**. In **daily weather data analysis**, that shape shows up when you model a **sequence in order** (days in a window, readings in a station chain, events in a live ingest feed) and care about **prepend/append at the ends** or **pointer-style merges** more than random access by index.

| | |
| --- | --- |
| **What it is** | Nodes in a chain: each holds a value (e.g. one daily reading dict or `reading_id`) and a link to the *next* node. The *head* is the entry to the list. |
| **Core operations** | Insert or delete at the head in O(1); traverse from the head for everything else. |
| **When to use** | Frequent insert/delete at the front (newest reading arrives “at the top” of a working buffer), unknown or changing length, or algorithms defined as **rewiring** (reverse a daily chain, merge two sorted station streams). |
| **Trade-off** | Random access by index is O(n)—painful if you keep calling `get(i)` on thousands of daily rows; extra memory per node for `next`. Multi-year archives and indexed lookups usually belong on a Python `list` or `dict`. |

Python has **no built-in singly linked list type**. You either implement nodes yourself (the best way to learn the ADT) or reach for tools that solve similar problems—`collections.deque` for a live reading queue, or a `list` when you need `readings[i]` and vectorized pandas work. This page is your **ready reference** for singly linked lists in Python: structure, a complete implementation, every operation with examples, and **time and space complexity** on each. For Big-O notation and weather-scale *n*, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How a singly linked list differs from Python’s `list`

| | **Singly linked list** | **Python `list`** ([array-based list](../array-based-lists/index.md)) |
| --- | --- | --- |
| **Storage** | Scattered nodes linked by references | Contiguous array of references |
| **Access `i`-th item** | O(n) walk from head | O(1) index |
| **Insert at head** | O(1) | O(n) shift |
| **Insert at tail** | O(1) with tail pointer; O(n) without | Amortized O(1) `append` |
| **Insert in middle** | O(n) to find position; O(1) pointer rewiring once there | O(n) shift |
| **Cache behavior** | Poor (nodes may be far apart in memory) | Good (sequential slots) |
| **Weather-style workload** | One station window chain | Full daily observation table, `readings[i]`, `groupby`, export to parquet |

In CPython, `list` is always a dynamic array. A “linked list” in Python is **your own classes**, not a language primitive. Your multi-year CSV belongs in a **`list` of dicts or a DataFrame**; a linked list is for **ordered chains** where pointer costs are the lesson or the algorithm (merge two sorted reading-id chains without array shifts).

```mermaid
flowchart LR
  subgraph array["Python list (dynamic array)"]
    direction LR
    A0["[0]"] --- A1["[1]"] --- A2["[2]"] --- A3["[3]"] 
  end
  subgraph linked["Singly linked list"]
    direction LR
    H["head"] --> N0["data + next"]
    N0 --> N1["data + next"]
    N1 --> N2["data + next"]
    N2 --> NIL["None"]
  end
```

Throughout this page, **n** means the number of nodes in the list (e.g. days in one analysis window). **i** means a zero-based index. In production weather pipelines, **n** per list is often small (one month window) while total daily rows in an archive live in tables—do not confuse “linked list of one window” with “50k-row observation DataFrame.”

---

## Singly linked vs doubly linked vs Python `list`

| | **Singly linked** | [Doubly linked](../doubly-linked-list/index.md) | [Python `list`](../array-based-lists/index.md) |
| --- | --- | --- | --- |
| **Pointers per node** | `next` only | `next` + `prev` | None (array of refs) |
| **`pop_tail`** | O(n) — must find predecessor | O(1) with `tail` | O(1) amortized |
| **Delete when you hold a node reference** | O(n) to find predecessor; **copy-value hack** is an O(1) workaround with caveats | O(1) rewire `prev` and `next` | O(n) shift after removal |
| **Access by index `i`** | O(n) from head only | O(n) from nearer end | O(1) |
| **Memory** | Medium | Highest per element | Compact + cache-friendly |
| **Weather fit** | Head-heavy live ingest, merge drills | Bidirectional timeline UI, both-end window | Full daily observation table |

The **copy-value hack** (detailed below) is the main singly linked workaround when you hold a node reference but not its predecessor. A [doubly linked list](../doubly-linked-list/index.md) avoids the hack entirely with a `prev` pointer.

---

## Daily weather analysis: what a linked list models

You will rarely store a full season in a hand-rolled `LinkedList`. The structure still matters because the **same costs** appear in custom code, interviews, and pointer-based algorithms you might use on **chunks** of data.

| Weather analysis idea | Linked-list view | Typical *n* |
| --- | --- | --- |
| **Days in one window** | Head = oldest day; `next` = next day in chronological order | ~7–31 |
| **Live ingest buffer** | `prepend` newest tick; trim from tail when window exceeds *k* | window size *k* |
| **Merge two sorted streams** | Each stream is a chain sorted by `(station_id, reading_id)`; merge without shifting a whole array | *n* + *m* |
| **Walk the chain** | Sum temp anomaly, find first cold front, detect cycle in bad test data | O(n) traverse |

**Reach for a Python `list` or pandas** when you filter 50,000 daily rows by station, sort months by precipitation, or need `readings[i]` in a loop. **Reach for a linked list (or `deque`)** when the problem is inherently **sequential** and **end-heavy**: stack of undo edits on a forecast editor, merge sorted linked chains in a streaming join sketch, or learning how `insert(0)` on a `list` differs from O(1) `prepend`.

```python
from dataclasses import dataclass


@dataclass
class DailyReading:
    reading_id: int
    month: int
    temp_anomaly: float
    summary: str
```

Each node’s `data` can be a `DailyReading`, a `reading_id`, or a row dict. `LinkedList` is defined in [Reference implementation](#reference-implementation) below; later sections use `DailyReading` in operation examples.

---

## Mental model: pointers, head, and tail

Each **node** stores:

1. **`data`** — the value (any Python object).
2. **`next`** — reference to the next node, or `None` at the end.

The **head** is the only handle the outside world needs to reach the whole chain (unless you also keep a **tail** reference for fast appends).

```mermaid
sequenceDiagram
  participant Client
  participant Head as head pointer
  participant N1 as node A
  participant N2 as node B
  participant N3 as node C
  Client->>Head: holds reference to first node
  Head->>N1: data = A
  N1->>N2: next
  N2->>N3: next
  N3->>N3: next = None
  Client->>Head: traverse: cur = head; cur = cur.next
```

**Three kinds of cost** (mirror the array-based list page):

| Kind | What you pay for | Linked list examples | Weather-flavored example |
| --- | --- | --- | --- |
| **Head change** | Rewire one or two pointers | `prepend`, `pop_head` | New live reading pushed to front of a scratch buffer |
| **Find position** | Walk up to *n* nodes | `get(i)`, `insert(i)`, `remove(value)` | “Third day in this window”—must walk from head |
| **Rewire after find** | Constant pointer updates | splice after predecessor | Insert corrected sensor row after day 2 without shifting a whole array |

---

## Node definition (foundation for everything)

Use a small class. The list **logic** lives in a wrapper class that holds `head` (and optionally `tail`, `size`).

```python
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
```

| | |
| --- | --- |
| **Time** | O(1) to construct one node |
| **Space** | O(1) per node (value + `next` reference; object overhead applies in CPython) |

```mermaid
flowchart TB
  subgraph node["Node"]
    D["data: Any"]
    N["next: Node | None"]
  end
  D --- N
```

---

## Ways to create a linked list

### 1. Empty list — `head is None`

The canonical empty structure.

```python
head = None
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Empty `LinkedList` wrapper

```python
class LinkedList:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0

ll = LinkedList()
assert ll.head is None
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 3. Single-node list

```python
head = Node(42)

head = Node("only", next=None)
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) for one node |

### 4. Build from an iterable — append at tail (forward order)

Preserves input order; needs O(n) steps (and a tail pointer for O(1) per append).

```python
def from_iterable(items):
    head = None
    tail = None
    for item in items:
        node = Node(item)
        if head is None:
            head = tail = node
        else:
            tail.next = node
            tail = node
    return head

reading_ids = [401, 402, 403]
chain = from_iterable(reading_ids)
```

| | |
| --- | --- |
| **Time** | O(k) for *k* items (e.g. *k* days in a window) |
| **Space** | O(k) nodes |

### 5. Build from an iterable — prepend at head (reversed order)

Each insert at head is O(1); result is **backwards** unless you reverse later.

```python
def from_iterable_reversed(items):
    head = None
    for item in items:
        head = Node(item, next=head)
    return head

chain = from_iterable_reversed([10, 20, 30])
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(k) |

### 6. Constructor on a class

```python
class LinkedList:
    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.size = 0
        if values is not None:
            for value in values:
                self.append(value)

ll = LinkedList([1, 2, 3])
```

| | |
| --- | --- |
| **Time** | O(k) for *k* items with tail-tracked `append` |
| **Space** | O(k) |

### 7. Manual chain wiring (tests and diagrams)

```python
n3 = Node(3)
n2 = Node(2, next=n3)
n1 = Node(1, next=n2)
head = n1
```

| | |
| --- | --- |
| **Time** | O(k) |
| **Space** | O(k) |

### Creation cheat sheet

```mermaid
flowchart TD
  Start([Need a linked list?])
  Start --> Empty{Empty?}
  Empty -->|yes| E1["head = None or LinkedList()"]
  Empty -->|no| Order{Preserve input order?}
  Order -->|yes| Tail["append each item — keep tail pointer"]
  Order -->|no / reverse OK| Head["prepend each item — O(1) per item"]
  Order -->|fixed tiny chain| Manual["wire Node(..., next=...)"]
  E1 --> Done([ready])
  Tail --> Done
  Head --> Done
  Manual --> Done
```

---

## Reference implementation

The sections below use this **complete** singly linked list (`LinkedList` class). Every method is documented with complexity in the following sections.

```python
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:

    def __init__(self, values=None):
        self.head = None
        self.tail = None
        self.next = None
        self.size = 0

        if values is not None:
            for value in values:
                self.append(value)


    def __str__(self):
        current = self.head
        out = []
        while current:
            out.append(repr(current.data))
            current = current.next
        return f"LinkedList([{', '.join(out)}])"


    def __repr__(self):
        return self.__str__()


    def __len__(self):
        return self.size

    def __iter__(self):
        cur = self.head
        while cur is not None:
            yield cur.data
            cur = cur.next


    def is_empty(self):

        return self.head is None


    def prepend(self, data):

        new_node = Node(data, next=self.head)


        self.head = new_node


        if self.tail is None:
            self.tail = new_node


        self.size += 1


    def append(self, data):

        node = Node(data)


        if self.tail is None:
            self.head = self.tail = node
        else:

            self.tail.next = node

            self.tail = node


        self.size += 1

    def insert(self, index, data):

        if index >= self.size:
            self.append(data)
            return


        if index == 0:
            self.prepend(data)
            return


        prev = self._node_at(index - 1)


        node = Node(data, next=prev.next)


        prev.next = node


        self.size += 1

    def pop_head(self):

        if self.head is None:
            raise IndexError("pop from empty list")

        data = self.head.data


        if self.head.next is None:
            self.head = None
            self.tail = None

        else:
            self.head = self.head.next


        self.size -= 1


        return data

    def pop_tail(self):

        if self.head is None:
            raise IndexError("pop from empty list")


        if self.head.next == None:
            return self.pop_head()


        else:
            prev = self._node_at(self.size - 2)
            data = prev.next.data
            prev.next = None
            self.tail = prev
            self.size -= 1
            return data

    def remove(self, index):

        if index < 0 or index >= self.size:
            raise IndexError("index out of range")


        if index == 0:
            return self.pop_head()


        else:
            prev      = self._node_at(index - 1)
            cur       = prev.next
            prev.next = cur.next


            if prev.next is None:
                self.tail = prev

        self.size -= 1
        return cur.data


    def get(self, index):
        return self._node_at(index).data

    def set(self, index, data):
        self._node_at(index).data = data


    def _node_at(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")
        cur = self.head
        for _ in range(index):
            cur = cur.next
        return cur

    def index_of(self, data):

        index = 0
        cur = self.head
        while cur is not None:
            if cur.data == data:
                return index
            cur = cur.next
            index += 1
        raise ValueError()


    def contains(self, data):
        cur = self.head
        while cur is not None:
            if cur.data == data:
                return True
            cur = cur.next
        return False

    def reverse(self):
        prev = None
        cur = self.head
        self.tail = self.head
        while cur is not None:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def to_list(self):
        return list(self)

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0


    def extend(self, other):
        self.tail.next = other.head
        self.tail = other.tail
        self.size += other.size

    def sort(self):
        nodes = self.to_list()
        nodes.sort()
        self.clear()
        for node in nodes:
            self.append(node)
```

---

## All operations (with examples and complexity)

Examples below use small integers or strings where the focus is pointer mechanics. In a weather script, the same methods apply when `data` is a `DailyReading`, a `reading_id`, or a row dict—costs depend on **chain length**, not on whether `data` is a float or a dict.

```mermaid
flowchart TB
  subgraph fast["O(1) with head / tail / size"]
    prepend
    pop_head
    append["append (with tail)"]
    len_op["len / is_empty"]
  end
  subgraph linear["O(n) — traverse"]
    get
    insert_at["insert(i)"]
    remove_at["remove(i)"]
    index_of
    contains
    pop_tail
    reverse
  end
```

### `is_empty()` / `len(ll)`

```python
ll = LinkedList()
assert ll.is_empty()
assert len(ll) == 0

ll.append(1)
assert not ll.is_empty()
assert len(ll) == 1
```

| | |
| --- | --- |
| **Time** | O(1) when `size` is maintained; O(n) if you walk the chain each time |
| **Space** | O(1) |

---

### `prepend(data)` — insert at head

New node points to old head; update `head` (and `tail` if list was empty).

```python
ll = LinkedList([2, 3])
ll.prepend(1)
assert list(ll) == [1, 2, 3]

buffer = LinkedList([
    DailyReading(201, 3, 0.2, "overcast"),
    DailyReading(202, 3, -0.5, "windy"),
])
buffer.prepend(DailyReading(200, 3, 0.0, "sensor backfill"))
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) auxiliary (one new node) |

**Weather note:** Prepending every day in a multi-year archive would still be Θ(n) nodes total; you are choosing O(1) **per prepend**, not O(1) for the whole dataset.

```mermaid
sequenceDiagram
  participant L as list
  participant New as new node
  participant Old as old head
  L->>New: create Node(data)
  New->>Old: next = head
  L->>L: head = New
```

---

### `append(data)` — insert at tail

With a **tail pointer**, no traversal. Without tail, each append is O(n).

```python
ll = LinkedList()
ll.append("a")
ll.append("b")
assert list(ll) == ["a", "b"]

series = LinkedList()
series.append(DailyReading(1, 1, 0.3, "mild"))
series.append(DailyReading(2, 1, 1.1, "warm spell"))
```

| | |
| --- | --- |
| **Time** | O(1) with `tail`; O(n) if only `head` |
| **Space** | O(1) auxiliary per append |

**Weather note:** Appending each daily row as a window grows matches live ingest: O(1) amortized per reading **if** you keep `tail`, same idea as [array-based list](../array-based-lists/index.md) `append` on a growing table.

```mermaid
flowchart LR
  subgraph before["Before append(x)"]
    H1["head"] --> A["a"] --> B["b"] --> NIL["None"]
    T1["tail"] --> B
  end
  subgraph after["After"]
    H2["head"] --> A2["a"] --> B2["b"] --> X["x"] --> NIL2["None"]
    T2["tail"] --> X
  end
  before --> after
```

---

### `insert(index, data)` — insert before position `index`

Index `0` delegates to `prepend`. Otherwise find the **predecessor** at `index - 1` and splice in.

```python
ll = LinkedList([10, 30])
ll.insert(1, 20)
assert list(ll) == [10, 20, 30]

ll.insert(0, 5)
assert list(ll) == [5, 10, 20, 30]
```

| | |
| --- | --- |
| **Time** | O(n) — O(i) to find position + O(1) rewire |
| **Space** | O(1) auxiliary |

```mermaid
flowchart TD
  S([insert at index i])
  S --> Z{i == 0?}
  Z -->|yes| P[prepend — O(1)]
  Z -->|no| W[walk i-1 steps to predecessor]
  W --> R[rewire: prev.next = new; new.next = old next]
```

---

### `get(index)` / `set(index, data)`

No shortcut: walk from head.

```python
ll = LinkedList(["a", "b", "c"])
assert ll.get(1) == "b"
ll.set(1, "B")
assert ll.get(1) == "B"
```

| | |
| --- | --- |
| **Time** | O(n) worst case (index near end); O(i) for index `i` |
| **Space** | O(1) |

**Weather note:** “Give me reading index 7 in this window” without a `list` backing store is O(i) pointer hops. If you need random day access repeatedly, materialize `series.to_list()` once or keep a Python `list` for that window.

---

### `pop_head()` — remove first element

```python
ll = LinkedList([1, 2, 3])
assert ll.pop_head() == 1
assert list(ll) == [2, 3]
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

---

### `pop_tail()` — remove last element

Singly linked list needs the **predecessor** of the tail—full scan O(n).

```python
ll = LinkedList([1, 2, 3])
assert ll.pop_tail() == 3
assert list(ll) == [1, 2]
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

For O(1) pops at both ends in Python, use `collections.deque` ([deque](../dequeue-deque/index.md)) or a [doubly linked list](../doubly-linked-list/index.md).

---

### `remove(index)` — delete by position

```python
ll = LinkedList([10, 20, 30])
assert ll.remove(1) == 20
assert list(ll) == [10, 30]
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

```mermaid
sequenceDiagram
  participant L as list
  participant Prev as predecessor
  participant Target as node at index
  L->>Prev: walk to index-1
  Prev->>Target: cur.next
  Note over Prev,Target: prev.next = target.next — O(1) rewire
```

If you hold a **node reference** but not its index or predecessor, see [copy-value hack](#delete-node-when-you-only-have-the-node-singly-linked) below—or use a [doubly linked list](../doubly-linked-list/index.md).

---

### `index_of(data)` / `contains(data)`

Linear search.

```python
ll = LinkedList(["x", "y", "z"])
assert ll.index_of("y") == 1
assert ll.contains("z")
assert not ll.contains("w")
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

---

### `clear()`

Drop `head` (and `tail`); let garbage collection reclaim nodes.

```python
ll = LinkedList([1, 2, 3])
ll.clear()
assert ll.is_empty() and len(ll) == 0
```

| | |
| --- | --- |
| **Time** | O(1) to clear references; O(n) if you iterate to free explicitly |
| **Space** | O(1) |

---

### `reverse()` — in-place reverse

Iterative three-pointer walk (`prev`, `cur`, `nxt`); update `head` and `tail`.

```python
ll = LinkedList([1, 2, 3])
ll.reverse()
assert list(ll) == [3, 2, 1]
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) auxiliary |

```mermaid
flowchart LR
  subgraph step["One step"]
    P["prev"] --> C["cur"]
    C --> N["nxt"]
  end
  Note["cur.next = prev; advance all three"]
```

Recursive reverse (educational):

```python
def reverse_recursive(head):
    if head is None or head.next is None:
        return head
    new_head = reverse_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) call stack depth |

---

### `extend(other)` / `to_list()`

`extend` splices another `LinkedList` onto the tail in O(1) pointer steps (no new nodes). The constructor `LinkedList(values)` builds from an iterable by calling `append` for each item.

```python
ll = LinkedList([1, 2, 3])
tail = LinkedList([4, 5])
ll.extend(tail)
assert ll.to_list() == [1, 2, 3, 4, 5]
assert tail.to_list() == [4, 5]
```

| Operation | Time | Space |
| --- | --- | --- |
| `extend` | O(1) pointer splice | O(1) — reuses `other`'s nodes |
| `to_list` | O(n) | O(n) new Python `list` |

---

### `sort()` — in-place sort via materialize

Converts to a Python `list`, sorts in place, clears the chain, and rebuilds with `append`. Simple and correct; not an in-node pointer sort.

```python
ll = LinkedList([3, 1, 4, 2])
ll.sort()
assert ll.to_list() == [1, 2, 3, 4]
```

| | |
| --- | --- |
| **Time** | O(n log n) — dominated by Python's Timsort |
| **Space** | O(n) for the temporary `list` |

---

### Iteration: `for x in ll` / `__iter__`

```python
ll = LinkedList([10, 20, 30])
total = sum(x for x in ll)
assert total == 60

series = LinkedList([
    DailyReading(1, 1, 0.5, "a"),
    DailyReading(2, 1, -0.3, "b"),
    DailyReading(3, 1, 0.2, "c"),
])
series_anomaly = sum(r.temp_anomaly for r in series)
```

| | |
| --- | --- |
| **Time** | O(n) full traversal |
| **Space** | O(1) auxiliary |

This is the right pattern for **aggregate on a chain** (sum temp anomaly, count cold fronts). For **aggregate on a full archive**, traverse a table or column once—still O(n), but *n* is all daily rows and the structure should be a `list`/DataFrame, not a linked list of 50k nodes.

Manual walk (no wrapper class):

```python
def walk(head):
    cur = head
    while cur is not None:
        print(cur.data)
        cur = cur.next
```

---

## Low-level pointer operations (no class)

Useful in interviews and for understanding splice logic.

### Insert after a known node (not necessarily head)

You already hold reference `node`; no search.

```python
def insert_after(node, data):
    node.next = Node(data, next=node.next)
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### Delete `node` when you only have the node (singly linked)

On a singly linked list, normal deletion needs the **predecessor** to set `predecessor.next = node.next`. If you only hold a reference to `node` itself, finding that predecessor costs **O(n)**.

The **copy-value hack** avoids the predecessor scan when you may **mutate** `node.data`:

1. Copy `node.next.data` into `node.data`.
2. Delete `node.next` instead — O(1) when you hold `node`, because `node` is the predecessor of `node.next`.

```python
def delete_node_copy_hack(node: Node) -> None:
    if node.next is None:
        raise ValueError("cannot delete tail with copy-value hack")
    node.data = node.next.data
    node.next = node.next.next
```

Weather example: a timeline holds a `Node` for “Day 102 — cold front”. You want to drop that day without scanning from the head; copy Day 103’s data into Day 102’s node, then unlink Day 103.

```python
n3 = Node(DailyReading(103, 2, 0.1, "light rain"))
n2 = Node(DailyReading(102, 2, -1.2, "cold front"), next=n3)
n1 = Node(DailyReading(101, 2, 0.4, "partly cloudy"), next=n2)

delete_node_copy_hack(n2)

assert n1.next.data.reading_id == 103
assert n1.next.next is None
```

| | |
| --- | --- |
| **Time** | O(1) when `node.next` is not `None` |
| **Space** | O(1) |

| Caveat | Why it matters |
| --- | --- |
| **Tail node** | No `node.next` — hack fails; scan for predecessor or use a [doubly linked list](../doubly-linked-list/index.md) |
| **Mutates data in place** | The node at that address keeps its identity but holds a different day’s readings |
| **Stale references** | After unlinking `node.next`, other pointers to that detached node are invalid |
| **Production dashboards** | Prefer doubly linked `remove_node` or pass the predecessor explicitly |

```mermaid
sequenceDiagram
  participant N as node (Day 102)
  participant Nxt as node.next (Day 103)
  N->>N: data = Nxt.data
  N->>N: next = Nxt.next
  Note over N: Day 102 slot now holds Day 103 data; Day 103 node dropped
```

For contrast, a [doubly linked list](../doubly-linked-list/index.md) rewires `prev` and `next` in true O(1) without copying values.

### Dummy head sentinel

Simplifies “delete head” and “insert before head” in one uniform loop.

```python
def remove_all_greater_than(head, limit):
    dummy = Node(0, next=head)
    prev = dummy
    while prev.next is not None:
        if prev.next.data > limit:
            prev.next = prev.next.next
        else:
            prev = prev.next
    return dummy.next
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) extra (dummy node) |

```mermaid
flowchart LR
  D["dummy"] --> H["real head"] --> N1 --> N2 --> NIL["None"]
```

---

## Master complexity table

Let **n** = `len(ll)`, **i** = index. For weather work, map **n** to the chain you are holding (days in one window, nodes in a merge sketch)—not archive row count unless you mistakenly built one giant linked list.

| Operation | Time | Space (auxiliary) | Notes |
| --- | --- | --- | --- |
| Create empty | O(1) | O(1) | |
| Build from *k* items (tail append) | O(k) | O(k) nodes | |
| Build from *k* items (head prepend) | O(k) | O(k) | reversed order |
| `prepend` | O(1) | O(1) | |
| `append` (with tail) | O(1) | O(1) | |
| `append` (head only) | O(n) | O(1) | |
| `insert(i)` | O(n) | O(1) | find + splice |
| `get` / `set` at `i` | O(i) ≤ O(n) | O(1) | |
| `pop_head` | O(1) | O(1) | |
| `pop_tail` | O(n) | O(1) | singly linked |
| `remove(i)` | O(n) | O(1) | |
| `index_of` / `contains` | O(n) | O(1) | |
| `len` (cached) | O(1) | O(1) | |
| `len` (walk) | O(n) | O(1) | |
| `clear` | O(1) | O(1) | drop head |
| `reverse` iterative | O(n) | O(1) | |
| `reverse` recursive | O(n) | O(n) stack | |
| `extend` (splice `LinkedList`) | O(1) | O(1) | reuses nodes from `other` |
| `sort` | O(n log n) | O(n) | materialize + Timsort + rebuild |
| `to_list` | O(n) | O(n) | |
| Traverse all | O(n) | O(1) | sum temp anomaly on one window chain |
| Delete with node ref (copy-value hack) | O(1) | O(1) | fails on tail; mutates `node.data` |

**Storage for the whole structure:** Θ(n) nodes, each O(1) extra for `next` (and object headers in CPython). Storing a full multi-year archive as nodes costs Θ(all daily rows) memory with poor locality—use tabular storage instead.

---

## Classic patterns (with complexity)

These patterns appear in structure-heavy interview questions; they also describe **one-pass** logic you might apply to a **short** weather chain (one month window, two merged station logs) before you reach for pandas.

### Two pointers: find middle

Slow moves 1 step, fast moves 2; when fast hits end, slow is middle. On a daily chain, that is the middle **reading node** without knowing length ahead of time (still O(n); `size` on the class makes it O(1) if you trust cached length).

```python
def middle_node(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(1) |

### Detect cycle (Floyd)

If fast meets slow inside a cycle, loop exists.

```python
def has_cycle(head):
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

### Merge two sorted lists

**Weather use:** Two chains sorted by `reading_id` (e.g. January and February rows already sorted) can be merged into one chronological chain in O(n + m) pointer steps—no array shifts. Production merges usually sort keys in pandas/SQL; the linked version teaches the combine step.

```python
def merge_sorted(a, b):
    dummy = Node(0)
    tail = dummy
    while a is not None and b is not None:
        if a.data <= b.data:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a if a is not None else b
    return dummy.next
```

| | |
| --- | --- |
| **Time** | O(n + m) |
| **Space** | O(1) auxiliary (relinks existing nodes) |

```mermaid
sequenceDiagram
  participant A as list A
  participant B as list B
  participant Out as merged chain
  loop while both non-empty
    Out->>A: compare heads
    Out->>Out: attach smaller node
  end
  Out->>Out: attach remainder
```

---

## Python stdlib: what to use instead

| Need | Prefer | Why |
| --- | --- | --- |
| Fast indexing, slicing | `list` | O(1) index; cache-friendly |
| Full daily observation archive | `list` / **pandas** / parquet | Random access, vectorized stats, joins by `station_id` |
| Queue / stack at both ends | `collections.deque` | O(1) `append` / `pop` both ends—live reading queue, rolling window |
| Station lookup by id | `dict` | O(1) average after index build—not a linked list |
| Ordered mapping | `dict` (3.7+ insertion order) | Station order sketches; not pointer chains |
| Learning / interviews | `Node` + `LinkedList` (this page) | Pointer discipline |
| Merge / reverse on **nodes** | Custom linked list or algorithm on `Node` | Teaches merge-sort chain step |

```python
from collections import deque


recent = deque(maxlen=10)
recent.append(9021)
recent.appendleft(9020)
```

`deque` is **not** a singly linked list you implement in Python—it is a C-level block deque. Treat it as the practical weather tool when the *reason* you wanted a linked list was O(1) push/pop at both ends of a **small** buffer.

---

## Linked list vs Python `list` — when to choose which

```mermaid
flowchart TD
  Q([What do you need most?])
  Q --> I{Random access by index?}
  I -->|yes| PY["Python list"]
  I -->|no| E{Frequent inserts at head?}
  E -->|yes| LL["Singly linked list or deque"]
  E -->|no| M{Middle insert/delete in hot loop?}
  M -->|yes, in Python code| PY2["Often still list — measure first"]
  M -->|theory / interview| LL2["Linked list"]
  E -->|FIFO at scale| DQ["collections.deque"]
```

| Scenario | Linked list | Python `list` |
| --- | --- | --- |
| `get(i)` in a loop | O(n) each — painful | O(1) |
| Prepend in a tight loop | O(1) each | O(n) per `insert(0)` |
| Memory per element | Value + `next` + object overhead | One reference in array |
| Merge sort on sequence | Natural for linked nodes | [Merge sort](../../algorithms/merge-sort/index.md) often uses arrays in Python |
| Multi-year climate aggregates | Wrong default structure | `DataFrame` / `list` of rows + `dict` indexes |
| One month window, algorithm homework | Clear teaching model | Still fine to use `list` in prod for one window |

---

## Common pitfalls

| Pitfall | Why it hurts | Better approach |
| --- | --- | --- |
| Losing `head` reference | Rest of chain unreachable | Always assign to `self.head` or return new head |
| No `tail` but frequent `append` | O(n²) builds | Keep `tail` pointer |
| `pop_tail` on singly linked list | Must scan to predecessor | Doubly linked list or `deque` |
| `remove(node)` without predecessor | Cannot rewire in O(1) | Pass predecessor, use copy-value hack (with caveats), or use [doubly linked list](../doubly-linked-list/index.md) |
| Copy-value hack on tail node | No `node.next` to copy from | Scan for predecessor or use doubly linked list |
| `extend` shares nodes with `other` | Mutating one list affects both | Copy data with `to_list()` + rebuild if isolation matters |
| Using linked list for `xs[i]` hot paths | O(n) per access | `list` or array |
| Storing full archive as nodes | Huge overhead, slow scans | Parquet/CSV → pandas; index stations with `dict` |
| `get(i)` for every day in every window | O(windows × days²) if nested wrong | Store window as `list` or one traverse per window |
| Confusing chain *n* with table *n* | Mis-estimate Big-O | Name *n*: days in **this** list only |

---

## Related structures in this guide

| Structure | Difference |
| --- | --- |
| [Array-based lists](../array-based-lists/index.md) | Contiguous dynamic array; Python `list` |
| [Doubly linked list](../doubly-linked-list/index.md) | `prev` pointer; O(1) delete with node reference (no copy-value hack) |
| [Circularly linked list](../circularly-linked-list/index.md) | Last `next` points to head; round-robin |
| [Stacks](../stacks/index.md) | LIFO—often `list.append` / `pop` or linked head |
| [Queue](../queue/index.md) | FIFO—`deque` over singly linked `pop(0)` |

Official Python sequences tutorial (arrays, not linked lists): [Data Structures — More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists).

---

## Quick reference card

```python
head = None
ll = LinkedList([1, 2, 3])

ll.prepend(0)
x = ll.pop_head()
ll.append(4)
ll.get(i)
ll.insert(i, x)
ll.remove(i)
ll.pop_tail()
ll.extend(other_ll)
ll.sort()

for reading in ll:
    ...
```

Use a singly linked list when the **algorithm** is defined in terms of pointer rewiring (merge, reverse, cycle detection) or when inserts at the **head** dominate—often on **small** weather chains (one month window, two sorted streams). Use Python’s `list`, **pandas**, or `deque` when the **machine and library** should carry archive-scale load.

**Weather pipeline checklist**

1. **Default** — Daily observation table in pandas/`list`; station index in `dict`.
2. **Chain** — Use linked list (or `deque`) only when order and O(1) ends matter for a **bounded** buffer or exercise.
3. **Count *n*** — Days in this window, not rows in the full archive file.
4. **Hot loop** — Never `get(i)` inside `for each day in archive`; walk the chain once or vectorize.
5. **Delete with node ref** — Use copy-value hack only when mutation is OK; prefer doubly linked list in production timelines.
