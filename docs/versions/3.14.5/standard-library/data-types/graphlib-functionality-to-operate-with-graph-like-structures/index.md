# [graphlib — Functionality to operate with graph-like structures](https://docs.python.org/3/library/graphlib.html)

The [`graphlib`](https://docs.python.org/3/library/graphlib.html) module (3.9+) provides **`TopologicalSorter`** for ordering **directed acyclic graphs (DAGs)** — task dependency resolution, build pipelines, and course prerequisites. Nodes and edges use hashable objects; the graph maps each node to an iterable of **predecessors** (nodes that must come first). Parallel-friendly `get_ready` / `done` API and convenience `static_order()` are documented on [docs.python.org](https://docs.python.org/3/library/graphlib.html).

---

## Graph model

| Representation | Meaning |
|----------------|---------|
| `{"C": {"A", "B"}}` | `C` depends on `A` and `B` |
| `add(node, *predecessors)` | Incremental edge insertion |
| Cycles | `CycleError` at `prepare()` (subclass of `ValueError`) |

A complete topological order exists **iff** the graph is acyclic.

```python
# Goal: linearize task dependencies
from graphlib import TopologicalSorter

graph = {"compile": {"lint"}, "test": {"compile"}, "deploy": {"test"}}
order = list(TopologicalSorter(graph).static_order())
assert order.index("lint") < order.index("compile") < order.index("test") < order.index("deploy")
```

---

## Incremental API — [TopologicalSorter](https://docs.python.org/3/library/graphlib.html#graphlib.TopologicalSorter)

| Method | When |
|--------|------|
| `add(node, *predecessors)` | Before `prepare()` |
| `prepare()` | Lock graph; detect cycles |
| `get_ready()` | Tuple of nodes with all preds done |
| `done(*nodes)` | Mark processed; unblock successors |
| `is_active()` / `bool(ts)` | More work remains |
| `static_order()` | Iterator without manual done loop |

Designed for **thread/process pools**: workers take ready nodes, call `done` when finished.

```python
# Goal: manual ready/done loop (parallel-ready pattern)
from graphlib import TopologicalSorter

ts = TopologicalSorter({"D": {"B", "C"}, "C": {"A"}, "B": {"A"}})
ts.prepare()
seen = []
while ts.is_active():
    ready = ts.get_ready()
    seen.extend(ready)
    ts.done(*ready)
assert seen.index("A") < seen.index("B")
assert seen.index("A") < seen.index("C")
assert seen.index("B") < seen.index("D")
```

---

## Ordering notes

| Topic | Detail |
|-------|--------|
| Tie-breaking | Among ready nodes, order follows insertion history |
| Partial cycles | `prepare()` may still yield some nodes before blocking |
| `prepare()` re-call | Allowed before sort starts (3.14+); was error before |
| `CycleError.args[1]` | List showing one cycle ring |

---

## Best practices

| Practice | Why |
|----------|-----|
| Model **predecessors explicitly** | Matches `TopologicalSorter` API |
| Use **`static_order()`** for simple scripts | Less boilerplate |
| Use **`get_ready`/`done`** for parallelism | Built for worker pools |
| Validate graphs **before** scheduling | Catch `CycleError` early |
| Keep nodes **hashable and immutable IDs** | Strings/ints, not lists |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Edges reversed (successor as pred) | Wrong execution order | Draw dependency arrows toward node |
| Calling `add` after `prepare` | `ValueError` | Build graph first |
| `done` without prior `get_ready` | `ValueError` | Only mark returned nodes |
| Assuming deterministic global order | Insertion affects ties | Document tie policy |
| Using on cyclic graphs | `CycleError` | Break cycle or report to user |

---

## See also

- [`functools`](https://docs.python.org/3/library/functools.html) — unrelated sorting; graphlib is dependency order
- [`heapq`](../heapq-heap-queue-algorithm/index.md) — priority within a level, not full DAG sort
