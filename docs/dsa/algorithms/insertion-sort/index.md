# Insertion sort

A **comparison sort** that builds a **sorted prefix** at the left of the array. Each new element is **inserted** into its correct position among the already-sorted items—like sorting a handful of fantasy cards in your hand as you pull them from a pile.

| | |
| --- | --- |
| **What it is** | For each index `i`, shift larger keys right and drop `A[i]` into the hole. |
| **Time** | **Best** O(n) when already sorted; **average** Θ(n²); **worst** Θ(n²). |
| **Space** | O(1) auxiliary—in-place. |
| **Stability** | **Stable** (shift only on strict `>`). |
| **In-place** | **Yes**. |
| **When to use** | Very small *n*, nearly sorted slices, or as the base case inside better hybrids (e.g. Timsort). |

For **NFL analytics**, insertion sort mirrors how you might manually order five **red-zone targets** by share: pick the next receiver, slide down anyone with lower share. At season scale (thousands of rows), use **`sort_values`**; insertion sort shines when *n* &lt; ~20 or data are **already almost sorted** (e.g. plays mostly ordered by `play_id` with a few corrections).

[Complexity analysis](../../complexity/index.md) · [Parent: Algorithms](../index.md)

---

## NFL-shaped use cases

| Task | Why insertion sort fits mentally | Production choice |
| --- | --- | --- |
| Sort 8 players on a single-game leaderboard | O(n²) is tiny | `sorted(..., key=ppr)` |
| Fix a nearly sorted play list after one edit | O(n) best case | `sort_values` or insert in order |
| Teach “growing sorted region” | Clear invariant | This page |
| Hybrid sort inner loop | Timsort uses insertion for runs | CPython internals |

---

## Summary properties

| Property | Value |
| --- | --- |
| **Best time** | O(n) — inner while never runs |
| **Average time** | Θ(n²) |
| **Worst time** | Θ(n²) — reverse PPR order |
| **Space** | O(1) |
| **Stable** | Yes |
| **In-place** | Yes |
| **Adaptive** | Yes |
| **Online** | Can sort as values arrive one-by-one |

---

## How the algorithm works

**Invariant:** `A[0..i-1]` is sorted after processing index `i-1`.

1. Start at `i = 1`.
2. Save `key = A[i]`.
3. Set `j = i - 1`. While `j >= 0` and `A[j] > key`, shift `A[j]` to `A[j+1]` and decrement `j`.
4. Place `key` at `A[j+1]`.
5. Increment `i` until `i == n`.

```mermaid
flowchart TD
  Start([i = 1]) --> Loop{i < n?}
  Loop -->|no| Done([Done])
  Loop -->|yes| Key[key = A[i], j = i-1]
  Key --> Shift{j >= 0 and A[j] > key?}
  Shift -->|yes| Move[A[j+1] = A[j]; j -= 1] --> Shift
  Shift -->|no| Place[A[j+1] = key]
  Place --> Inc[i += 1] --> Loop
```

---

## Pseudocode

```text
INSERTION_SORT(A):
    for i = 1 to n - 1:
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j = j - 1
        A[j + 1] = key
```

---

## Python implementation

```python
from __future__ import annotations

from dataclasses import dataclass


def insertion_sort(nums: list[float]) -> None:
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key


@dataclass(frozen=True, slots=True)
class Player:
    name: str
    ppr: float
    jersey: int


def insertion_sort_players(players: list[Player], *, key=lambda p: p.ppr) -> None:
    for i in range(1, len(players)):
        current = players[i]
        k = key(current)
        j = i - 1
        while j >= 0 and key(players[j]) > k:
            players[j + 1] = players[j]
            j -= 1
        players[j + 1] = current
```

| | |
| --- | --- |
| **Time** | Best O(n), worst Θ(n²) |
| **Space** | O(1) |

---

## Trace: jersey numbers on a practice squad

Sort ascending by **jersey** (stable on equal jerseys if we use strict `>`).

Start: `[89, 12, 12, 45]` (two TEs with jersey 12)

| i | key | Shifts | Result |
| ---: | ---: | --- | --- |
| 1 | 12 | 89→right | `[12, 89, 12, 45]` |
| 2 | 12 | none (89>12) | `[12, 12, 89, 45]` |
| 3 | 45 | none | `[12, 12, 45, 89]` |

Equal jerseys **12** stayed in original relative order → **stable**.

---

## Versus `list.sort()` / `sorted()` / `heapq`

- **`list.sort`**: Timsort combines merge + insertion on **runs**; O(n log n) worst, often faster on real NFL CSV order.
- **`heapq`**: Not a full sort—use for top-*k* receivers, not inserting into a prefix.
- **Insertion sort**: Best didactic match for “one card at a time”; same Θ(n²) class as bubble/selection but **fewer writes** on average and **O(n)** on sorted play_id streams.

```python
# Nearly sorted play_ids — insertion-style thinking:
def one_pass_fix(plays: list[int]) -> bool:
    """True if already non-decreasing."""
    return all(plays[i] <= plays[i + 1] for i in range(len(plays) - 1))
```

---

## When to use / avoid

| Use | Avoid |
| --- | --- |
| *n* &lt; 15 in a notebook demo | Full season player table |
| Educational “sorted prefix” | Latency-critical APIs |
| Custom tiny embedded lists | pandas groupby + sort |

```python
df = weekly_stats.sort_values(["week", "ppr"], ascending=[True, False])
```

---

## Master complexity table

| | Best | Average | Worst | Space |
| --- | --- | --- | --- | --- |
| Time | O(n) | Θ(n²) | Θ(n²) | O(1) |
| Comparisons | O(n) | Θ(n²) | Θ(n²) | — |
| Writes | O(1) | Θ(n²) | Θ(n²) | — |

---

## Pitfalls

| Pitfall | Fix |
| --- | --- |
| Using `>=` in shift test | Breaks stability |
| Binary insertion without shifts | Needs extra space or different structure |
| Sorting millions of rows in Python | Vectorized `sort_values` |

---

## Related pages

| Page | Note |
| --- | --- |
| [Shell sort](../shell-sort/index.md) | Insertion sort with gaps |
| [Bubble sort](../bubble-sort/index.md) | More swaps, less adaptive |
| [Merge sort](../merge-sort/index.md) | Θ(n log n) stable |
| [Complexity](../../complexity/index.md) | Notation |

---

## Quick reference

```python
insertion_sort(ppr)              # in-place
insertion_sort_players(roster)   # stable by PPR
roster.sort(key=lambda p: p.ppr) # production
```

**Insertion sort:** stable, in-place, adaptive—ideal for **small or nearly sorted** NFL slices, not season warehouses.
