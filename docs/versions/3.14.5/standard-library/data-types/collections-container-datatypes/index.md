# [collections — Container datatypes](https://docs.python.org/3/library/collections.html)

The [`collections`](https://docs.python.org/3/library/collections.html) module implements **specialized containers** that extend or replace built-in `dict`, `list`, and `tuple` patterns: double-ended queues, counted mappings, default factories, ordered views (legacy), named tuples, layered dicts, and wrapper bases for subclassing. Full recipes (ChainMap CLI/env layering, Counter statistics) are on [docs.python.org](https://docs.python.org/3/library/collections.html). For protocol typing see [`collections.abc`](../collectionsabc-abstract-base-classes-for-containers/index.md).

---

## Factory and class overview

| Name | Kind | Primary use |
|------|------|-------------|
| `namedtuple(typename, fields)` | factory | Lightweight immutable records with named fields |
| `deque` | class | O(1) append/pop at both ends |
| `Counter` | dict subclass | Count hashable items; multiset math |
| `defaultdict` | dict subclass | Auto-vivify missing keys via factory |
| `OrderedDict` | dict subclass | Ordered dict + `move_to_end` (rarely needed on 3.7+) |
| `ChainMap` | class | Search stacked mappings without copying |
| `UserDict` / `UserList` / `UserString` | wrappers | Easier subclassing of built-ins |

---

## deque — [deque objects](https://docs.python.org/3/library/collections.html#deque-objects)

| Operation | Complexity | Notes |
|-----------|------------|-------|
| `append` / `appendleft` | O(1) | Queue and stack at both ends |
| `pop` / `popleft` | O(1) | |
| `maxlen` | optional | Drops opposite end when full — bounded buffers |
| `rotate(n)` | O(k) | Circular shift for round-robin |

```python
# Goal: bounded FIFO with automatic eviction
from collections import deque

log = deque(maxlen=3)
for line in ("a", "b", "c", "d"):
    log.append(line)
assert list(log) == ["b", "c", "d"]
```

---

## Counter and defaultdict

| Type | Pattern |
|------|---------|
| `Counter` | `elements()`, `most_common(n)`, in-place `+=`/`-=` between counters |
| `defaultdict(list)` | `d[key].append(x)` without `KeyError` |
| `defaultdict(int)` | Numeric aggregation defaulting to 0 |

```python
# Goal: count tokens and group by first letter
from collections import Counter, defaultdict

words = ["apple", "apricot", "banana", "apple"]
counts = Counter(words)
assert counts.most_common(1)[0] == ("apple", 2)

by_initial = defaultdict(list)
for w in words:
    by_initial[w[0]].append(w)
assert "a" in by_initial and len(by_initial["b"]) == 1
```

---

## ChainMap — [ChainMap objects](https://docs.python.org/3/library/collections.html#chainmap-objects)

| Method / attr | Behavior |
|---------------|----------|
| Lookup | First mapping in `maps` with key wins |
| Write / delete | Only top mapping (`maps[0]`) |
| `new_child(m=None)` | Push context for nested scopes |
| `parents` | View skipping top mapping |

```python
# Goal: defaults overridden by explicit overrides dict
from collections import ChainMap

defaults = {"color": "red", "timeout": 30}
overrides = {"color": "blue"}
cfg = ChainMap(overrides, defaults)
assert cfg["color"] == "blue"
assert cfg["timeout"] == 30
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use plain **`dict`** unless you need a specialty | Simpler and faster for most cases |
| Pick **`deque`** over `list` for queue workloads | `list.pop(0)` is O(n) |
| Use **`Counter`** for frequency, not manual increments | Built-in multiset operations |
| Prefer **`typing.NamedTuple` or dataclasses** over `namedtuple` for new code | Better tooling; `namedtuple` still fine for quick tuples |
| **`ChainMap`** for scoped overrides, not long-lived merges | Writes only hit the top dict |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `Counter` negative counts | Allowed — not a multiset | Use `+ Counter` to drop non-positive |
| `defaultdict` factory holds mutable state | Shared default objects | Use `lambda: []` not `defaultdict(list)` with prebuilt list |
| `OrderedDict` for ordering only | Redundant on modern Python | Plain dict preserves insertion order |
| `namedtuple` field names as keywords | Syntax errors (`class`, `def`) | Use `_replace` and valid identifiers |
| Mutating `ChainMap.maps` unexpectedly | Changes live view | Copy when snapshot needed |

---

## See also

- [`collections.abc`](../collectionsabc-abstract-base-classes-for-containers/index.md) — ABC protocols
- [`heapq`](../heapq-heap-queue-algorithm/index.md) — priority queues (different shape than deque)
