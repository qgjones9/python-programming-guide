# Hash table

A **key → value** map implemented by hashing keys into **bucket indices**, with a **collision policy** when two keys land in the same slot. Average-case lookup, insert, and delete are **O(1)**; Python’s `dict` and `set` are highly optimized hash tables in C.

| | |
| --- | --- |
| **What it is** | `hash(key) % buckets` picks a slot; collisions resolved by open addressing or chaining (CPython dict uses open addressing). |
| **Core operations** | `get`, `set`, `delete`, membership; iteration over keys (insertion-ordered in dict 3.7+). |
| **When to use** | Play lookups by `play_id`, player rosters, counting stats, caches, deduplication, grouping. |
| **Trade-off** | Keys must be hashable; worst-case O(n) if all keys collide; no cheap “sorted by key” without extra structure. |

In **NFL data analysis**, hash tables are the **default index layer**: map **`play_id` → row dict**, **`player_id` → name**, team abbreviations, weekly **`Counter`** of formations, and **`defaultdict`** aggregations. You rarely implement a hash table from scratch in production—you **use `dict` / `set` / `Counter` / `defaultdict`** and understand collisions, load factor, and hashability so debug sessions make sense.

This page is your **ready reference**: Python built-ins, a teaching implementation, collision concepts, every common operation with NFL examples, and **time and space complexity**. For Big-O notation, see [Complexity analysis](../../complexity/index.md).

[Parent: Data structures](../index.md)

---

## Hash table vs list vs tree

| | **`dict` / `set`** | **`list` scan** | **BST / `sorted`** |
| --- | --- | --- | --- |
| **Find by key** | O(1) average | O(n) | O(log n) |
| **Insert** | O(1) average | O(1) append; find O(n) | O(log n) |
| **Ordered by key** | Insertion order only (dict) | Index order | Sorted order |
| **NFL** | `plays[play_id]` | scan all plays | season leaders tree |

```mermaid
flowchart LR
  K["key: play_id 4021"] --> H["hash()"]
  H --> I["index in bucket array"]
  I --> V["value: Play row"]
```

Throughout this page, **n** is the number of entries; **m** is bucket count (implementation detail in CPython).

---

## NFL data analysis: what a hash table models

| NFL idea | Map type | Example key |
| --- | --- | --- |
| **Play by id** | `dict[int, Play]` | `play_id` |
| **Player name by gsis_id** | `dict[str, str]` | `00-0031234` |
| **Team colors / meta** | `dict[str, dict]` | `"KC"` |
| **Unique players seen** | `set[str]` | `player_id` |
| **Count snaps by formation** | `Counter[str]` | `"11"` personnel |
| **EPA sum per receiver** | `defaultdict(float)` | `player_id` |

```python
from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Play:
    play_id: int
    game_id: str
    posteam: str
    epa: float
    passer_id: str | None


@dataclass(frozen=True)
class Player:
    player_id: str
    name: str
    position: str
```

---

## Mental model: hash, bucket, collision

1. **`hash(key)`** → integer (must be stable for lifetime of key in table).
2. **Bucket index** = `hash % m` (conceptually).
3. **Collision** — two keys want the same bucket; probe other slots or chain a list.

```mermaid
sequenceDiagram
  participant Code
  participant Dict as dict
  Code->>Dict: d[play_id] = play
  Dict->>Dict: hash(play_id)
  Dict->>Dict: find slot / probe
  Dict-->>Code: stored
  Code->>Dict: d[play_id]
  Dict-->>Code: play O(1) avg
```

| Concept | Meaning | NFL impact |
| --- | --- | --- |
| **Hashable key** | Immutable or defines `__hash__` | Use `int`, `str`, `tuple` of immutables |
| **Load factor** | n/m; resize when too full | CPython resizes dict automatically |
| **Collision** | Same bucket | Still O(1) average with good hash |

---

## Ways to create a hash table in Python

### 1. Empty `dict`

```python
plays_by_id: dict[int, Play] = {}
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) empty overhead |

### 2. Dict literal / comprehension

```python
team_abbr = {"KC": "Chiefs", "BUF": "Bills", "SF": "49ers"}

plays = {
    p.play_id: p
    for p in load_plays_from_csv("week1.csv")
}
```

| | |
| --- | --- |
| **Time** | O(n) for n plays |
| **Space** | O(n) |

### 3. `dict()` constructor

```python
d = dict([("KC", 3), ("BUF", 2)])
d2 = dict(zip(team_ids, team_names))
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) |

### 4. Empty `set`

```python
seen_players: set[str] = set()
```

| | |
| --- | --- |
| **Time** | O(1) |
| **Space** | O(1) |

### 5. `defaultdict` — missing keys get default

```python
epa_by_receiver: defaultdict[float] = defaultdict(float)
epa_by_receiver["00-0031234"] += 1.2
```

| | |
| --- | --- |
| **Time** | O(1) average per update |
| **Space** | O(keys) |

### 6. `Counter` — multiset counts

```python
formation_counts = Counter(["11", "11", "12", "21", "11"])
assert formation_counts["11"] == 3
```

| | |
| --- | --- |
| **Time** | O(k) build for k labels |
| **Space** | O(unique) |

### 7. Build index from list of rows (manual)

```python
def index_plays(rows: list[dict]) -> dict[int, dict]:
    return {row["play_id"]: row for row in rows}
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(n) |

### 8. Teaching: `SeparateChainingHashTable`

See [Reference implementation](#reference-implementation-separatechaininghashtable) below.

```mermaid
flowchart TD
  Q([Need counts?])
  Q -->|yes| C["Counter"]
  Q -->|no| D{Default on miss?}
  D -->|yes| DD["defaultdict"]
  D -->|no| DI["dict / set"]
```

---

## Hashability rules (Python)

| Hashable | Not hashable (default) |
| --- | --- |
| `int`, `float`, `str`, `bytes` | `list`, `dict`, `set` |
| `tuple` of hashables | mutable custom objects unless `__hash__` defined |
| `frozenset` | `bytearray` |

**NFL:** Use `play_id: int` or `(game_id, play_id)` tuple as key—not a mutable row `dict` as key.

```python
# Bad
# row = {"play_id": 1}
# keys[row] = ...  # TypeError: unhashable type: 'dict'

# Good
key = (row["game_id"], row["play_id"])
index[key] = row
```

---

## Collisions (conceptual)

**Separate chaining:** each bucket is a list of `(key, value)` pairs.

**Open addressing:** on collision, probe `i+1`, `i+2`, … (CPython dict uses a variant).

```python
# Toy: two keys might share bucket in tiny table — still works via probing/chain
def toy_hash(key: str, m: int) -> int:
    return sum(ord(c) for c in key) % m
```

| Case | Time |
| --- | --- |
| Average insert/lookup | O(1) |
| Worst all collide | O(n) |

You will not tune CPython’s table in NFL ETL; trust `dict` unless profiling shows pathological keys.

---

## Reference implementation: `SeparateChainingHashTable`

Simplified teaching class (not production).

```python
from __future__ import annotations

from typing import Any, Hashable, Iterator


class SeparateChainingHashTable:
    """Hash table with separate chaining. Keys must be hashable."""

    def __init__(self, capacity: int = 8) -> None:
        self._capacity = max(4, capacity)
        self._buckets: list[list[tuple[Hashable, Any]]] = [[] for _ in range(self._capacity)]
        self._size = 0

    def _index(self, key: Hashable) -> int:
        return hash(key) % self._capacity

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Hashable) -> bool:
        return self.get(key, _missing := object()) is not _missing

    def get(self, key: Hashable, default: Any = None) -> Any:
        bucket = self._buckets[self._index(key)]
        for k, v in bucket:
            if k == key:
                return v
        return default

    def set(self, key: Hashable, value: Any) -> None:
        i = self._index(key)
        bucket = self._buckets[i]
        for j, (k, _) in enumerate(bucket):
            if k == key:
                bucket[j] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size > self._capacity * 2:
            self._resize(self._capacity * 2)

    def delete(self, key: Hashable) -> bool:
        i = self._index(key)
        bucket = self._buckets[i]
        for j, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(j)
                self._size -= 1
                return True
        return False

    def keys(self) -> Iterator[Hashable]:
        for bucket in self._buckets:
            for k, _ in bucket:
                yield k

    def _resize(self, new_cap: int) -> None:
        old_items = [(k, v) for b in self._buckets for k, v in b]
        self._capacity = new_cap
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for k, v in old_items:
            self.set(k, v)
```

| Operation | Average | Worst |
| --- | --- | --- |
| `get` / `set` / `delete` | O(1) | O(n) |
| `_resize` | O(n) | O(n) |

---

## `dict` operations (with NFL examples and complexity)

### `d[key] = value` / `setdefault`

```python
plays: dict[int, Play] = {}
plays[4021] = Play(4021, "2024_01_KC", "KC", 0.5, "00-001")

meta = plays.setdefault(4021, default_play)  # insert only if missing
```

| | |
| --- | --- |
| **Time** | O(1) average |
| **Space** | O(1) auxiliary |

---

### `d[key]` / `get`

```python
p = plays[4021]
p2 = plays.get(9999)  # None
p3 = plays.get(9999, default_play)
```

| | |
| --- | --- |
| **Time** | O(1) average |
| **Space** | O(1) |

---

### `del d[key]` / `pop`

```python
del plays[4021]
removed = plays.pop(4022, None)
```

| | |
| --- | --- |
| **Time** | O(1) average |
| **Space** | O(1) |

---

### `key in d` / `len(d)`

```python
if 4021 in plays:
    ...
```

| | |
| --- | --- |
| **Time** | O(1) average |
| **Space** | O(1) |

---

### Iteration: `keys`, `values`, `items`

```python
for play_id, play in plays.items():
    total_epa += play.epa
```

| | |
| --- | --- |
| **Time** | O(n) full scan |
| **Space** | O(1) iterator |

**NFL:** Full scan is fine for **one game’s plays**; for season scale use **pandas** vectorization, not Python loops over giant dicts if avoidable.

---

### `update`, merge `|` (3.9+)

```python
plays.update({5001: play_a, 5002: play_b})
merged = plays_a | plays_b
```

| | |
| --- | --- |
| **Time** | O(k) for k new keys |
| **Space** | O(k) |

---

### `dict comprehension` — rebuild index

```python
kc_only = {pid: p for pid, p in plays.items() if p.posteam == "KC"}
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(output) |

---

## `set` operations

```python
seen: set[str] = set()
seen.add("00-0031234")
if "00-0035678" in seen:
    ...
union = seen | other
```

| Operation | Average time |
| --- | --- |
| `add` / `remove` / `in` | O(1) |
| `union` / `intersection` | O(len) |

**NFL:** Unique receivers who targeted in a game.

---

## `Counter` and `defaultdict` patterns

### Formation frequency

```python
formations = Counter(row["personnel"] for row in pbp_rows)
top3 = formations.most_common(3)
```

| | |
| --- | --- |
| **Time** | O(n) over rows |
| **Space** | O(unique formations) |

### EPA by team without KeyError

```python
team_epa: defaultdict[float] = defaultdict(float)
for play in plays.values():
    team_epa[play.posteam] += play.epa
```

| | |
| --- | --- |
| **Time** | O(n) |
| **Space** | O(teams) |

### `Counter` arithmetic

```python
home = Counter({"rush": 20, "pass": 30})
away = Counter({"rush": 18, "pass": 35})
diff = home - away
```

| | |
| --- | --- |
| **Time** | O(keys) |
| **Space** | O(keys) |

```mermaid
sequenceDiagram
  participant ETL
  participant C as Counter
  ETL->>C: update from each play row
  C-->>ETL: most_common(5) formations
```

---

## Building NFL indexes from CSV

```python
import csv

def load_play_index(path: str) -> dict[int, dict]:
    index: dict[int, dict] = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            pid = int(row["play_id"])
            index[pid] = row
    return index

# O(1) lookup during drive replay
row = index[4021]
```

| Phase | Time |
| --- | --- |
| Build index | O(n) |
| Per lookup | O(1) average |

---

## Master complexity table

| Operation | `dict`/`set` avg | Worst | Notes |
| --- | --- | --- | --- |
| `__getitem__` / `__setitem__` | O(1) | O(n) | rare bad hashes |
| `in` | O(1) | O(n) | |
| `del` | O(1) | O(n) | |
| iterate all | O(n) | O(n) | |
| build from n rows | O(n) | O(n) | |
| `Counter` update | O(1) per | O(n) worst | |
| resize (internal) | O(n) | O(n) | amortized |

**Space:** Θ(n) entries plus table overhead.

---

## Python stdlib: what to use

| Need | Type |
| --- | --- |
| Key → value | `dict` |
| Unique keys | `set` |
| Counting | `Counter` |
| Group then aggregate | `defaultdict(list)` + append |
| Ordered by sorted key | `sorted(d)` keys or BST — not hash |
| Disk-scale season | **pandas** + index, or parquet |

```python
import pandas as pd

pbp = pd.read_parquet("plays.parquet")
pbp.set_index("play_id", inplace=True)
row = pbp.loc[4021]  # hash index inside DataFrame
```

---

## When dict vs list vs database

```mermaid
flowchart TD
  Q([Lookup by play_id?])
  Q -->|many random| DICT["dict / DataFrame index"]
  Q -->|scan all| DF["pandas filter"]
  Q -->|persistent team| DB["SQL with index"]
```

| Pitfall | Fix |
| --- | --- |
| Mutable dict as key | Use tuple of ids |
| Assuming sorted keys | `sorted(d)` explicitly |
| Giant dict in tight loop | Vectorize with numpy/pandas |
| `defaultdict` memory | `dict.get` if sparse |
| Rebuilding index every play | Build once per game load |

---

## `frozenset` — hashable set keys

Use when you need a **set as dict key** (e.g. grouping lineups):

```python
skill_group = frozenset({"Mahomes", "Kelce", "Rice"})
lineup_epa: dict[frozenset[str], float] = {}
lineup_epa[skill_group] = 12.4
```

| | |
| --- | --- |
| **Time** | O(1) average lookup |
| **Space** | O(n) for frozenset of n names |

---

## `functools.lru_cache` — memoize expensive NFL queries

Hash table caches **function arguments** → return values:

```python
from functools import lru_cache

@lru_cache(maxsize=4096)
def epa_for_player_season(player_id: str, season: int) -> float:
    # expensive parquet scan once per key
    return load_and_sum(player_id, season)
```

| | |
| --- | --- |
| **Time** | O(1) on cache hit |
| **Space** | O(maxsize) entries |

Keys must be **hashable**—use `str`, `int`, not mutable `dict`.

---

## `defaultdict(list)` — group plays by drive

```python
by_drive: defaultdict[list[dict]] = defaultdict(list)
for row in pbp_rows:
    by_drive[row["drive"]].append(row)
```

| | |
| --- | --- |
| **Time** | O(n) build |
| **Space** | O(n) rows stored |

Same pattern as `pandas.groupby` on a smaller scale in pure Python.

---

## `dict` methods reference (extended)

| Method | Time avg | NFL example |
| --- | --- | --- |
| `keys()` | O(1) view | iterate play ids |
| `values()` | O(1) view | all Play objects |
| `items()` | O(1) view | id + play pairs |
| `get(k, default)` | O(1) | safe lookup missing play |
| `setdefault(k, v)` | O(1) | init team bucket |
| `pop(k)` | O(1) | remove stale cache |
| `popitem()` | O(1) | LIFO eviction policy |
| `clear()` | O(1) | reset game cache |
| `copy()` | O(n) | shallow fork index |
| `fromkeys(keys, v)` | O(n) | init all teams to 0 |
| `dict \| dict` (3.9+) | O(n) | merge indexes |

```mermaid
flowchart TD
  CSV["CSV rows"] --> B["build dict play_id → row"]
  B --> L["O(1) lookup in analysis loop"]
  L --> OUT["charts / EPA"]
```

---

## Open addressing vs chaining (teaching)

| Policy | Idea | Python |
| --- | --- | --- |
| **Separate chaining** | Bucket → list of pairs | Teaching `SeparateChainingHashTable` |
| **Open addressing** | Probe on collision | CPython `dict` (perturbed probing) |

You cannot switch CPython’s policy; understanding collisions explains rare worst-case slowdowns when many keys share hash patterns.

---

## Custom `@dataclass(frozen=True)` as dict key

```python
@dataclass(frozen=True)
class PlayKey:
    game_id: str
    play_id: int

index: dict[PlayKey, Play] = {}
index[PlayKey("2024_01_KC", 4021)] = play
```

| | |
| --- | --- |
| **Time** | O(1) average |
| **Space** | O(1) per key object |

Frozen dataclasses generate `__hash__` automatically when `eq=True`.

---

## `Counter` — advanced NFL stats

```python
from collections import Counter

down_dist = Counter(
    (row["down"], row["ydstogo"])
    for row in pbp_rows
)

# Weighted EPA: not built-in — combine with manual loop or numpy
epa_weights = Counter()
for row in pbp_rows:
    epa_weights[row["play_type"]] += float(row["epa"])
```

| Operation | Time |
| --- | --- |
| `update` | O(k) |
| `most_common(n)` | O(n log n) or O(n) depending on size |
| `elements()` | O(total count) |

---

## When pandas replaces dict

| n (rows) | Recommendation |
| --- | --- |
| < 10⁴ in memory script | `dict` index fine |
| 10⁵–10⁶ season | `DataFrame` + `set_index` |
| Repeated SQL filters | database with B-tree index |

```python
# dict: one game
game_plays = {int(r["play_id"]): r for r in rows}

# pandas: season
import pandas as pd
season = pd.read_parquet("pbp.parquet")
play = season.loc[4021]
```

---

## Set algebra for roster logic

```python
kc_roster = {"00-a", "00-b", "00-c"}
buf_roster = {"00-b", "00-d", "00-e"}

both_teams = kc_roster & buf_roster   # intersection
either = kc_roster | buf_roster       # union
kc_only = kc_roster - buf_roster      # difference
symmetric = kc_roster ^ buf_roster    # in one but not both
```

| Operation | Time avg |
| --- | --- |
| `&` `|` `-` `^` | O(len(smaller)) roughly |

**NFL:** Players who appear on multiple fantasy rosters, or unique to one team.

---

## Inverting index: player → list of play_ids

```python
receiver_plays: defaultdict[list[int]] = defaultdict(list)
for pid, play in plays_by_id.items():
    if play.passer_id:
        receiver_plays[play.passer_id].append(pid)
```

| Build | Lookup plays for player |
| --- | --- |
| O(n) | O(1) get list + O(k) scan k plays |

Pair with [Tries](tries/index.md) when the UI searches **names**; use **dict** when the key is already `player_id`.

---

## Load factor and resize (intuition)

When a CPython `dict` grows past ~2/3 full, it **resizes** to a larger table—occasional O(n) rehash, **amortized O(1)** insert. You see a one-time hitch when a dict jumps from thousands to millions of play keys; pre-size with comprehension from known CSV row count if profiling shows resize spikes.

```python
# If you know n before building
n_plays = 180
plays_by_id = {int(r["play_id"]): r for r in rows}  # one resize pattern
```

---

## Related structures in this guide

| Structure | Link |
| --- | --- |
| [Sets](../sets/index.md) | Set ADT focus |
| [Tries](tries/index.md) | Prefix keys, not hash |
| [Binary search tree](../binary-search-tree/index.md) | Ordered map O(log n) |
| [Array-based lists](../array-based-lists/index.md) | Sequential storage |

---

## Quick reference card

```python
from collections import Counter, defaultdict

# Index plays
plays: dict[int, Play] = {p.play_id: p for p in load()}
p = plays[4021]

# Unique players
seen: set[str] = set()
seen.add(player_id)

# Count formations
cnt = Counter(row["personnel"] for row in rows)

# Sum EPA by team
team_epa: defaultdict[float] = defaultdict(float)
team_epa[team] += epa
```

Use **`dict` / `set` / `Counter` / `defaultdict`** for virtually all NFL hash-table needs in Python. Implement chaining only to **learn** collisions; ship production code with **`dict`** and **pandas indexes**.

**NFL pipeline checklist**

1. **Load once** — Build `play_id → row` map per game or season file.
2. **Keys** — `int`, `str`, `(game_id, play_id)` tuples.
3. **Counts** — `Counter` on categorical columns (formation, play_type).
4. **Aggregates** — `defaultdict` or `groupby` for EPA sums.
5. **Scale** — Move heavy loops to pandas when n > ~10⁵ in pure Python.
