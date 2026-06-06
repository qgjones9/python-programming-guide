# Heap sort

A **comparison sort** built on a **binary heap**: place the array in **heap order**, then repeatedly extract the maximum (max-heap) to the end of the array and **sift down** the reduced heap. It guarantees **Θ(n log n)** worst-case time and **O(1)** extra space aside from the array itself.

| | |
| --- | --- |
| **What it is** | `build_max_heap` + (n−1) × (swap root with end + `sift_down`). |
| **Time** | **Best, average, worst** Θ(n log n). |
| **Space** | O(1) auxiliary—in-place on the array. |
| **Stability** | **Not stable**. |
| **In-place** | **Yes**. |
| **When to use** | Guaranteed O(n log n) without merge buffer; understanding [max-heap](../../data-structures/max-heap/index.md) structure. |

In **daily weather data analysis**, imagine a **priority queue of pending anomaly alerts** ranked by magnitude—heap sort is the batch version that drains the max repeatedly to rank readings worst-to-best in-place. For “top 5 hottest days only,” use **`heapq.nlargest`** instead of full heap sort.

**Data-structure deep dive:** heap property, `sift_up` / `sift_down`, and array indexing are covered on [Heap sort (data structures)](../../data-structures/heap-sort/index.md). **This page** focuses on **sorting** readings, stations, and numeric columns.

[Complexity analysis](../../complexity/index.md) · [Parent: Algorithms](../index.md)

---

## Summary properties

| Property | Value |
| --- | --- |
| **Best / average / worst time** | Θ(n log n) |
| **Space** | O(1) in-place |
| **Stable** | No |
| **In-place** | Yes |
| **Comparison-based** | Yes |

---

## How it works

1. **Build max-heap** in O(n): sift down from last parent `⌊n/2⌋−1` down to `0`.
2. For `end` from `n−1` down to `1`:
   - Swap `A[0]` (max) with `A[end]`.
   - Sift down root on range `[0, end)`.
3. Array is ascending if you used max-heap (largest moved to end each step).

```mermaid
flowchart TD
  Start([Build max-heap]) --> Loop{end > 0?}
  Loop -->|no| Done([Sorted ascending])
  Loop -->|yes| Swap[swap A[0] and A[end]]
  Swap --> Sift[sift_down A, 0, end]
  Sift --> Dec[end -= 1] --> Loop
```

---

## Pseudocode

```text
HEAP_SORT(A):
    BUILD_MAX_HEAP(A)
    for end = n - 1 down to 1:
        swap A[0], A[end]
        SIFT_DOWN(A, 0, end)

SIFT_DOWN(A, i, heap_size):
    while true:
        largest = i
        left = 2*i + 1
        right = 2*i + 2
        if left < heap_size and A[left] > A[largest]:
            largest = left
        if right < heap_size and A[right] > A[largest]:
            largest = right
        if largest == i:
            break
        swap A[i], A[largest]
        i = largest
```

---

## Python implementation

```python
from __future__ import annotations

from dataclasses import dataclass


def sift_down(nums: list[float], i: int, heap_size: int) -> None:
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < heap_size and nums[left] > nums[largest]:
            largest = left
        if right < heap_size and nums[right] > nums[largest]:
            largest = right
        if largest == i:
            break
        nums[i], nums[largest] = nums[largest], nums[i]
        i = largest


def build_max_heap(nums: list[float]) -> None:
    n = len(nums)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(nums, i, n)


def heap_sort(nums: list[float]) -> None:
    build_max_heap(nums)
    for end in range(len(nums) - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(nums, 0, end)


@dataclass(frozen=True, slots=True)
class DailyReading:
    station_id: str
    temp_anomaly: float


def heap_sort_readings(readings: list[DailyReading], *, key=lambda r: r.temp_anomaly) -> None:
    n = len(readings)
    idx = list(range(n))

    def sift_idx(i: int, size: int) -> None:
        while True:
            largest = i
            l, r = 2 * i + 1, 2 * i + 2
            if l < size and key(readings[idx[l]]) > key(readings[idx[largest]]):
                largest = l
            if r < size and key(readings[idx[r]]) > key(readings[idx[largest]]):
                largest = r
            if largest == i:
                break
            idx[i], idx[largest] = idx[largest], idx[i]
            i = largest

    for i in range(n // 2 - 1, -1, -1):
        sift_idx(i, n)
    for end in range(n - 1, 0, -1):
        idx[0], idx[end] = idx[end], idx[0]
        sift_idx(0, end)
    readings[:] = [readings[i] for i in idx]
```

| | |
| --- | --- |
| **Time** | Θ(n log n) all cases |
| **Space** | O(1) |

---

## Trace: three temperature anomalies

`[0.4, 2.1, 1.2]` → build heap → repeatedly swap max to end.

After `build_max_heap`: max 2.1 at root (array representation may be `[2.1, 0.4, 1.2]`).

| step | swap root/end | after sift | sorted suffix |
| --- | --- | --- | --- |
| 1 | 2.1 ↔ 1.2 | heap on `[1.2, 0.4]` | `[..., 2.1]` |
| 2 | 1.2 ↔ 0.4 | — | `[0.4, 1.2, 2.1]` |

---

## Versus `list.sort()`, `sorted()`, and `heapq`

| API | Role |
| --- | --- |
| `heapq.heapify` + repeated `heappop` | Same idea as heap sort; Python uses a min-heap |
| `heapq.nlargest(k, readings, key=...)` | Top *k* hottest days—**O(n log k)** |
| `list.sort` | Timsort—faster constants, stable |
| **Heap sort** | In-place **worst-case** Θ(n log n) guarantee |

```python
import heapq

top_anomalies = heapq.nlargest(10, window, key=lambda r: r.temp_anomaly)
full_sorted = sorted(window, key=lambda r: r.temp_anomaly)
```

---

## When to use / avoid

| Use | Avoid |
| --- | --- |
| Teaching heap + guaranteed worst case | Need stable ties on equal anomalies |
| Embedded / memory-tight in-place | pandas-scale climatology tables |
| Introsort fallback in other languages | When `sort_values` is one line |

```python
df.sort_values("temp_anomaly", ascending=True)
```

---

## Master complexity table

| | Best | Average | Worst | Space |
| --- | --- | --- | --- | --- |
| Time | Θ(n log n) | Θ(n log n) | Θ(n log n) | O(1) |
| `build_max_heap` | Θ(n) | Θ(n) | Θ(n) | — |
| Each extract | Θ(log n) | Θ(log n) | Θ(log n) | — |

---

## Pitfalls

| Pitfall | Fix |
| --- | --- |
| Off-by-one in `heap_size` | Pass `end`, not `end-1`, correctly to sift |
| Confusing min-heap vs max-heap | Heap sort on ascending uses max-heap |
| Expecting stability | Use merge sort or `sort` |
| Full sort via `heappop` on copy | Fine for learning; `sort` is faster |

---

## Related pages

| Page | Note |
| --- | --- |
| [Heap sort (data structures)](../../data-structures/heap-sort/index.md) | Structure-first treatment |
| [Max heap](../../data-structures/max-heap/index.md) | Priority queue API |
| [Quicksort](../quicksort/index.md) | In-place, Θ(n²) worst |
| [Merge sort](../merge-sort/index.md) | Stable Θ(n log n) |
| [Complexity](../../complexity/index.md) | |

---

## Quick reference

```python
heap_sort(anomaly_list)
heap_sort_readings(window)
heapq.nlargest(5, window, key=lambda r: r.temp_anomaly)
window.sort(key=lambda r: r.temp_anomaly)
```

**Heap sort:** in-place, **Θ(n log n) worst**, **unstable**—pair with [max-heap](../../data-structures/max-heap/index.md); use **`heapq`** for partial ranks in weather dashboards.
