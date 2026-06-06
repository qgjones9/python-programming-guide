# Sets

An abstract collection of **unique** elements where **membership**, **insert**, and **remove** dominate the API. **Unordered** sets usually sit on **hash tables**; **ordered** sets sit on **balanced BSTs** (red–black in many languages). Python's built-in `set` and `frozenset` are hash-based and unordered.

| | |
| --- | --- |
| **What it is** | No duplicate members; typical ops: `add`, `discard`, `in`, and set algebra (`|`, `&`, `-`, `^`). |
| **Core operations** | Average O(1) hash set ops; O(log n) tree set ops; algebra on two sets of size n, m is O(n + m) with hashing. |
| **When to use** | Deduplication, fast membership, climate-zone pools, station tags, and combining station groups. |
| **Trade-off** | Hash sets sacrifice sorted iteration; tree sets cost more per op but give order. |

In **daily weather data analysis**, sets model **climate regions**, **active station lists**, **condition tags**, and **"which stations reported rain in both months"** style questions without duplicate rows. You will still join large tables in **pandas**—sets excel for **small-to-medium unique collections** and **algebra** on station ids.

This page is your **ready reference**: ADT semantics, hash vs tree implementations, full Python patterns, every operation with weather-flavored examples, and **time and space complexity**. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## How sets fit weather-shaped problems

| Weather idea | Set view | Typical op |
| --- | --- | --- |
| **Pacific Northwest stations** | 4 station ids | `membership`, iterate |
| **Stations with rain in Jan and Feb** | Intersection of two condition sets | `&` |
| **All coastal minus offline** | Difference | `-` |
| **Home or remote sensors** | Union of two sensor sets | `\|` |
| **Unique station ids in file** | Dedup from list | `set(list)` |
| **Frozen region snapshot** | Immutable set | `frozenset` |

```mermaid
flowchart LR
  subgraph ops["Set algebra on station ids"]
    A["Pacific_NW"]
    B["High_Anomaly_2024"]
    A --> I["A & B — in both"]
    A --> U["A | B — either"]
    A --> D["A - B — NW not high anomaly"]
  end
```

Throughout this page, **n** = \|set A\|, **m** = \|set B\|, **u** = universe size for bitset discussion.

---

## Set vs multiset vs dict vs list

| | **Set** | Multiset (bag) | `dict` | `list` |
| --- | --- | --- | --- | --- |
| **Duplicates** | No | Counted | Keys unique | Yes |
| **`in`** | O(1) avg hash | O(1) with Counter | O(1) avg | O(n) |
| **Order** | Unordered (Py 3.7+ insertion order incidental) | Varies | Insertion order 3.7+ | Index order |
| **Algebra** | Built-in | `Counter` arithmetic | Key sets only | Manual |
| **Weather fit** | Regions, tags | Reading counts per station | Stats per id | Reading sequence |

---

## ADT operations (abstract)

| Operation | Meaning | Weather example |
| --- | --- | --- |
| `insert(x)` | Add if absent | Add station to region |
| `remove(x)` | Delete if present | Remove decommissioned station id |
| `contains(x)` | Membership test | Is `station_id` in high-anomaly set? |
| `size()` | Count distinct | Active station count (unique ids) |
| `union(A,B)` | All in either | Coastal \| mountain sensors |
| `intersection(A,B)` | In both | Rain days ∩ cold-front days |
| `difference(A,B)` | In A not B | Active minus offline |
| `symmetric_difference` | In exactly one | XOR of two month lists |

```mermaid
flowchart TB
  subgraph venn["Intersection & union"]
    direction TB
    U["Union A ∪ B"]
    I["Intersection A ∩ B"]
  end
```

---

## Ways to create a set (Python)

### 1. Empty set — **not** `{}` (that is a dict)

```python
pacific_nw: set[str] = set()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 2. Literal with members

```python
pacific_nw = {"SEA-01", "PDX-01", "EUG-01", "BOI-01"}
```

| | |
| --- | --- |
| **Time** | O(k) for k members (hash each) |
| **Space** | O(k) |

### 3. From iterable — dedup reading ids

```python
rainy_days = set(row["reading_id"] for row in january_rain_rows)
```

| | |
| --- | --- |
| **Time** | O(n) average for n inputs |
| **Space** | O(unique) |

### 4. Set comprehension

```python
coastal = {s["station_id"] for s in stations if s["zone"] in {"coastal", "maritime"}}
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(output) |

### 5. `frozenset` — immutable region snapshot

```python
region_2024 = frozenset(["SEA-01", "PDX-01", "EUG-01", "BOI-01"])
rules_cache[region_2024] = calibration_policy
```

| | |
| --- | --- |
| **Time** | O(k) build |
| **Space** | O(k) |

### 6. From pandas column

```python
import pandas as pd

stations = set(df["station_id"].dropna().unique())
```

| | |
| --- | --- |
| **Time** | O(n) scan |
| **Space** | O(unique stations) |

---

## Hash-table set (how Python `set` behaves)

Conceptual buckets: `hash(x) % table_size` → chain or open addressing (CPython uses open addressing with perturbation).

```python
def demo_membership() -> None:
    high_anomaly = {"SEA-01", "DEN-01", "PHX-01", "MIA-01"}
    assert "SEA-01" in high_anomaly
    high_anomaly.add("ORD-01")
    high_anomaly.discard("DEN-01")
```

| Operation | Average time | Worst time | Notes |
| --- | --- | --- | --- |
| `in` / `add` / `discard` | O(1) | O(n) | Rare bad hashes |
| `len` | O(1) | O(1) | |
| Iterate | O(n) | O(n) | |
| `union` (update many) | O(n + m) | O(n + m) | |

**Space:** Θ(n) for n members (overhead factor ~2–3 in CPython).

---

## Tree-based ordered set (concept + sketch)

Used in C++ `std::set`, Java `TreeSet`—not Python stdlib. **Red–black** or similar keeps keys sorted.

```python
class OrderedSet:
    def __init__(self) -> None:
        self.root = None

    def insert(self, key: str) -> None: ...
    def contains(self, key: str) -> bool: ...
    def inorder(self) -> list[str]: ...
```

| Operation | Time | Space |
| --- | --- | --- |
| `insert` / `contains` / `remove` | O(log n) | O(1) |
| In-order iterate | O(n) | O(n) output |

**Weather use:** walk stations in alphabetical order for printed reports without sorting each time.

---

## Set algebra (full reference)

```python
pacific = {"SEA-01", "PDX-01", "EUG-01", "BOI-01"}
high_anomaly = {"SEA-01", "DEN-01", "PHX-01", "MIA-01"}

both = pacific & high_anomaly
either = pacific | high_anomaly
nw_only = pacific - high_anomaly
symmetric = pacific ^ high_anomaly

pacific |= {"BOI-01"}
pacific &= high_anomaly
```

```mermaid
flowchart LR
  A["Set A<br/>January rain days"]
  B["Set B<br/>February rain days"]
  A --> I["A & B — rain both months"]
  A --> D["A - B — only January"]
  B --> D2["B - A — only February"]
  A --> X["A ^ B — exactly one month"]
```

| Operation | Operator / method | Time (hash) | Space |
| --- | --- | --- | --- |
| Union | `\|`, `.union()` | O(n + m) | O(n + m) result |
| Intersection | `&`, `.intersection()` | O(min(n,m)) typical | O(output) |
| Difference | `-`, `.difference()` | O(n) | O(output) |
| Symmetric diff | `^`, `.symmetric_difference()` | O(n + m) | O(output) |
| Subset test | `<=`, `.issubset()` | O(n) | O(1) |
| Disjoint | `.isdisjoint()` | O(min(n,m)) avg | O(1) |

---

## All operations (weather examples + complexity)

### `add(x)` — tag station as flagged

```python
flagged.add("SEA-01")
```

| **Time** | O(1) average |
| **Space** | O(1) |

### `discard(x)` / `remove(x)`

```python
flagged.discard("DEN-99")
flagged.remove("SEA-01")
```

| **Time** | O(1) average |
| **Space** | O(1) |

### `in` — is station in region?

```python
if "SEA-01" in pacific_nw:
    apply_coastal_calibration()
```

| **Time** | O(1) average |
| **Space** | O(1) |

### Copy and freeze

```python
live = {"SEA-01", "DEN-01"}
snapshot = live.copy()
frozen = frozenset(live)
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) new structure |

### Pop arbitrary element

```python
station = flagged.pop()
```

| **Time** | O(1) average |

---

## Weather application: climate region pools

```python
PACIFIC_NW = frozenset({"SEA-01", "PDX-01", "EUG-01", "BOI-01"})
SOUTHWEST = frozenset({"PHX-01", "LAS-01", "ABQ-01", "ELP-01"})
WEST = PACIFIC_NW | SOUTHWEST

def same_region(s1: str, s2: str) -> bool:
    for region in (PACIFIC_NW, SOUTHWEST):
        if s1 in region and s2 in region:
            return True
    return False
```

| | |
| --- | --- |
| **Time** | O(1) membership per region check with small frozensets |
| **Space** | O(stations in archive) |

---

## Weather application: two-month rain overlap

```python
def reading_ids_with_rain(rows: list[dict]) -> set[int]:
    return {r["reading_id"] for r in rows if r["summary"] == "rain"}

jan = reading_ids_with_rain(january_readings)
feb = reading_ids_with_rain(february_readings)
repeat = jan & feb
only_jan = jan - feb
```

| | |
| --- | --- |
| **Time** | O(n_jan + n_feb) build + O(min) intersect |
| **Space** | O(unique readings) |

---

## Weather application: condition filter set

```python
WINDY = frozenset({"windy", "gusty", "storm"})
windy_stations = {
    s["station_id"]
    for s in stations
    if s["dominant_condition"] in WINDY
}
```

---

## Bitset set (honorable implementation note)

When universe is **small and fixed** (32 climate zones, 64 station index), bit vectors give O(1) word-sized ops.

```python
def bitset_from_ids(ids: list[int], universe: int = 32) -> int:
    mask = 0
    for i in ids:
        mask |= 1 << i
    return mask

def in_bitset(mask: int, i: int) -> bool:
    return (mask >> i) & 1 == 1

def union_masks(a: int, b: int) -> int:
    return a | b
```

| Operation | Time | Space |
| --- | --- | --- |
| Union/intersect on fixed universe | O(1) word ops | O(1) |

---

## Python stdlib: `set` and `frozenset`

| Type | Mutable | Hashable | Use |
| --- | --- | --- | --- |
| `set` | Yes | No | Live station tags, monthly builds |
| `frozenset` | No | Yes | Region constants, dict keys |

```python
import networkx as nx

G = nx.Graph()
G.add_edge("SEA-01", "DEN-01")
```

**networkx** models **graphs** ([graphs](../graphs/index.md)), not replacement for `set`—listed when you cross station **networks** with set **nodes**.

---

## Master complexity table

| Operation | Hash set (avg) | Hash set (worst) | Tree set |
| --- | --- | --- | --- |
| `add` / `discard` / `in` | O(1) | O(n) | O(log n) |
| `len` | O(1) | O(1) | O(1) |
| Iterate all | O(n) | O(n) | O(n) |
| Union / update | O(n + m) | O(n + m) | O(n log m) merge walk |
| Intersection | O(min(n,m)) | O(n + m) | O(n log m) |
| Build from list len n | O(n) | O(n²) worst | O(n log n) |

**Space:** Θ(n) stored elements plus hash table overhead.

---

## When to pick which structure (weather context)

```mermaid
flowchart TD
  Q([Unique ids?])
  Q --> N{Need sorted walk?}
  N -->|no| HS["set / frozenset"]
  N -->|yes| TS["tree set / sorted keys"]
  Q --> L{Huge table column?}
  L -->|yes| PD["pandas.unique / categorical"]
```

| Scenario | Best tool |
| --- | --- |
| 4-station region membership | `frozenset` |
| 50k reading dedup ids | `set` or pandas |
| Ordered station report | `sorted(set)` once or tree set |
| Fixed 32-zone universe bitwise | bitset |

---

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| `s = {}` for empty set | Creates dict | `s = set()` |
| Lists in set | Unhashable TypeError | Use ids/tuples |
| Relying on set order for logic | Order not semantic in theory | Sort for display |
| O(n²) `in` in loop over list | Slow station scans | Build `set` once |
| Mutating set while iterating | RuntimeError | Iterate on `list(s)` copy |

---

## Related pages

| Page | Relationship |
| --- | --- |
| [Hash table](../hash-table/index.md) | Implementation behind `set` |
| [Red–black tree](../red-black-tree/index.md) | Ordered set backend |
| [Treaps](../treaps/index.md) | Alternative ordered set |
| [Graphs](../graphs/index.md) | Edges, not just vertices |
| [Complexity analysis](../../complexity/index.md) | Big-O reference |

---

## Quick reference card

```python
stations = set()
stations = {"SEA-01", "DEN-01"}
region = frozenset(["SEA-01", "PDX-01", "EUG-01", "BOI-01"])
from_list = set(station_ids)

"x" in stations
stations.add("ORD-01")
stations.discard("DEN-01")

a | b; a & b; a - b; a ^ b
a |= b; a <= b; a.isdisjoint(b)

stations.copy()
frozenset(stations)
```

Use **`set`** for **fast unique membership and algebra** on weather station ids—use **pandas** for **column-wide** archive tables.
