# [Data Types](https://docs.python.org/3/library/datatypes.html)

Python’s standard library groups **specialized container and value types** under **Data Types**: dates and time zones, ordered and counted mappings, heaps and sorted insertion, compact numeric arrays, weak-reference caches, dynamic type introspection, copy semantics, pretty-printing, enumerations, and graph ordering. Built-in `dict`, `list`, `set`, `tuple`, `str`, and `bytes` live elsewhere; this section adds alternatives and helpers on top of them. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/datatypes.html); this hub orients you to each module and when to reach for it.

Related material outside this section: built-in [`datetime`](../built-in-types/index.md) is not separate — see [`datetime`](datetime-basic-date-and-time-types/index.md) here; numeric stacks may also use [`array`](array-efficient-arrays-of-numeric-values/index.md) or third-party NumPy; text formatting overlaps [`pprint`](pprint-data-pretty-printer/index.md) with [`text-processing-services`](../text-processing-services/index.md).

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`datetime`](datetime-basic-date-and-time-types/index.md) | `date`, `time`, `datetime`, `timedelta`, fixed-offset `timezone` |
| [`zoneinfo`](zoneinfo-iana-time-zone-support/index.md) | IANA time zones (`America/New_York`, `Europe/Berlin`, …) |
| [`calendar`](calendar-general-calendar-related-functions/index.md) | Month/year calendars, weekday math, `cal`-style output |
| [`collections`](collections-container-datatypes/index.md) | `deque`, `Counter`, `defaultdict`, `namedtuple`, `ChainMap`, … |
| [`collections.abc`](collectionsabc-abstract-base-classes-for-containers/index.md) | ABCs for `Mapping`, `Sequence`, `Iterable`, `Buffer`, … |
| [`heapq`](heapq-heap-queue-algorithm/index.md) | Min/max heaps, `nlargest`/`nsmallest`, merge sorted streams |
| [`bisect`](bisect-array-bisection-algorithm/index.md) | Maintain sorted lists; O(log n) insertion-point search |
| [`array`](array-efficient-arrays-of-numeric-values/index.md) | Compact homogeneous numeric arrays (C-interchange friendly) |
| [`weakref`](weakref-weak-references/index.md) | Weak mappings/sets, proxies, `finalize` cleanup hooks |
| [`types`](types-dynamic-type-creation-and-names-for-built-in-types/index.md) | Dynamic class creation, interpreter type names, `SimpleNamespace` |
| [`copy`](copy-shallow-and-deep-copy-operations/index.md) | Shallow/deep copy and `copy.replace()` for dataclasses |
| [`pprint`](pprint-data-pretty-printer/index.md) | Readable multi-line reprs for nested structures |
| [`reprlib`](reprlib-alternate-repr-implementation/index.md) | Size-limited reprs and `@recursive_repr` |
| [`enum`](enum-support-for-enumerations/index.md) | Symbolic constants: `Enum`, `Flag`, `StrEnum`, `IntEnum` |
| [`graphlib`](graphlib-functionality-to-operate-with-graph-like-structures/index.md) | Topological sort for DAG task graphs |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Store an instant with DST rules | [`zoneinfo.ZoneInfo`](zoneinfo-iana-time-zone-support/index.md) on aware [`datetime`](datetime-basic-date-and-time-types/index.md) |
| Fixed UTC offset only (no DST) | `datetime.timezone(timedelta(hours=…))` or `datetime.UTC` |
| Print a month grid or weekday layout | [`calendar`](calendar-general-calendar-related-functions/index.md) |
| Count occurrences or group with defaults | [`collections.Counter`](collections-container-datatypes/index.md) / [`defaultdict`](collections-container-datatypes/index.md) |
| Fast queue with pops at both ends | [`collections.deque`](collections-container-datatypes/index.md) |
| Test “is this a mapping?” in APIs | [`collections.abc.Mapping`](collectionsabc-abstract-base-classes-for-containers/index.md) |
| Priority queue or streaming top-k | [`heapq`](heapq-heap-queue-algorithm/index.md) |
| Keep a list sorted as you insert | [`bisect`](bisect-array-bisection-algorithm/index.md) |
| Millions of floats with low overhead | [`array`](array-efficient-arrays-of-numeric-values/index.md) |
| Cache large objects without pinning them | [`weakref.WeakValueDictionary`](weakref-weak-references/index.md) |
| Clone nested config safely | [`copy.deepcopy`](copy-shallow-and-deep-copy-operations/index.md) |
| Log or debug huge nested dicts | [`pprint`](pprint-data-pretty-printer/index.md) or [`reprlib.repr`](reprlib-alternate-repr-implementation/index.md) |
| Named constants instead of magic strings | [`enum.Enum`](enum-support-for-enumerations/index.md) |
| Order build steps with dependencies | [`graphlib.TopologicalSorter`](graphlib-functionality-to-operate-with-graph-like-structures/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **aware** datetimes for real-world timestamps | Naive values have no unambiguous UTC/local meaning |
| Declare **`tzdata`** on Windows/cross-platform apps using `zoneinfo` | System IANA database may be missing |
| Use **`collections.abc`** for parameter types, concrete types for construction | Keeps APIs flexible without forcing one dict/list impl |
| Reach for **`bisect` + sorted list** before resorting whole lists | Sort is O(n log n); repeated inserts benefit from order maintenance |
| Treat **`copy.copy` vs `deepcopy`** as explicit choices | Shallow copies share nested mutable objects |
| Cap debug output with **`reprlib`** or **`pprint` depth/width** | Prevents huge logs and accidental secret dumps |
| Model fixed sets of options with **`Enum`**, not bare strings | Catches typos and documents allowed values |

```python
# Goal: aware UTC timestamp and safe shallow config copy
import copy
import datetime as dt

created = dt.datetime.now(dt.UTC)
config = {"retries": 3, "tags": ["api", "v2"]}
snapshot = copy.copy(config)
snapshot["tags"].append("staging")
assert config["tags"] == ["api", "v2", "staging"]
assert created.tzinfo is dt.UTC
```

```python
# Goal: count items and schedule tasks in dependency order
from collections import Counter
from graphlib import TopologicalSorter

counts = Counter("abracadabra")
assert counts["a"] == 5

graph = {"compile": {"lint"}, "test": {"compile"}, "deploy": {"test"}}
order = list(TopologicalSorter(graph).static_order())
assert order.index("lint") < order.index("compile") < order.index("deploy")
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Mixing naive and aware datetimes | `TypeError` on comparison/arithmetic | Normalize with `.replace(tzinfo=…)` or `astimezone()` first |
| Assuming `ZoneInfo` keys are user-facing labels | Raw IANA names shown in UI | Map through locale data (CLDR) for display |
| Using `OrderedDict` for ordering on 3.7+ | Unnecessary — plain `dict` preserves insertion order | Use `OrderedDict` only when you need `move_to_end` |
| `deepcopy` on modules, sockets, or open files | Unsupported or surprising results | Copy plain data structures; reopen resources |
| `WeakKeyDictionary` with equal-but-not-identical keys | Silent entry loss on reassignment | Delete old key before inserting alias |
| `bisect` on unsorted lists | Wrong insertion points | Sort once, or verify monotonic order |
| `Enum` members compared to raw integers (plain `Enum`) | False negatives | Use `IntEnum` when numeric interoperability is required |

---

## Sections in this repo

| Module | Notes |
|--------|-------|
| [datetime — Basic date and time types](datetime-basic-date-and-time-types/index.md) | Aware/naive rules, `timedelta`, strftime |
| [zoneinfo — IANA time zone support](zoneinfo-iana-time-zone-support/index.md) | `ZoneInfo`, `TZPATH`, fold/DST |
| [calendar — General calendar-related functions](calendar-general-calendar-related-functions/index.md) | `Calendar`, `monthrange`, HTML/text calendars |
| [collections — Container datatypes](collections-container-datatypes/index.md) | `deque`, `Counter`, `defaultdict`, `ChainMap` |
| [collections.abc — Abstract Base Classes for Containers](collectionsabc-abstract-base-classes-for-containers/index.md) | Protocol-style ABC checks and mixins |
| [heapq — Heap queue algorithm](heapq-heap-queue-algorithm/index.md) | Min/max heap API, `merge`, `nlargest` |
| [bisect — Array bisection algorithm](bisect-array-bisection-algorithm/index.md) | `bisect_left`/`insort`, grade-table pattern |
| [array — Efficient arrays of numeric values](array-efficient-arrays-of-numeric-values/index.md) | Type codes, `tobytes`, buffer protocol |
| [weakref — Weak references](weakref-weak-references/index.md) | Weak maps/sets, `finalize`, proxies |
| [types — Dynamic type creation and names for built-in types](types-dynamic-type-creation-and-names-for-built-in-types/index.md) | `new_class`, `SimpleNamespace`, type objects |
| [copy — Shallow and deep copy operations](copy-shallow-and-deep-copy-operations/index.md) | `copy`, `deepcopy`, `replace` |
| [pprint — Data pretty printer](pprint-data-pretty-printer/index.md) | `pp`, `PrettyPrinter`, depth/width |
| [reprlib — Alternate repr() implementation](reprlib-alternate-repr-implementation/index.md) | Bounded repr, `@recursive_repr` |
| [enum — Support for enumerations](enum-support-for-enumerations/index.md) | `Enum`, `Flag`, `auto`, `unique` |
| [graphlib — Functionality to operate with graph-like structures](graphlib-functionality-to-operate-with-graph-like-structures/index.md) | `TopologicalSorter`, parallel-ready API |
