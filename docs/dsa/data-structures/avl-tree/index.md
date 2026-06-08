# AVL tree

A **self-balancing binary search tree** where the **height difference** (balance factor) between left and right subtrees is at most **1** at every node. After each insert or delete, **rotations** restore that invariant so height stays **O(log n)**—guaranteed fast lookup even when scheduler entries arrive **sorted by timestamp** or **task ID**.

| | |
| --- | --- |
| **What it is** | A [BST](../binary-search-tree/index.md) plus balance factors in {−1, 0, +1} and single/double rotations on violation. |
| **Core operations** | Same as BST—`search`, `insert`, `delete`, traversals—with **O(log n)** worst case. |
| **Balance factor** | `height(left) − height(right)`; must be −1, 0, or +1. |
| **When to use** | Teaching strict balancing; guaranteed log height when plain BST would skew. |
| **Trade-off** | More bookkeeping and rotations than [red–black](../red-black-tree/index.md); stricter balance → slightly fewer compares on lookup, more work on write. |

An AVL tree models a **live ordered index** that stays balanced as you ingest `(timestamp, task_id, weight)` in **chronological or alphabetical order**—the case that breaks a plain BST. Use it to understand **rotations** before [red–black trees](../red-black-tree/index.md) (used in many language runtimes). For production Python, you still reach for **`dict`** or **`sortedcontainers`**; AVL is for **learning and interviews**.

This page is your **ready reference**: balance factors, rotations, full Python implementation, practical examples, and complexity per operation. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How an AVL tree fits ordered-map problems

| Use case | AVL view | Why balance matters |
| --- | --- | --- |
| **Scheduler feed** | Insert `(timestamp, weight, task_id)` in time order | Plain BST becomes a chain; AVL stays log |
| **Symbol table by name** | Ordered key; frequent insert/remove | O(log n) guaranteed each update |
| **Live score index** | Inorder = sorted; height log | Predictable latency during bursts |
| **Merge two sorted streams** | Inorder merge of two AVLs | O(n + m) walk if both balanced |

**Use bulk `sorted()`** for static archives. **Use AVL** when you implement **ordered maps** yourself or need to **explain rotations** on a whiteboard.

```mermaid
flowchart TB
 subgraph before["BST skew — sorted timestamp insert"]
 direction TB
 D1["D1"] --> D2["D2"] --> D3["D3"] --> D4["D4"]
 end
 subgraph after["AVL — same keys, rebalanced"]
 D2a["D2"]
 D2a --> D1a["D1"]
 D2a --> D4a["D4"]
 D4a --> D3a["D3"]
 end
 before -->|"rotations"| after
```

Throughout this page, **n** = nodes, **h** = O(log n) guaranteed.

---

## AVL vs BST vs red–black vs Python

| | **AVL** | [BST](../binary-search-tree/index.md) | [Red–black](../red-black-tree/index.md) | **`dict`** |
| --- | --- | --- | --- | --- |
| **Search** | O(log n) | O(h) | O(log n) | O(1) avg |
| **Insert/delete** | O(log n), more rotations | O(h) | O(log n), fewer rotations | O(1) avg |
| **Balance** | Stricter (BF ∈ {−1,0,1}) | None | Relaxed via color rules | N/A |
| **Lookup-heavy** | Slightly favored | Skew risk | Industry default for maps | Hash, unordered |
| **Teaching fit** | Rotation drills | Baseline invariant | "Why not RB in Python dict" | `id` lookup |

!!! note "Python `dict` uses hashing, not AVL"
 CPython **`dict`** is a **hash table** (open addressing with perturbation). It does **not** keep keys in sorted order by comparison. For sorted maps in Python ecosystems, see **`sortedcontainers`**, **`bisect`** on a list, or databases with indexes.

---

## Node definition

Store **key**, **height** (or balance factor), **left**, **right**.

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator


@dataclass(frozen=True, order=True)
class ScheduleEntry:
 timestamp: int
 task_id: str
 weight: float = 0.0


@dataclass
class AVLNode:
 key: Any
 height: int = 1
 left: AVLNode | None = None
 right: AVLNode | None = None
```

| | |
| --- | --- |
| **Time** | O(1) per node |
| **Space** | O(1) per node (+ height int) |

---

## Rotations (the core mechanic)

### Right rotation (fix left-heavy)

When left subtree is too tall (**LL** or **LR** case after rebalance at child).

```mermaid
flowchart LR
 subgraph before["Left-heavy"]
 Y["y"]
 X["x"]
 T["T"]
 Y --> X
 Y --> Z["z"]
 X --> T
 end
 subgraph after["After right_rotate(y)"]
 X2["x"]
 Y2["y"]
 T2["T"]
 X2 --> T2
 X2 --> Y2
 Y2 --> Z2["z"]
 end
 before --> after
```

```python
def _height(node: AVLNode | None) -> int:
 return 0 if node is None else node.height


def _update_height(node: AVLNode) -> None:
 node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node: AVLNode) -> int:
 return _height(node.left) - _height(node.right)


def _right_rotate(y: AVLNode) -> AVLNode:
 x = y.left
 assert x is not None
 t2 = x.right
 x.right = y
 y.left = t2
 _update_height(y)
 _update_height(x)
 return x


def _left_rotate(x: AVLNode) -> AVLNode:
 y = x.right
 assert y is not None
 t2 = y.left
 y.left = x
 x.right = t2
 _update_height(x)
 _update_height(y)
 return y
```

| | |
| --- | --- |
| **Time** | O(1) per rotation |
| **Space** | O(1) |

### Rebalance after insert/delete

Four cases from balance factor at node **z**:

| Case | Shape | Fix |
| --- | --- | --- |
| **LL** | BF(z) = +2, BF(left) ≥ 0 | Right rotate z |
| **LR** | BF(z) = +2, BF(left) < 0 | Left rotate left child, then right rotate z |
| **RR** | BF(z) = −2, BF(right) ≤ 0 | Left rotate z |
| **RL** | BF(z) = −2, BF(right) > 0 | Right rotate right child, then left rotate z |

```mermaid
flowchart TD
 I([insert/delete changed heights]) --> U[update height up the path]
 U --> C{abs BF > 1?}
 C -->|no| Done([done])
 C -->|yes| LL{LL / LR / RR / RL}
 LL --> R[apply 1–2 rotations]
 R --> Done
```

```python
def _rebalance(node: AVLNode) -> AVLNode:
 _update_height(node)
 bf = _balance_factor(node)
 if bf > 1:
 assert node.left is not None
 if _balance_factor(node.left) < 0:
 node.left = _left_rotate(node.left)
 return _right_rotate(node)
 if bf < -1:
 assert node.right is not None
 if _balance_factor(node.right) > 0:
 node.right = _right_rotate(node.right)
 return _left_rotate(node)
 return node
```

| | |
| --- | --- |
| **Time** | O(1) at each level; O(log n) along path |
| **Space** | O(1) |

---

## Ways to create an AVL tree

### 1. Empty tree

```python
class AVLTree:
 def __init__(self) -> None:
 self.root: AVLNode | None = None
 self._size = 0

tree = AVLTree()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Insert sorted timestamps — stays O(log n) per insert

Unlike plain BST, inserting timestamps 1…365 in order keeps height logarithmic.

```python
tree = AVLTree()
for t in range(1, 366):
 tree.insert(ScheduleEntry(t, f"task{t}", t * 0.01))
assert tree.height() <= 10
```

| | |
| --- | --- |
| **Time** | O(n log n) total |
| **Space** | O(n) |

---

## Full implementation: `AVLTree`

```python
class AVLTree:
 def __init__(self) -> None:
 self.root: AVLNode | None = None
 self._size = 0

 def __len__(self) -> int:
 return self._size

 def is_empty(self) -> bool:
 return self.root is None

 def height(self) -> int:
 return _height(self.root)

 def search(self, key: Any) -> AVLNode | None:
 cur = self.root
 while cur is not None:
 if key == cur.key:
 return cur
 cur = cur.left if key < cur.key else cur.right
 return None

 def contains(self, key: Any) -> bool:
 return self.search(key) is not None

 def insert(self, key: Any) -> None:
 self.insert_strict(key)

 def insert_strict(self, key: Any) -> bool:
 before = self._size
 self.root = self._insert_rec_strict(self.root, key)
 return self._size > before

 def _insert_rec_strict(self, node: AVLNode | None, key: Any) -> AVLNode:
 if node is None:
 self._size += 1
 return AVLNode(key)
 if key < node.key:
 node.left = self._insert_rec_strict(node.left, key)
 elif key > node.key:
 node.right = self._insert_rec_strict(node.right, key)
 return _rebalance(node)

 def delete(self, key: Any) -> bool:
 self.root, deleted = self._delete_rec(self.root, key)
 if deleted:
 self._size -= 1
 return deleted

 def _delete_rec(
 self, node: AVLNode | None, key: Any
 ) -> tuple[AVLNode | None, bool]:
 if node is None:
 return None, False
 if key < node.key:
 node.left, deleted = self._delete_rec(node.left, key)
 elif key > node.key:
 node.right, deleted = self._delete_rec(node.right, key)
 else:
 if node.left is None:
 return node.right, True
 if node.right is None:
 return node.left, True
 succ = self._min_node(node.right)
 node.key = succ.key
 node.right, _ = self._delete_rec(node.right, succ.key)
 deleted = True
 if node is None:
 return None, deleted
 return _rebalance(node), deleted

 def _min_node(self, node: AVLNode) -> AVLNode:
 while node.left is not None:
 node = node.left
 return node

 def inorder(self) -> list[Any]:
 out: list[Any] = []
 self._inorder_rec(self.root, out)
 return out

 def _inorder_rec(self, node: AVLNode | None, out: list[Any]) -> None:
 if node is None:
 return
 self._inorder_rec(node.left, out)
 out.append(node.key)
 self._inorder_rec(node.right, out)

 def inorder_iter(self) -> Iterator[Any]:
 stack: list[AVLNode] = []
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
| **Insert/delete path** | O(log n) |
| **Space** | O(n) tree + O(log n) stack |

---

## Operations with ordered-map examples

### Insert scheduler entries in sorted order

```python
tree = AVLTree()
for ts in range(1, 366):
 tree.insert_strict(ScheduleEntry(ts, "task01", ts * 0.025))
assert len(tree) == 365
assert tree.height() <= 10
ordered_ts = [k.timestamp for k in tree.inorder()]
assert ordered_ts == list(range(1, 366))
```

| | |
| --- | --- |
| **Time** | O(log n) per insert |
| **Space** | O(1) aux per level |

```mermaid
sequenceDiagram
 participant Feed as event stream
 participant AVL as AVLTree
 Feed->>AVL: insert T1..T365 in order
 loop each insert
 AVL->>AVL: descend O(log n)
 AVL->>AVL: rebalance with 0–1 rotations
 end
 AVL-->>Feed: height O(log n) not 365
```

---

### Search / delete — remove cancelled task from scheduler

```python
tree = AVLTree()
for t in [3, 1, 4, 2, 5]:
 tree.insert_strict(ScheduleEntry(t, "task07", t * 0.4))

assert tree.contains(ScheduleEntry(4, "task07"))
tree.delete(ScheduleEntry(4, "task07"))
assert not tree.contains(ScheduleEntry(4, "task07"))
assert [k.timestamp for k in tree.inorder()] == [1, 2, 3, 5]
```

| | |
| --- | --- |
| **Time** | O(log n) |
| **Space** | O(log n) recursion |

---

### Inorder — chronological scheduler report

Same as BST: **inorder** yields sorted keys.

```python
tree = AVLTree()
stats = [ScheduleEntry(150, "A", 0.9), ScheduleEntry(60, "B", 1.1), ScheduleEntry(240, "C", 0.7)]
for s in stats:
 tree.insert_strict(s)
for s in tree.inorder_iter():
 print(f"t={s.timestamp}: weight {s.weight:.1f}")
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(h) = O(log n) stack |

---

## Application: balanced task scheduler index

```python
class TaskScheduleIndex:
 def __init__(self) -> None:
 self._tree = AVLTree()

 def schedule(self, timestamp: int, task_id: str, weight: float) -> None:
 self._tree.insert_strict(ScheduleEntry(timestamp, task_id, weight))

 def tasks_for_id(self, task_id: str) -> list[ScheduleEntry]:
 return [k for k in self._tree.inorder() if k.task_id == task_id]

 def report_through(self, max_ts: int) -> list[ScheduleEntry]:
 return [k for k in self._tree.inorder() if k.timestamp <= max_ts]


idx = TaskScheduleIndex()
for t in range(1, 11):
 idx.schedule(t, "task10", t * 0.08)
through = idx.report_through(5)
assert len(through) == 5
assert idx._tree.height() <= 5
```

| Operation | Time | Space |
| --- | --- | --- |
| `schedule` | O(log n) | O(1) |
| `report_through` | O(n) scan | O(output) |

---

## AVL vs red–black (when teaching)

| | **AVL** | **Red–black** |
| --- | --- | --- |
| Balance | Stricter | Looser |
| Rotations on insert | Often more | Often fewer |
| Lookup | Fewer compares (shorter) | Slightly more |
| Typical use | Databases (some), teaching | `std::map`, Java `TreeMap` |
| Ordered-map analogy | Strict scheduler with fairness guarantees | High-volume symbol-table index |

---

## Master complexity table

| Operation | Time | Space (aux) | Notes |
| --- | --- | --- | --- |
| Create empty | O(1) | O(1) | |
| Search | O(log n) | O(1) | |
| Insert | O(log n) | O(log n) stack | ≤ 2 rotations |
| Delete | O(log n) | O(log n) stack | |
| Inorder | O(n) | O(log n) | |
| Height query | O(1) cached at root | O(1) | |
| Rotations | O(1) each | O(1) | |
| Storage | — | O(n) | |

---

## When to pick which structure

```mermaid
flowchart TD
 Q([Need sorted map?])
 Q --> G{Guaranteed worst-case log?}
 G -->|yes| W{Write-heavy?}
 W -->|no lookup-heavy| AVL["AVL tree"]
 W -->|yes| RB["Red–black tree"]
 G -->|no| BST["BST if random input"]
 Q --> H{Python production?}
 H -->|yes| D["dict / DB / sortedcontainers"]
```

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Forgetting `_update_height` before BF | Wrong rotation case | Update bottom-up after child change |
| Wrong rotation order in LR/RL | Still unbalanced | Rotate **child** first, then **parent** |
| Using height 0 vs −1 for empty | Off-by-one BF | Be consistent with `_height(None)` |
| Duplicate key policy unclear | Silent skip vs overwrite | Document `insert_strict` |
| Expecting AVL in `dict` | Wrong mental model | Hash table; see [hash table](../hash-table/index.md) |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Binary search tree](../binary-search-tree/index.md) | Base invariant without balance |
| [Red–black tree](../red-black-tree/index.md) | Looser balance; library maps |
| [2-3-4 tree](../2-3-4-tree/index.md) | B-tree family; LLRB isomorphism |
| [Complexity analysis](../../complexity/index.md) | Big-O |
| [Data structures hub](../index.md) | Index |

---

## Quick reference card

```python
tree = AVLTree()
tree.insert_strict(ScheduleEntry(150, "task01", 2.8))
tree.search(ScheduleEntry(150, "task01"))
tree.delete(ScheduleEntry(150, "task01"))
list(tree.inorder_iter())
tree.height()
```

An **AVL tree** is a **BST with strict height balance**—master **rotations** here, then compare with **[red–black](../red-black-tree/index.md)** for the trade-offs real map implementations make.
