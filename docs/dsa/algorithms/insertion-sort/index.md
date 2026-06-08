# Insertion sort

A **comparison sort** that builds a **sorted prefix** at the left of the array. Each new element is **inserted** into its correct position among the already-sorted items—like ordering a handful of index cards as you pull them from a pile.

| | |
| --- | --- |
| **What it is** | For each index `i`, shift larger keys right and drop `A[i]` into the hole. |
| **Time** | **Best** O(n) when already sorted; **average** Θ(n²); **worst** Θ(n²). |
| **Space** | O(1) auxiliary—in-place. |
| **Stability** | **Stable** (shift only on strict `>`). |
| **In-place** | **Yes**. |
| **When to use** | Very small *n*, nearly sorted slices, or as the base case inside better hybrids (e.g. Timsort). |

Insertion sort mirrors how you might manually order five **records** by `score`: pick the next `Record`, slide down anyone with a lower score. At scale (thousands of rows), use **`sort_values`**; insertion sort shines when *n* &lt; ~20 or data are **already almost sorted** (e.g. records mostly ordered by `record_id` with a few corrections).

[Complexity analysis](../../complexity/index.md) · [Parent: Algorithms](../index.md)

---

## Typical use cases

| Task | Why insertion sort fits mentally | Production choice |
| --- | --- | --- |
| Sort 8 records in one batch by `score` | O(n²) is tiny | `sorted(..., key=lambda r: r.score)` |
| Fix a nearly sorted ingest batch after one edit | O(n) best case | `sort_values` or insert in order |
| Teach "growing sorted region" | Clear invariant | This page |
| Hybrid sort inner loop | Timsort uses insertion for runs | CPython internals |

---

## Summary properties

| Property | Value |
| --- | --- |
| **Best time** | O(n) — inner while never runs |
| **Average time** | Θ(n²) |
| **Worst time** | Θ(n²) — reverse score order |
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


def insertion_sort(nums):
 for i in range(1, len(nums)):
 key = nums[i]
 j = i - 1
 while j >= 0 and nums[j] > key:
 nums[j + 1] = nums[j]
 j -= 1
 nums[j + 1] = key


@dataclass(frozen=True, slots=True)
class Record:
 record_id = 0
 timestamp = 0.0
 score = 0.0
 label = ""


def insertion_sort_records(
 records, *, key=lambda r: r.score
):
 for i in range(1, len(records)):
 current = records[i]
 k = key(current)
 j = i - 1
 while j >= 0 and key(records[j]) > k:
 records[j + 1] = records[j]
 j -= 1
 records[j + 1] = current
```

| | |
| --- | --- |
| **Time** | Best O(n), worst Θ(n²) |
| **Space** | O(1) |

---

## Trace: record IDs in one batch

Sort ascending by **`record_id`** (stable on equal IDs if we use strict `>`).

Start: `[405, 101, 101, 203]` (two rows share `record_id` 101)

| i | key | Shifts | Result |
| ---: | ---: | --- | --- |
| 1 | 101 | 405→right | `[101, 405, 101, 203]` |
| 2 | 101 | none (405>101) | `[101, 101, 405, 203]` |
| 3 | 203 | none | `[101, 101, 405, 203]` |

Equal `record_id` **101** stayed in original relative order → **stable**.

---

## Versus `list.sort()` / `sorted()` / `heapq`

| Tool | When it wins | vs insertion sort |
| --- | --- | --- |
| `list.sort` | Timsort combines merge + insertion on **runs**; O(n log n) worst, often faster on real ingest order | Production default |
| `heapq` | Top-*k* scores, not full prefix sort | Different problem |
| Insertion sort | Best didactic match for "one record at a time"; same Θ(n²) class as bubble/selection but **fewer writes** on average and **O(n)** on sorted `record_id` streams | Pedagogy and tiny *n* |

```python
def one_pass_fix(record_ids):
    return all((record_ids[i] <= record_ids[i + 1] for i in range(len(record_ids) - 1)))
```

---

## When to use / avoid

| Use | Avoid |
| --- | --- |
| *n* &lt; 15 in a notebook demo | Full multi-year archives |
| Educational "sorted prefix" | Latency-critical APIs |
| Custom tiny embedded lists | pandas `groupby` + `sort_values` |

```python
import pandas as pd
df = events.sort_values(['month', 'score'], ascending=[True, False])
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
insertion_sort(scores)
insertion_sort_records(window)
window.sort(key=lambda r: r.score)
```

**Insertion sort:** stable, in-place, adaptive—ideal for **small or nearly sorted** slices, not large archives.
