# Complexity analysis

How cost grows as input size grows—so you can compare structures and algorithms before you implement them. The ideas below apply to any domain; here you will see them through an **NFL data analysis** lens: play-by-play tables, player lookups, season leaderboards, and pipelines that must stay fast as weeks of data accumulate.

| | |
| --- | --- |
| **What it is** | A way to describe **time** (steps) and **space** (extra memory) as a function of input size *n*, ignoring machine constants. |
| **Why it matters** | The same stats question can be O(n) or O(n²); indexing plays once and reusing a hash map often beats re-scanning a CSV every time you filter by team. |
| **In this guide** | Structure pages use **Trade-off** rows; algorithm pages use **Time & space** rows. Both assume the notation below. |

## Input size and cost

In NFL pipelines, **input size** is whatever you scale with—not always “number of players.”

- **Input size** — Usually *n*, but name the unit:
 - *n* = number of **plays** in a slice (one game, one week, full season export).
 - *m* = number of **players** on rosters you join against.
 - *g* = number of **games** when you aggregate per-game rows.
- **Time complexity** — How comparisons, dictionary lookups, and group-by passes grow as those counts grow (e.g. one full scan of *n* plays is O(n)).
- **Space complexity** — **Extra** memory beyond the raw table: a player-id index, a merge buffer for sorting, recursion stack. Storing the play-by-play file itself is not counted as auxiliary space.

**Example.** You load 50,000 plays for a season (*n* ≈ 5×10⁴). A single pass to sum passing yards per quarterback is O(n) time and O(1) extra space if you only keep running totals. Building a side index `player_id → career row` before thousands of lookups is O(m) space once, then O(1) average time per lookup afterward.

## Asymptotic notation

**Asymptotic** means behavior in the limit—as *n* gets large (more plays, more seasons, more teams in the pool). Notation describes how **time** or **space** scales without pinning down constant factors like “Python loop overhead” or “pandas is faster here.” You care about the **growth class**: constant, logarithmic, linear, quadratic. That is why “3*n* + 5 comparisons per play” is summarized as O(*n*) in [Simplifying expressions](#simplifying-expressions).

| Symbol | Meaning (informal) | NFL-flavored use |
| --- | --- | --- |
| O(g) | Grows **at most** like *g* (upper bound) | Worst-case guarantee: “scan all plays to find one play_id is O(n).” |
| Ω(g) | Grows **at least** like *g* (lower bound) | “Any algorithm that must read every play to compute league-wide EPA/play needs Ω(n) time.” |
| Θ(g) | Grows **exactly** like *g* (tight bound) | “Merge-sorting *m* players by season yards is Θ(m log m) comparisons.” |

When this guide writes Θ(n²) on [bubble sort](../algorithms/bubble-sort/index.md), it means both upper and lower bounds match that rate for the stated model (e.g. number of comparisons).

## Common growth classes

| Class | Name | NFL data analysis example |
| --- | --- | --- |
| O(1) | Constant | Lookup `players[player_id]` after you built a dict; [deque](../data-structures/dequeue-deque/index.md) push/pop when streaming the latest drive into a fixed window |
| O(log n) | Logarithmic | Binary search a **sorted** list of weeks to find the bye week; balanced [BST](../data-structures/binary-search-tree/index.md) if you maintain ordered keys |
| O(n) | Linear | One pass over plays to flag targets of 20+ air yards; scan a [linked list](../data-structures/linked-list/index.md) of drives |
| O(n log n) | Linearithmic | [Merge sort](../algorithms/merge-sort/index.md) receivers by yards; build a [heap](../data-structures/max-heap/index.md) for “top 10 EPA” |
| O(n²) | Quadratic | Naive all-pairs: every play × every play to find duplicate timestamps; nested loops over *n* games × *n* games |
| O(2ⁿ) | Exponential | Enumerate every subset of downs on a drive (fine for tiny *n*, unusable at scale) |

Larger *n* makes slower-growing classes win: sorting 32 teams’ weekly summaries with O(n log n) beats an O(n²) pairwise swap approach once *n* is big enough—even if the O(n²) script was quick to write for a one-off notebook.

## Simplifying expressions

When stating Big-O for a stats job:

1. **Drop constants** — Inspecting 4 fields per play still counts as O(n), not O(4n).
2. **Keep the dominant term** — *n* + *m*² stays O(*m*²) if *m*² dominates (e.g. *m* players, naive all-pairs correlation).
3. **Different variables** — O(n + m) when you read *n* plays and touch *m* roster rows once each (e.g. join plays to players without nested “every play × every player” loops). Graph-style pipelines use O(n + e) for *n* nodes and *e* edges—see [graphs](../data-structures/graphs/index.md).

## Best, average, and worst case

The **same operation** on NFL data can have different costs depending on how you stored the table and what the input looks like:

| Case | Question | NFL example |
| --- | --- | --- |
| **Best** | What is the cheapest possible input? | Plays already sorted by `game_id`, `play_id`: merge weekly files in O(n) |
| **Worst** | What is the most expensive input? | Quicksort players with bad pivots: O(m²); hash map with many id collisions degrades toward O(m) per lookup |
| **Average** | What do we expect over typical or random inputs? | `dict[player_id]` after indexing: O(1) average; degrades if keys cluster badly |

Always ask **which case** a statement refers to. “O(1) player lookup” usually means **average** case after you paid O(m) once to build the index—not O(1) if you linear-scan the roster every time.

## Reading simple code

The patterns below use generic names; read **values** as a column (e.g. `air_yards`) and **n** as `len(plays)`.

**Single loop over *n* items** — O(n): league max air yards on one pass

```python
def max_air_yards(plays: list[dict]) -> float:
 best = plays[0]["air_yards"]
 for snap in plays[1:]:
 yards = snap["air_yards"]
 if yards > best:
 best = yards
 return best
```

**Nested loops, each up to *n*** — O(n²): did two plays share the same `(game_id, play_id)`?

```python
def duplicate_play_keys(plays: list[dict]) -> bool:
 for i in range(len(plays)):
 for j in range(i + 1, len(plays)):
 if (
 plays[i]["game_id"] == plays[j]["game_id"]
 and plays[i]["play_id"] == plays[j]["play_id"]
 ):
 return True
 return False
```

For deduplication at scale, sort by `(game_id, play_id)` and scan once—O(n log n)—or use a set of keys—O(n) average space and time.

**Halving the search space** — O(log n): find a week in a sorted schedule list

```python
def week_index(sorted_weeks: list[int], target: int) -> int | None:
 lo, hi = 0, len(sorted_weeks) - 1
 while lo <= hi:
 mid = (lo + hi) // 2
 if sorted_weeks[mid] == target:
 return mid
 if sorted_weeks[mid] < target:
 lo = mid + 1
 else:
 hi = mid - 1
 return None
```

**Recursion** — Multiply **depth** by **work per level**. Merge-sorting *m* players by total yards: Θ(log m) levels, Θ(m) work per level → Θ(m log m) time and O(m) auxiliary space for the merge buffer (unless in place). See [recursion](../recursion/index.md) for stack depth when you recurse over drive trees or play hierarchies.

## Amortized analysis

Some operations are **usually** cheap but **occasionally** expensive; **amortized** cost spreads that occasional cost over many cheap steps.

- **[Array-based lists](../data-structures/array-based-lists/index.md)** — Appending each new play to `live_plays` is O(1) amortized: most appends are one write; resizing the backing array copies all references rarely enough that *n* appends still cost O(n) total.

Amortized O(1) append is not the same as worst-case O(1) on **every** play during a burst that triggers resize—important if you benchmark live ingest latencies, not just season totals.

## NFL pipeline checklist

When you design or review a stats script, map the work to the table in [Common growth classes](#common-growth-classes):

1. **Name *n* (and *m*, *g*)** — Plays? Players? Games? Weeks?
2. **Count passes** — One full read of the play table per metric is often O(n); doing that inside a loop over 32 teams without an index is O(32·n), still linear in *n* but with a large constant.
3. **Prefer index + scan** — Build `player_id → row` once (O(m)), then answer many O(1) lookups instead of rescanning rosters.
4. **State the case** — Leaderboard after sort: worst-case Θ(m log m); hash lookup: average O(1).
5. **Re-check after pandas** — `groupby` and merges hide loops; the same rules apply to rows touched.

## How to use this in the roadmap

1. Read this page before Phase 1.
2. When you open a structure or algorithm page, map its **Time & space** / **Trade-off** row back to the growth-class table—and ask what *n* means in your NFL (or other) dataset.
3. After implementing in Python, re-check loop structure and whether you chose the case (best / average / worst) that matches production input (sorted feeds, indexed rosters, collision-heavy keys).

Further reading: [Big O notation](https://en.wikipedia.org/wiki/Big_O_notation) (Wikipedia).

[Parent: Data structures and algorithms](../index.md)
