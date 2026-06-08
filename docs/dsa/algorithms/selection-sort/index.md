# Selection sort

A **comparison sort** that divides the array into a **sorted prefix** and an **unsorted suffix**. Each round, it **selects** the minimum (for ascending) from the unsorted part and swaps it into the next prefix slot.

| | |
| --- | --- |
| **What it is** | Repeatedly pick the smallest remaining score (or `record_id`) and exchange it to the front of the unsorted region. |
| **Time** | **Best, average, worst** all Θ(n²)—always scans the full unsorted tail. |
| **Space** | O(1) auxiliary. |
| **Stability** | **Not stable** with swap-based exchange (long jumps over equal keys). |
| **In-place** | **Yes**. |
| **When to use** | Minimizing **writes** (at most n swaps); teaching “sorted vs unsorted regions.” |

Selection sort is like building a **priority list** left-to-right: each round you scan every remaining record and pull the lowest **score** to the next slot. You always do Θ(n²) work even if the list started sorted—unlike insertion sort’s O(n) best case. For large archives (tens of thousands of rows), use **`sort_values`** or **`list.sort`**; selection sort teaches the min-scan invariant on small batches.

[Complexity analysis](../../complexity/index.md) · [Parent: Algorithms](../index.md)

---

## Summary properties

| Property | Value |
| --- | --- |
| **Best / average / worst time** | Θ(n²) comparisons |
| **Swaps** | ≤ n − 1 |
| **Space** | O(1) |
| **Stable** | No (typical swap implementation) |
| **In-place** | Yes |
| **Adaptive** | No |

---

## How it works

1. For `i` from `0` to `n-2`:
2. `min_idx = i`. Scan `j` from `i+1` to `n-1`; if `A[j] < A[min_idx]`, update `min_idx`.
3. If `min_idx != i`, swap `A[i]` and `A[min_idx]`.
4. After step `i`, `A[0..i]` is sorted.

```mermaid
flowchart TD
 Start([i = 0]) --> Outer{i < n-1?}
 Outer -->|no| Done([Sorted])
 Outer -->|yes| Min[min_idx = i]
 Min --> Scan[j = i+1 .. n-1]
 Scan --> Cmp{A[j] < A[min_idx]?}
 Cmp -->|yes| Set[min_idx = j]
 Cmp -->|no| NextJ{more j?}
 Set --> NextJ
 NextJ -->|yes| Scan
 NextJ -->|no| Swap{min_idx != i?}
 Swap -->|yes| swap A[i], A[min_idx]
 Swap -->|no| Inc[i += 1]
 Inc --> Outer
```

---

## Pseudocode

```text
SELECTION_SORT(A):
 n = length(A)
 for i = 0 to n - 2:
 min_idx = i
 for j = i + 1 to n - 1:
 if A[j] < A[min_idx]:
 min_idx = j
 if min_idx != i:
 swap A[i], A[min_idx]
```

---

## Python implementation

```python
from dataclasses import dataclass


def selection_sort(nums):
 n = len(nums)
 for i in range(n - 1):
 min_idx = i
 for j in range(i + 1, n):
 if nums[j] < nums[min_idx]:
 min_idx = j
 if min_idx != i:
 nums[i], nums[min_idx] = nums[min_idx], nums[i]


@dataclass
class Record:
 label = ""
 record_id = 0  # lower = earlier in ingest order
 score = 0.0


def selection_sort_records(records, *, key=lambda r: r.record_id):
 n = len(records)
 for i in range(n - 1):
 min_idx = i
 for j in range(i + 1, n):
 if key(records[j]) < key(records[min_idx]):
 min_idx = j
 if min_idx != i:
 records[i], records[min_idx] = records[min_idx], records[i]
```

---

## Trace: record_id rank (ascending)

Lower `record_id` = earlier entry in the ingest log. Data: ids `[32, 5, 5, 12]` for four records in one batch (two tied at 5).

| i | Scan finds min | After swap | Prefix sorted |
| ---: | --- | --- | --- |
| 0 | min at index 1 (5) | swap 0↔1 → `[5, 32, 5, 12]` | `[5, …]` |
| 1 | min at index 2 (5) | swap 1↔2 → `[5, 5, 32, 12]` | `[5,5,…]` |
| 2 | min at index 3 (12) | swap → `[5, 5, 12, 32]` | all |

**Stability note:** the two records with id **5** may have swapped relative order when the first `5` moved from index 1 to 0—selection sort is **not stable**.

---

## Versus `list.sort()` / `sorted()` / `heapq`

| | Selection | `list.sort` |
| --- | --- | --- |
| Comparisons | Always Θ(n²) | O(n log n) |
| Swaps | O(n) | More on average |
| Stability | No | Yes (Python 3) |
| Large datasets | Never | Always |

`heapq.nsmallest(k, records, key=...)` finds the next *k* scores without fully sorting—O(n log k).

---

## When to use / avoid

| Use | Avoid |
| --- | --- |
| Flash drives / EEPROM with costly writes | Large aggregate tables |
| Explaining min-scan | Stable tie-breaking on equal scores |
| Interview “implement selection” | pandas pipelines |

```python
records.sort(key=lambda r: (r.record_id, r.label))
```

---

## Master complexity table

| | Best | Average | Worst | Space |
| --- | --- | --- | --- | --- |
| Time | Θ(n²) | Θ(n²) | Θ(n²) | O(1) |
| Swaps | O(n) | O(n) | O(n) | — |

---

## Pitfalls

| Pitfall | Fix |
| --- | --- |
| Expecting O(n) on sorted data | Use insertion sort or `sort` |
| Need stable equal-score order | Merge sort or `sort` |
| Re-scanning for max and min each pass | Bidirectional selection still Θ(n²) |

---

## Related pages

| Page | Note |
| --- | --- |
| [Insertion sort](../insertion-sort/index.md) | Stable, adaptive |
| [Heap sort](../heap-sort/index.md) | Also selects extrema via heap |
| [Quickselect](../quickselect/index.md) | One order statistic, not full sort |
| [Complexity](../../complexity/index.md) | |

---

## Quick reference

```python
selection_sort(nums)
selection_sort_records(window, key=...)
window.sort(key=lambda r: r.record_id)
```

**Selection sort:** in-place, few swaps, **always Θ(n²)**, **not stable**—teach the min-scan idea, then move on.
