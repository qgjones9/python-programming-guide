# Red–black tree

A **self-balancing binary search tree** where every node is colored **red** or **black** and five **coloring rules** guarantee height **O(log n)**. Inserts and deletes fix violations with **recoloring** and at most **two rotations**—the design behind many language **sorted maps** (C++ `std::map`, Java `TreeMap`), though **Python’s built-in `dict` is not a red–black tree**.

| | |
| --- | --- |
| **What it is** | A [BST](../binary-search-tree/index.md) plus color bit and RB invariants; root is black; no two consecutive reds on a path. |
| **Core operations** | `search`, `insert`, `delete` in O(log n) worst case. |
| **Balance** | Looser than [AVL](../avl-tree/index.md)—fewer rotations on write, slightly taller. |
| **When to use** | Understanding library map/set implementations; interview “design a sorted dictionary.” |
| **Trade-off** | More cases than AVL on paper; excellent amortized behavior in practice. |

In **NFL data analysis**, red–black trees are the **conceptual engine** behind **ordered maps** in other ecosystems: e.g. a `TreeMap<(week, game_id), GameInfo>` for schedule lookup with guaranteed log updates. In **Python**, you use **`dict`** for `player_id → stats` (hash table) and **pandas/SQL** for sorted reports—not an RB tree in stdlib. Learn RB trees to **compare balancing strategies** and to read **CPython-adjacent** designs (some third-party sorted containers use similar ideas).

This page is your **ready reference**: invariants, insert/delete fixups, Python teaching implementation, NFL analogies, and complexity tables. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## Red–black rules (invariants)

1. Every node is **red** or **black**.
2. The **root** is **black**.
3. Every **leaf (NIL)** is **black** (often represented as `None` with implicit black).
4. If a node is **red**, both children are **black** (no **double red**).
5. Every path from a node to its descendant NILs has the **same number of black nodes** (**black-height**).

Together, these force height ≤ **2 log(n + 1)**.

```mermaid
flowchart TB
  subgraph rb["Valid red–black tree — keys = fantasy points tiers"]
    B1["15 BLACK"]
    R1["8 RED"]
    B2["22 BLACK"]
    B1 --> R1
    B1 --> B2
    R1 --> N1["NIL"]
    R1 --> N2["NIL"]
    B2 --> N3["NIL"]
    B2 --> N4["NIL"]
  end
```

Throughout this page, **n** = node count.

---

## How red–black fits NFL-shaped problems

| NFL idea | RB tree view | Note |
| --- | --- | --- |
| **Schedule map** | Key `(week, slot)` → broadcast info | Ordered iteration by week |
| **Fantasy price ladder** | Sorted unique price points | Insert/delete with log guarantee |
| **Play clock events** | Timestamp-ordered tree | Other langs; Python uses heap/list often |
| **Compare to Python** | Mental model for Java/C++ maps | `dict` = hash, not RB |

**Ship Python with `dict` + sort.** **Study red–black** to explain **why sorted maps in C++/Java are O(log n)** and how that differs from Python hashing.

---

## Red–black vs AVL vs BST vs Python `dict`

| | **Red–black** | [AVL](../avl-tree/index.md) | [BST](../binary-search-tree/index.md) | **`dict` / `set`** |
| --- | --- | --- | --- | --- |
| **Worst search** | O(log n) | O(log n) | O(n) skewed | O(1) average |
| **Insert rotations** | ≤ 2 | ≤ 2 (stricter rebalance) | 0 | N/A |
| **Key order** | Inorder sorted | Inorder sorted | Inorder sorted | Insertion order (3.7+), not sort order |
| **Implementation** | Color cases | Balance factor | Simple | Hash + probe |
| **NFL lookup by player id** | Overkill in Python | Overkill | Overkill | **Correct tool** |

!!! note "Python `dict` is a hash table, not a red–black tree"
    **`dict`** gives average **O(1)** lookup by hashable key. It does **not** maintain **comparison-based sorted order**. Need sorted keys? **`sorted(d.keys())`**, **`bisect`** on a list, or third-party **`sortedcontainers.SortedDict`**.

```mermaid
sequenceDiagram
  participant Py as Python analyst
  participant D as dict hash
  participant RB as RB tree concept
  Py->>D: stats["Mahomes"] — O(1) avg
  Note over Py,D: No inorder by passing yards
  Py->>RB: inorder walk — sorted keys
  Note over RB: Used in Java TreeMap not in dict
```

---

## Node definition

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterator


class Color(Enum):
    RED = 0
    BLACK = 1


@dataclass(frozen=True, order=True)
class FantasyTier:
    points: float
    player_id: str


@dataclass
class RBNode:
    key: Any
    color: Color = Color.RED
    left: RBNode | None = None
    right: RBNode | None = None
    parent: RBNode | None = None  # optional; helps delete fixup
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) per node |

---

## Rotations (same as AVL)

```python
def _left_rotate(tree: "RedBlackTree", x: RBNode) -> None:
    y = x.right
    assert y is not None
    x.right = y.left
    if y.left is not None:
        y.left.parent = x
    y.parent = x.parent
    if x.parent is None:
        tree.root = y
    elif x is x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y


def _right_rotate(tree: "RedBlackTree", y: RBNode) -> None:
    x = y.left
    assert x is not None
    y.left = x.right
    if x.right is not None:
        x.right.parent = y
    x.parent = y.parent
    if y.parent is None:
        tree.root = x
    elif y is y.parent.right:
        y.parent.right = x
    else:
        y.parent.left = x
    x.right = y
    y.parent = x
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

```mermaid
flowchart LR
  subgraph rr["Right rotate at y"]
    Y["y"] --> X["x"]
    Y --> C["C"]
    X --> A["A"]
    X --> B["B"]
  end
  subgraph rrafter["After"]
    X2["x"] --> A2["A"]
    X2 --> Y2["y"]
    Y2 --> B2["B"]
    Y2 --> C2["C"]
  end
  rr --> rrafter
```

---

## Insert fixup (teaching outline)

Standard BST insert as **red**, then fix **double-red** violations walking up:

| Case | Condition | Action |
| --- | --- | --- |
| **1** | Parent black | Done |
| **2** | Uncle red | Recolor parent, uncle, grandparent; continue at grandparent |
| **3** | Uncle black, triangle | Rotate parent to line case |
| **4** | Uncle black, line | Rotate grandparent + recolor | 

```mermaid
flowchart TD
  INS([BST insert new node RED]) --> P{parent black?}
  P -->|yes| OK([done])
  P -->|no| U{uncle red?}
  U -->|yes| RC[recolor parent uncle gparent flip gparent RED]
  RC --> UP([move up to gparent])
  U -->|no| TRI[triangle → line via rotate parent]
  TRI --> LIN[line case rotate gparent + recolor]
  LIN --> ROOT[ensure root BLACK]
  ROOT --> OK
```

---

## Full implementation sketch: `RedBlackTree`

Teaching implementation with **insert** and **search** (delete is longer but follows CLRS symmetric fixup).

```python
class RedBlackTree:
    def __init__(self) -> None:
        self.root: RBNode | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def search(self, key: Any) -> RBNode | None:
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def insert(self, key: Any) -> None:
        node = RBNode(key, color=Color.RED)
        parent: RBNode | None = None
        cur = self.root
        while cur is not None:
            parent = cur
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return  # duplicate
        node.parent = parent
        if parent is None:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self._insert_fixup(node)
        self._size += 1

    def _insert_fixup(self, node: RBNode) -> None:
        while node.parent is not None and node.parent.color == Color.RED:
            assert node.parent.parent is not None
            if node.parent is node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle is not None and uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        _left_rotate(self, node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    _right_rotate(self, node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle is not None and uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        _right_rotate(self, node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    _left_rotate(self, node.parent.parent)
        if self.root is not None:
            self.root.color = Color.BLACK

    def inorder(self) -> list[Any]:
        out: list[Any] = []
        self._inorder(self.root, out)
        return out

    def _inorder(self, node: RBNode | None, out: list[Any]) -> None:
        if node is None:
            return
        self._inorder(node.left, out)
        out.append(node.key)
        self._inorder(node.right, out)

    def inorder_iter(self) -> Iterator[Any]:
        stack: list[RBNode] = []
        cur = self.root
        while stack or cur is not None:
            while cur is not None:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            yield cur.key
            cur = cur.right
```

| | |
| --- | --- |
| **Insert** | O(log n) time, O(1) rotations amortized |
| **Space** | O(n) |

---

## Ways to create a red–black tree

### 1. Empty tree

```python
tree = RedBlackTree()
```

### 2. Insert unsorted fantasy tiers

```python
tree = RedBlackTree()
for pts, pid in [(18.2, "QB1"), (12.1, "RB3"), (22.5, "WR7"), (15.0, "TE2")]:
    tree.insert(FantasyTier(pts, pid))
assert [k.points for k in tree.inorder()] == sorted([18.2, 12.1, 22.5, 15.0])
```

| | |
| --- | --- |
| **Time** | O(n log n) |
| **Space** | O(n) |

### 3. Sorted insert — still O(log n) height

Unlike plain BST, inserting ascending `(week, id)` stays balanced.

```python
tree = RedBlackTree()
for w in range(1, 19):
    tree.insert(FantasyTier(float(w), f"W{w}"))
# height O(log n) — contrast with BST chain
```

---

## Operations with NFL examples

### Search — find player at fantasy tier

```python
tree = RedBlackTree()
tree.insert(FantasyTier(19.5, "WR01"))
found = tree.search(FantasyTier(19.5, "WR01"))
assert found is not None
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(1) |

---

### Inorder — ascending fantasy points

```python
tree = RedBlackTree()
scores = [(14.0, "A"), (21.5, "B"), (9.0, "C")]
for p, pid in scores:
    tree.insert(FantasyTier(p, pid))
for k in tree.inorder_iter():
    print(f"{k.player_id}: {k.points}")
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(log n) stack |

---

## NFL application: ordered schedule (conceptual)

In Java/C++ you might write:

```text
TreeMap<WeekSlot, GameInfo> schedule;
schedule.put(new WeekSlot(1, "G001"), game);
```

Python equivalent patterns:

```python
# Lookup by id — use dict
games_by_id: dict[str, dict] = {"G001": {"week": 1, "matchup": "KC @ BAL"}}

# Sorted by week — sort once
games = sorted(games_by_id.values(), key=lambda g: (g["week"], g.get("id", "")))

# Or teaching RB tree
schedule_rb = RedBlackTree()
schedule_rb.insert(FantasyTier(1.0, "G001"))  # stand-in key type
```

| Approach | Lookup by id | Sorted by week |
| --- | --- | --- |
| `dict` | O(1) avg | Sort separately O(n log n) |
| Red–black (other langs) | O(log n) | Inorder O(n) |
| pandas | Column index | `sort_values` |

---

## Delete fixup (outline)

BST delete, then if removed node was black, fix **extra black** on path with sibling cases (CLRS §13.4). Same rotation primitives as insert.

| Case | Idea |
| --- | --- |
| Sibling red | Rotate parent; recolor |
| Sibling black, both nephews black | Recolor sibling red; propagate |
| Far nephew black | Rotate sibling; recolor |
| Near/far red nephew | Rotate parent; recolor |

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(log n) |

---

## Master complexity table

| Operation | Time | Space (aux) | Notes |
| --- | --- | --- | --- |
| Search | O(log n) | O(1) | |
| Insert | O(log n) | O(1) | ≤ 2 rotations |
| Delete | O(log n) | O(1) | ≤ 3 rotations |
| Inorder | O(n) | O(log n) | |
| Storage | — | O(n) | color + key + pointers |

---

## When to pick which structure

```mermaid
flowchart TD
  Q([Python NFL project?])
  Q -->|player lookup| D["dict"]
  Q -->|sorted report once| P["pandas sort_values"]
  Q -->|learn maps in C++/Java| RB["Red–black tree"]
  Q -->|stricter balance theory| AVL["AVL tree"]
```

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Assuming `dict` is ordered by value | Wrong API expectations | `sorted(d.items(), key=...)` |
| Forgetting to blacken root after insert | Invariant broken | Always set `root.color = BLACK` at end |
| Confusing insertion order with sort order | Python 3.7+ dict order ≠ sorted | Explicit sort or tree |
| Implementing delete before insert solid | RB delete is hardest | Master insert + rotations first |
| Using RB for hashable player IDs only | Hash wins in Python | `dict[str, Stats]` |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Binary search tree](../binary-search-tree/index.md) | Base ordering |
| [AVL tree](../avl-tree/index.md) | Stricter balance |
| [2-3-4 tree](../2-3-4-tree/index.md) | Isomorphic to RB |
| [Hash table](../hash-table/index.md) | Python `dict` |
| [Complexity analysis](../../complexity/index.md) | Big-O |
| [Data structures hub](../index.md) | Index |

---

## Quick reference card

```python
tree = RedBlackTree()
tree.insert(FantasyTier(17.5, "WR09"))
tree.search(FantasyTier(17.5, "WR09"))
list(tree.inorder_iter())  # sorted by points, player_id

# Invariants: root black; no red-red; equal black height on all paths
# Python production: dict for lookup, not RB tree
```

A **red–black tree** is the **standard balanced BST** behind many **sorted map** APIs—compare with **[AVL](../avl-tree/index.md)** and remember **`dict` in Python is hashed**, not red–black.
