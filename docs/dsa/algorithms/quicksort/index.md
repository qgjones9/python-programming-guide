# Quicksort

A **divide-and-conquer** comparison sort: choose a **pivot**, **partition** so keys ≤ pivot sit left and keys &gt; pivot sit right, then recurse on both sides. Average performance is **Θ(n log n)** with low constants; worst case **Θ(n²)** on adversarial or unlucky pivots.

| | |
| --- | --- |
| **What it is** | Partition + two recursive sub-sorts; in-place on arrays with Lomuto or Hoare. |
| **Time** | **Best** Θ(n log n); **average** Θ(n log n); **worst** Θ(n²). |
| **Space** | O(log n) recursion stack average; O(n) worst stack. |
| **Stability** | **Not stable** (partition swaps jump over equals). |
| **In-place** | **Yes** (array partition). |
| **When to use** | General in-memory sort when stability not required; foundation for [Quickselect](../quickselect/index.md). |

**Practical lens:** quicksort is “split the array around a pivot **score**—values at or below the pivot to the left, larger values to the right—then sort each side.” CPython uses **Timsort** for `list.sort`, not pure quicksort, but quicksort still appears in libraries and interviews and powers **order statistics** via partitioning.

[Complexity analysis](../../complexity/index.md) · [Parent: Algorithms](../index.md)

---

## Summary properties

| Property | Value |
| --- | --- |
| **Best time** | Θ(n log n) — balanced partitions |
| **Average time** | Θ(n log n) |
| **Worst time** | Θ(n²) — pivot always min/max |
| **Space** | O(log n) stack typical |
| **Stable** | No |
| **In-place** | Yes |

---

## How it works (Lomuto partition)

1. Pick pivot (often `A[hi]`).
2. `i` tracks boundary of “≤ pivot” region.
3. Scan `j` from `lo` to `hi-1`; if `A[j] ≤ pivot`, swap into `++i` region.
4. Swap pivot to `i+1`; pivot index `p` is final.
5. Recurse on `[lo, p-1]` and `[p+1, hi]`.

**Hoare partition:** two pointers from ends; fewer swaps sometimes; pivot not fixed until end.

```mermaid
flowchart TD
 QS([quicksort A, lo, hi]) --> Check{lo < hi?}
 Check -->|no| Done([return])
 Check -->|yes| P[p = partition A, lo, hi]
 P --> L[quicksort lo, p-1]
 L --> R[quicksort p+1, hi]
 R --> Done
```

```mermaid
sequenceDiagram
 participant A as array
 Note over A: pivot = last element
 loop j from lo to hi-1
 A->>A: if A[j] <= pivot, expand <= region
 end
 A->>A: place pivot at boundary
```

---

## Pseudocode (Lomuto)

```text
QUICKSORT(A, lo, hi):
 if lo >= hi:
 return
 p = PARTITION(A, lo, hi)
 QUICKSORT(A, lo, p - 1)
 QUICKSORT(A, p + 1, hi)

PARTITION(A, lo, hi):
 pivot = A[hi]
 i = lo - 1
 for j = lo to hi - 1:
 if A[j] <= pivot:
 i += 1
 swap A[i], A[j]
 swap A[i + 1], A[hi]
 return i + 1
```

---

## Python implementation

```python
import random
from dataclasses import dataclass


def quicksort(nums: list[float], lo: int = 0, hi: int | None = None) -> None:
 if hi is None:
 hi = len(nums) - 1
 if lo >= hi:
 return
 p = _partition(nums, lo, hi)
 quicksort(nums, lo, p - 1)
 quicksort(nums, p + 1, hi)


def _partition(nums: list[float], lo: int, hi: int) -> int:
 pivot = nums[hi]
 i = lo - 1
 for j in range(lo, hi):
 if nums[j] <= pivot:
 i += 1
 nums[i], nums[j] = nums[j], nums[i]
 nums[i + 1], nums[hi] = nums[hi], nums[i + 1]
 return i + 1


def quicksort_randomized(nums: list[float]) -> None:
 random.shuffle(nums)
 quicksort(nums)


@dataclass(frozen=True, slots=True)
class Record:
 record_id: int
 category: int
 score: float
 label: str


def quicksort_records(
 records: list[Record],
 lo: int = 0,
 hi: int | None = None,
 *,
 key=lambda r: r.score,
) -> None:
 if hi is None:
 hi = len(records) - 1
 if lo >= hi:
 return
 p = _partition_records(records, lo, hi, key=key)
 quicksort_records(records, lo, p - 1, key=key)
 quicksort_records(records, p + 1, hi, key=key)


def _partition_records(records, lo, hi, *, key):
 pivot = key(records[hi])
 i = lo - 1
 for j in range(lo, hi):
 if key(records[j]) <= pivot:
 i += 1
 records[i], records[j] = records[j], records[i]
 records[i + 1], records[hi] = records[hi], records[i + 1]
 return i + 1
```

| | |
| --- | --- |
| **Time** | Avg Θ(n log n), worst Θ(n²) |
| **Space** | O(log n) recursion typical |

**Mitigations:** random pivot, median-of-three, **introsort** (switch to heap sort after depth limit)—what production C++ `std::sort` does.

---

## Trace: partition four scores

`[0.4, -1.2, 1.0, 0.1]`, pivot = `0.1` (last)

| j | action | array (conceptual) |
| ---: | --- | --- |
| — | pivot 0.1 | `[0.4, -1.2, 1.0, 0.1]` |
| 0 | 0.4 &gt; pivot | no swap |
| 1 | -1.2 ≤ pivot | swap → `[-1.2, 0.4, 1.0, 0.1]` |
| 2 | 1.0 &gt; pivot | no swap |
| end | place pivot | `[-1.2, 0.1, 1.0, 0.4]` |

Recurse left `[-1.2]`, right sort `[1.0, 0.4]` → full ascending order.

---

## Versus `list.sort()` / `sorted()` / `heapq`

| | Quicksort | `list.sort` (Timsort) |
| --- | --- | --- |
| Worst time | Θ(n²) naive | Θ(n log n) guaranteed |
| Stable | No | Yes |
| In-place | Yes | Yes (with temp merge buffer in worst cases) |
| Cache | Good locality on arrays | Excellent on real data |

```python
records.sort(key=lambda r: r["amount"], reverse=True)
```

Use **`heapq.nlargest`** when you only need the top 10 values, not full order.

---

## When to use / avoid

| Use | Avoid |
| --- | --- |
| Learning partition logic | Stable ties on equal scores |
| Quickselect foundation | Adversarial inputs without randomization |
| In-memory when library sort unavailable | Large pandas tables—`sort_values` |

---

## Master complexity table

| | Best | Average | Worst | Space |
| --- | --- | --- | --- | --- |
| Time | Θ(n log n) | Θ(n log n) | Θ(n²) | O(log n)–O(n) stack |
| Comparisons | Θ(n log n) | Θ(n log n) | Θ(n²) | — |

---

## Pitfalls

| Pitfall | Fix |
| --- | --- |
| Sorted `record_id` + last pivot | Random or median-of-three |
| Deep recursion | Iterative stack or introsort |
| Need stable sort | Merge sort / `sort` |
| Equal keys clustered with `>` test | `<=` on left partition for balance |

---

## Related pages

| Page | Note |
| --- | --- |
| [Quickselect](../quickselect/index.md) | One-sided recursion |
| [Merge sort](../merge-sort/index.md) | Stable Θ(n log n) |
| [Heap sort](../heap-sort/index.md) | Θ(n log n) worst in-place |
| [Complexity](../../complexity/index.md) | |

---

## Quick reference

```python
quicksort(scores)
quicksort_randomized(scores)
quicksort_records(batch)
batch.sort(key=lambda r: r.score)
```

**Quicksort:** in-place, fast on average, **unstable**, **Θ(n²) worst**—master partition; ship **Timsort/pandas** for large tables.
