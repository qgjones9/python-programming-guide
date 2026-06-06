# Binary search tree

A **binary tree** where, for every node, all keys in the **left** subtree are **strictly smaller** and all keys in the **right** subtree are **strictly greater**. That ordering lets you **search**, **insert**, and **delete** by walking one branch at each level—like a filing cabinet sorted by station id or day number.

| | |
| --- | --- |
| **What it is** | A rooted binary tree with the BST invariant: `left.key < node.key < right.key` at every node. |
| **Core operations** | `search`, `insert`, `delete`, traversals (`inorder` yields sorted keys). |
| **Height matters** | Time is O(h) where **h** = height. Balanced tree: h = O(log n). Sorted input: h = O(n). |
| **When to use** | Ordered lookup, range queries, and sorted iteration when you control shape or will upgrade to AVL/red–black. |
| **Trade-off** | Simple and teachable; **unbalanced** input degrades to linked-list speed. |

In **daily weather data analysis**, a BST is the right mental model for **ranking and range queries on ordered readings**: store `(temp_anomaly, station_id)` pairs, walk left/right to find an anomaly threshold, or run **inorder traversal** to print the station leaderboard in ascending order. For a full multi-year archive you will still use **pandas** or **`sorted()`**—implement a BST to learn the invariant, to support **range scans** (all stations between +0.5°C and +1.2°C anomaly), and as the foundation for [AVL](../avl-tree/index.md) and [red–black](../red-black-tree/index.md) trees.

This page is your **ready reference**: structure, a complete Python implementation, every way to create it, every method with daily weather data examples, and **time and space complexity** on each operation. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How a BST fits daily weather analysis

| Weather analysis idea | BST view | Why ordering helps |
| --- | --- | --- |
| **Anomaly leaderboard** | Key = `(temp_anomaly, station_id)`; inorder = ascending rank | O(n) sorted walk without separate sort step |
| **Find station at anomaly cutoff** | Search for `(0.9, ?)` or nearest neighbor | O(h) descent vs O(n) linear scan |
| **Day-of-year schedule lookup** | Key = `(day_of_year, reading_id)` | Range query: all readings in days 120–150 |
| **Heat-threshold filter** | Insert daily anomalies; query "who exceeded +2°C?" | Left = below, right = above |
| **Hourly observation index** | Key = `(hour_utc, reading_id)` | Ordered replay scrubber on one storm event |

**Use pandas / `dict` / `sorted()`** when you load 20,000 daily rows once and filter in vectorized code. **Use a BST** when the problem is **incremental ordered inserts**, **online** nearest/range queries on a **moderate** *n*, or when you are **learning balancing** on top of this base.

```mermaid
flowchart TB
  subgraph bst["BST keyed by temp anomaly"]
    R["(+1.2, STN_A)"]
    L["(+0.8, STN_B)"]
    RR["(+1.5, STN_C)"]
    RL["(+1.3, STN_D)"]
    R --> L
    R --> RR
    RR --> RL
  end
  note["inorder: STN_B → STN_A → STN_D → STN_C"]
```

Throughout this page, **n** is the number of nodes. **h** is tree height.

---

## BST vs balanced trees vs Python builtins

| | **BST (this page)** | [AVL tree](../avl-tree/index.md) | [Red–black tree](../red-black-tree/index.md) | **`dict` / `set`** | **`sorted()` / pandas** |
| --- | --- | --- | --- | --- | --- |
| **Search** | O(h) | O(log n) guaranteed | O(log n) guaranteed | O(1) avg hash | O(log n) if sorted list + bisect |
| **Insert** | O(h) | O(log n) + rotations | O(log n) + recolor/rotate | O(1) avg | O(n) resort or O(log n) bisect insert |
| **Sorted iteration** | O(n) inorder | O(n) inorder | O(n) inorder | O(n) arbitrary order | O(n) already sorted |
| **Ordering** | Total order on keys | Same | Same | Keys hashable; **not** sorted | Sort any column |
| **Weather fit** | Teach ordered search | Guaranteed log for live feed | Library map theory | `station_id → reading` lookup | Multi-year tables, climatology ranks |

!!! note "Python `dict` is not a BST"
    CPython **`dict`** and **`set`** use **hash tables**, not binary search trees. Average O(1) lookup by key; **no** in-order traversal of keys by value order unless you sort separately. Ordered **insertion** since 3.7 is by **insertion order**, not by key comparison.

```mermaid
sequenceDiagram
  participant Analyst
  participant BST as anomaly BST
  Analyst->>BST: search (+1.1, ?)
  BST->>BST: compare at root +1.2 — go left
  BST->>BST: compare at +0.8 — go right
  BST-->>Analyst: found or nearest O(h)
```

---

## Node definition

Each node stores a **key** (comparable tuple or dataclass) and **left** / **right** child pointers.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator


@dataclass(frozen=True, order=True)
class StationReading:
    temp_anomaly: float
    station_id: str
    summary: str = ""


@dataclass
class BSTNode:
    key: Any
    left: BSTNode | None = None
    right: BSTNode | None = None
    payload: Any = None
```

| | |
| --- | --- |
| **Time** | O(1) to construct one node |
| **Space** | O(1) per node (key + two refs + header) |

```mermaid
flowchart TB
  subgraph node["BSTNode"]
    K["key: StationReading"]
    L["left"]
    R["right"]
  end
  L --- K
  K --- R
```

---

## Ways to create a binary search tree

### 1. Empty tree — root is `None`

```python
root: BSTNode | None = None
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Empty `BinarySearchTree` wrapper

```python
class BinarySearchTree:
    def __init__(self) -> None:
        self.root: BSTNode | None = None
        self._size = 0

tree = BinarySearchTree()
assert tree.is_empty()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 3. Single-node tree

```python
root = BSTNode(StationReading(1.2, "STN01", "warm spell"))
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 4. Build from iterable — repeated insert

Preserves **BST shape** depends on **insert order**—same keys, different order → different shape.

```python
def insert_bst(root: BSTNode | None, key: Any) -> BSTNode:
    if root is None:
        return BSTNode(key)
    if key < root.key:
        root.left = insert_bst(root.left, key)
    elif key > root.key:
        root.right = insert_bst(root.right, key)
    return root

readings = [
    StationReading(1.2, "STN01"),
    StationReading(0.8, "STN02"),
    StationReading(1.5, "STN03"),
]
root = None
for r in readings:
    root = insert_bst(root, r)
```

| | |
| --- | --- |
| **Time** | O(n · h) — O(n log n) if balanced, O(n²) if sorted input |
| **Space** | O(n) nodes + O(h) recursion stack |

### 5. Build from **sorted** list — degenerates to a chain

Inserting strictly increasing `(temp_anomaly, id)` mimics **sorted daily CSV** row-by-row: every insert goes right → **h = n**.

```python
sorted_anomalies = [StationReading(a / 10, f"S{a}") for a in range(10, 200, 10)]
root = None
for r in sorted_anomalies:
    root = insert_bst(root, r)
```

| | |
| --- | --- |
| **Time** | O(n²) |
| **Space** | O(n) |

### 6. Random shuffle before insert — expected O(log n) height

```python
import random

shuffled = readings[:]
random.shuffle(shuffled)
root = None
for r in shuffled:
    root = insert_bst(root, r)
```

| | |
| --- | --- |
| **Time** | O(n log n) expected |
| **Space** | O(n) |

---

## Full implementation: `BinarySearchTree`

The class below implements **search**, **insert**, **delete**, **min/max**, **inorder/preorder/postorder**, **size**, **height**, and **range query**—enough for weather anomaly drills and interview follow-ups.

```python
class BinarySearchTree:
    def __init__(self) -> None:
        self.root: BSTNode | None = None
        self._size = 0

    def is_empty(self) -> bool:
        return self.root is None

    def __len__(self) -> int:
        return self._size

    def search(self, key: Any) -> BSTNode | None:
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def contains(self, key: Any) -> bool:
        return self.search(key) is not None

    def insert(self, key: Any, payload: Any = None) -> None:
        if self.root is None:
            self.root = BSTNode(key, payload=payload)
            self._size += 1
            return
        cur = self.root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = BSTNode(key, payload=payload)
                    self._size += 1
                    return
                cur = cur.left
            elif key > cur.key:
                if cur.right is None:
                    cur.right = BSTNode(key, payload=payload)
                    self._size += 1
                    return
                cur = cur.right
            else:
                cur.payload = payload
                return

    def delete(self, key: Any) -> bool:
        self.root, deleted = self._delete_rec(self.root, key)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_rec(
        self, node: BSTNode | None, key: Any
    ) -> tuple[BSTNode | None, bool]:
        if node is None:
            return None, False
        if key < node.key:
            node.left, deleted = self._delete_rec(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete_rec(node.right, key)
            return node, deleted
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        succ = self._min_node(node.right)
        node.key = succ.key
        node.payload = succ.payload
        node.right, _ = self._delete_rec(node.right, succ.key)
        return node, True

    def _min_node(self, node: BSTNode) -> BSTNode:
        while node.left is not None:
            node = node.left
        return node

    def minimum(self) -> Any | None:
        if self.root is None:
            return None
        return self._min_node(self.root).key

    def maximum(self) -> Any | None:
        if self.root is None:
            return None
        cur = self.root
        while cur.right is not None:
            cur = cur.right
        return cur.key

    def inorder(self) -> list[Any]:
        out: list[Any] = []
        self._inorder_rec(self.root, out)
        return out

    def _inorder_rec(self, node: BSTNode | None, out: list[Any]) -> None:
        if node is None:
            return
        self._inorder_rec(node.left, out)
        out.append(node.key)
        self._inorder_rec(node.right, out)

    def inorder_iter(self) -> Iterator[Any]:
        stack: list[BSTNode] = []
        cur = self.root
        while stack or cur is not None:
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            yield cur.key
            cur = cur.right

    def preorder(self) -> list[Any]:
        out: list[Any] = []
        self._preorder_rec(self.root, out)
        return out

    def _preorder_rec(self, node: BSTNode | None, out: list[Any]) -> None:
        if node is None:
            return
        out.append(node.key)
        self._preorder_rec(node.left, out)
        self._preorder_rec(node.right, out)

    def postorder(self) -> list[Any]:
        out: list[Any] = []
        self._postorder_rec(self.root, out)
        return out

    def _postorder_rec(self, node: BSTNode | None, out: list[Any]) -> None:
        if node is None:
            return
        self._postorder_rec(node.left, out)
        self._postorder_rec(node.right, out)
        out.append(node.key)

    def height(self) -> int:
        return self._height_rec(self.root)

    def _height_rec(self, node: BSTNode | None) -> int:
        if node is None:
            return -1
        return 1 + max(self._height_rec(node.left), self._height_rec(node.right))

    def range_query(self, lo: Any, hi: Any) -> list[Any]:
        out: list[Any] = []
        self._range_rec(self.root, lo, hi, out)
        return out

    def _range_rec(
        self, node: BSTNode | None, lo: Any, hi: Any, out: list[Any]
    ) -> None:
        if node is None:
            return
        if lo < node.key:
            self._range_rec(node.left, lo, hi, out)
        if lo <= node.key <= hi:
            out.append(node.key)
        if hi > node.key:
            self._range_rec(node.right, lo, hi, out)
```

| | |
| --- | --- |
| **Time to construct class** | O(1) |
| **Space** | O(n) for tree storage |

---

## Operations reference (with weather examples)

### `search` / `contains` — find a station by `(temp_anomaly, id)`

```python
tree = BinarySearchTree()
tree.insert(StationReading(1.2, "STN01", "warm spell"))
tree.insert(StationReading(0.8, "STN02", "cold front"))

node = tree.search(StationReading(0.8, "STN02"))
assert node is not None and node.key.summary == "cold front"
assert tree.contains(StationReading(9.9, "X")) is False
```

| | |
| --- | --- |
| **Time** | O(h) |
| **Space** | O(1) iterative; O(h) recursive variant |

```mermaid
flowchart TD
  Start([search key K]) --> R{root None?}
  R -->|yes| NF([return None])
  R -->|no| C{K vs node.key}
  C -->|K == node| Found([return node])
  C -->|K < node| L([go left])
  C -->|K > node| RI([go right])
  L --> R
  RI --> R
```

---

### `insert` — add daily reading

```python
tree = BinarySearchTree()
for anomaly, sid, summary in [(1.1, "STN01", "A"), (0.95, "STN02", "B"), (1.3, "STN03", "C")]:
    tree.insert(StationReading(anomaly, sid, summary))
assert len(tree) == 3
```

| | |
| --- | --- |
| **Time** | O(h) |
| **Space** | O(1) iterative; O(h) if recursive |

---

### `delete` — remove decommissioned station from active index

Three cases: **no left child**, **no right child**, **two children** (replace with inorder successor from right subtree).

```python
tree = BinarySearchTree()
for r in [
    StationReading(1.2, "STN01"),
    StationReading(0.8, "STN02"),
    StationReading(1.5, "STN03"),
    StationReading(1.3, "STN04"),
]:
    tree.insert(r)

tree.delete(StationReading(1.2, "STN01"))
assert tree.search(StationReading(1.2, "STN01")) is None
assert len(tree) == 3
ordered = tree.inorder()
assert ordered == sorted(ordered)
```

| Case | Action |
| --- | --- |
| Leaf | Unlink node |
| One child | Splice child up |
| Two children | Copy successor key; delete successor |

| | |
| --- | --- |
| **Time** | O(h) |
| **Space** | O(h) recursion stack |

```mermaid
flowchart TD
  D([delete key K]) --> F{found?}
  F -->|no| X([done False])
  F -->|yes| A{children?}
  A -->|0 or 1| S([splice child])
  A -->|2| SU([copy min of right subtree then delete it])
  S --> OK([done True])
  SU --> OK
```

---

### `inorder` — sorted anomaly leaderboard

**Inorder** (left → node → right) visits keys in **ascending** order—the BST's superpower for "print every station sorted by anomaly."

```python
tree = BinarySearchTree()
stats = [(1.05, "STN01"), (0.89, "STN02"), (1.4, "STN03"), (1.1, "STN04")]
for anomaly, sid in stats:
    tree.insert(StationReading(anomaly, sid))

leaderboard = [k.temp_anomaly for k in tree.inorder()]
assert leaderboard == [0.89, 1.05, 1.1, 1.4]
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) output; O(h) stack for `inorder_iter` |

```mermaid
flowchart LR
  L["left subtree sorted"] --> N["node"] --> R["right subtree sorted"]
  N --> OUT["full inorder = ascending anomaly"]
```

---

### `minimum` / `maximum` — floor / ceiling of anomaly

```python
tree = BinarySearchTree()
for a in [0.9, 1.2, 1.5]:
    tree.insert(StationReading(a, f"S{a}"))
assert tree.minimum().temp_anomaly == 0.9
assert tree.maximum().temp_anomaly == 1.5
```

| | |
| --- | --- |
| **Time** | O(h) |
| **Space** | O(1) |

---

### `range_query` — stations with +0.9°C to +1.2°C anomaly

```python
tree = BinarySearchTree()
for anomaly, sid in [(0.8, "a"), (0.95, "b"), (1.1, "c"), (1.3, "d")]:
    tree.insert(StationReading(anomaly, sid))

band = tree.range_query(StationReading(0.9, ""), StationReading(1.2, "zzz"))
anomalies = [k.temp_anomaly for k in band]
assert anomalies == [0.95, 1.1]
```

| | |
| --- | --- |
| **Time** | O(n) worst case (visit all); O(log n + k) typical for k results in balanced tree |
| **Space** | O(k) output + O(h) stack |

---

### `height` — detect degenerate "sorted insert" chain

```python
tree = BinarySearchTree()
for i in range(10):
    tree.insert(StationReading(i / 10, f"S{i}"))
assert tree.height() == 9
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(h) recursion |

---

## Weather application: live anomaly leaderboard

```python
class AnomalyLeaderboard:
    def __init__(self) -> None:
        self._tree = BinarySearchTree()

    def add_reading(self, station_id: str, summary: str, anomaly: float) -> None:
        node = self._tree.search(StationReading(0.0, station_id))
        if node is None:
            self._tree.insert(StationReading(anomaly, station_id, summary))
        else:
            old = node.key
            self._tree.delete(old)
            self._tree.insert(
                StationReading(old.temp_anomaly + anomaly, station_id, summary or old.summary)
            )

    def top_report(self, min_anomaly: float, max_anomaly: float) -> list[StationReading]:
        return self._tree.range_query(
            StationReading(min_anomaly, ""),
            StationReading(max_anomaly, "\uffff"),
        )

    def print_standings(self) -> None:
        for key in self._tree.inorder_iter():
            print(f"{key.station_id}: {key.temp_anomaly:+.1f}°C — {key.summary}")


board = AnomalyLeaderboard()
board.add_reading("STN01", "warm spell", 0.85)
board.add_reading("STN02", "cold front", 1.2)
board.add_reading("STN01", "warm spell", 0.4)
mid = board.top_report(1.0, 2.0)
assert len(mid) == 2
```

| Operation | Time | Space |
| --- | --- | --- |
| `add_reading` | O(h) search + delete + insert | O(1) aux |
| `top_report` | O(n) worst; O(log n + k) balanced | O(k) |
| `print_standings` | O(n) | O(h) stack |

---

## Weather application: schedule by `(day_of_year, reading_id)`

```python
@dataclass(frozen=True, order=True)
class ObservationSlot:
    day_of_year: int
    reading_id: str
    summary: str = ""


schedule = BinarySearchTree()
schedule.insert(ObservationSlot(120, "R001", "spring warm-up"))
schedule.insert(ObservationSlot(120, "R002", "coastal fog"))
schedule.insert(ObservationSlot(150, "R041", "heat wave onset"))

day120 = schedule.range_query(ObservationSlot(120, ""), ObservationSlot(120, "\uffff"))
assert len(day120) == 2
```

| Operation | Time | Notes |
| --- | --- | --- |
| Insert reading | O(h) | |
| Readings on day *d* | O(log n + k) balanced | k = readings that day |

---

## Python stdlib: what to use instead

| Need | Stdlib / ecosystem | vs hand-rolled BST |
| --- | --- | --- |
| Key → reading lookup | `dict[str, dict]` | O(1) avg; no sorted walk |
| Sort once, query many | `sorted(rows, key=...)` + bisect | Simpler for static daily CSV |
| Ordered multiset | `sortedcontainers.SortedList` (third party) | Production-grade balanced structure |
| Unique sorted keys | `set` + `sorted()` | Not incremental O(log n) unless bisect on list |

```python
import pandas as pd

df = pd.read_csv("daily_anomalies_2024.csv")
top = df[(df["temp_anomaly"] >= 0.9) & (df["temp_anomaly"] <= 1.2)].sort_values("temp_anomaly")
```

**Rule of thumb:** implement **`BinarySearchTree`** to learn and interview; use **pandas / dict / sorted list** for real multi-year pipelines unless you need **online** ordered structure semantics.

---

## Master complexity table

Let **n** = `len(tree)`, **h** = height.

| Operation | Time | Space (auxiliary) | Notes |
| --- | --- | --- | --- |
| Create empty | O(1) | O(1) | |
| Build from *n* inserts | O(n · h) | O(n) | O(n log n) if balanced |
| `search` / `contains` | O(h) | O(1) | |
| `insert` | O(h) | O(1) | |
| `delete` | O(h) | O(h) | recursive |
| `minimum` / `maximum` | O(h) | O(1) | |
| `inorder` / traversals | O(n) | O(h) stack | |
| `height` | O(n) | O(h) | |
| `range_query` | O(n) worst | O(k) output | O(log n + k) balanced |
| Storage | — | O(n) nodes | |

**Balanced vs skewed:** h = O(log n) random/balanced; h = O(n) sorted inserts.

---

## When to pick which structure (weather context)

```mermaid
flowchart TD
  Q([Ordered data problem?])
  Q --> S{Static multi-year CSV?}
  S -->|yes| P["pandas sort / dict lookup"]
  S -->|no| I{Need guaranteed log n?}
  I -->|yes| B["AVL or red–black"]
  I -->|no| T["Plain BST or sorted list + bisect"]
  T --> R{Insert order random?}
  R -->|yes| BST["BST OK expected log n"]
  R -->|no sorted| BAD["BST chain — balance or sort"]
```

| Scenario | Best tool |
| --- | --- |
| One-time climatology rank | pandas `sort_values` |
| Live incremental anomaly + sorted walk | BST → upgrade to AVL |
| Station ID → daily log | `dict`, not BST |
| Day range on observation schedule | BST range query or SQL `WHERE day BETWEEN` |
| Interview "implement map" | BST / red–black discussion |

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Sorted insert order | O(n) height, O(n) search | Shuffle, AVL, or sort-then-build |
| Duplicate keys undefined | Second insert may noop or overwrite | Document policy; use `(temp_anomaly, station_id)` tuple |
| Confusing `dict` with BST | Expect sorted keys from `{}` | Sort keys explicitly or use BST/SortedList |
| Delete two-child bug | Orphan subtree or broken order | Copy **successor** from right, not predecessor only |
| Range query wrong bounds | Miss edge keys | Use inclusive `lo <= key <= hi` and prune correctly |
| Storing entire DataFrame in nodes | Memory blowup | Index by key; payload = id or small record |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [AVL tree](../avl-tree/index.md) | Strict balance; rotations on insert/delete |
| [Red–black tree](../red-black-tree/index.md) | Relaxed balance; C++ `map` model |
| [Max heap](../max-heap/index.md) | Partial order for "top k" only |
| [Array-based lists](../array-based-lists/index.md) | Sorted list + bisect alternative |
| [Complexity analysis](../../complexity/index.md) | Big-O reference |
| [Data structures hub](../index.md) | All structures |

---

## Quick reference card

```python
tree = BinarySearchTree()
tree.insert(StationReading(1.2, "STN01", "warm spell"))

tree.search(StationReading(1.2, "STN01"))
tree.contains(key)
tree.delete(key)
tree.insert(key)

list(tree.inorder_iter())
tree.minimum()
tree.maximum()

tree.range_query(StationReading(0.9, ""), StationReading(1.2, "\uffff"))

len(tree)
tree.height()
```

Use a **binary search tree** when you need **ordered keys** with **search, insert, delete, and inorder iteration**—then move to **[AVL](../avl-tree/index.md)** or **[red–black](../red-black-tree/index.md)** when **worst-case O(log n)** must be guaranteed for live weather feeds and large *n*.
