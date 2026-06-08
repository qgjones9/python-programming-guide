# Radix sort

A **non-comparison** sort that orders keys **digit by digit** (or by fixed-width **characters**), from least significant digit (LSD) or most significant (MSD). When keys have **d** digits and you use a stable digit sort, total time is **Θ(d · (n + k))** where *k* is the digit radix (often 10 or 256).

| | |
| --- | --- |
| **What it is** | Bucket/count per digit place; stable pass per digit preserves prior order. |
| **Time** | **Best, average, worst** Θ(d · n) for LSD with counting sort per digit (fixed *d*). |
| **Space** | O(n + k) per digit pass for counting sort auxiliary. |
| **Stability** | **Stable** when each digit pass is stable (counting sort). |
| **In-place** | **No** (typical counting-sort radix). |
| **When to use** | Fixed-width integers: **product codes**, **record_id** (bounded range), millisecond **timestamps** encoded as ints—not arbitrary floats without scaling. |

Radix sort shines when you sort **32-bit record_id** or **product codes 00–99** in linear passes over digits—think “sort every item in a catalog by code without comparing full strings.” For **floating scores**, you normally scale to integers or use comparison sort / `sort_values`.

[Complexity analysis](../../complexity/index.md) · [Parent: Algorithms](../index.md)

---

## Summary properties

| Property | Value |
| --- | --- |
| **Best / average / worst** | Θ(d · n) with stable counting per digit |
| **Space** | O(n + radix) per pass |
| **Stable** | Yes (LSD + stable digit sort) |
| **In-place** | No (standard) |
| **Comparison-based** | No |

---

## How LSD radix sort works

1. Pad keys to fixed width if needed (e.g. product code always two digits conceptually).
2. For digit position `d` from **least** to **most** significant:
 - **Counting sort** on digit `d` (stable).
3. After last digit, array is sorted.

```mermaid
flowchart TD
 Start([digits d0..d_{w-1} LSD first]) --> Pos{more positions?}
 Pos -->|no| Done([Sorted])
 Pos -->|yes| Count[stable counting sort on current digit]
 Count --> Next[next position] --> Pos
```

---

## Pseudocode (LSD, base 10)

```text
RADIX_SORT_LSD(A, w):
 for digit = 0 to w - 1:
 COUNTING_SORT_BY_DIGIT(A, digit)
```

```text
COUNTING_SORT_BY_DIGIT(A, digit):
 count[0..9] = 0
 for x in A:
 count[digit_value(x, digit)] += 1
 prefix sum count
 build output stable by scanning A backward
 copy output to A
```

---

## Python implementation

```python
from __future__ import annotations

from dataclasses import dataclass


def counting_sort_by_digit(nums: list[int], exp: int) -> None:
 n = len(nums)
 output = [0] * n
 count = [0] * 10
 for x in nums:
 count[(x // exp) % 10] += 1
 for i in range(1, 10):
 count[i] += count[i - 1]
 for i in range(n - 1, -1, -1):
 d = (nums[i] // exp) % 10
 count[d] -= 1
 output[count[d]] = nums[i]
 nums[:] = output


def radix_sort_lsd(nums: list[int]) -> None:
 if not nums:
 return
 max_val = max(nums)
 exp = 1
 while max_val // exp > 0:
 counting_sort_by_digit(nums, exp)
 exp *= 10


@dataclass(frozen=True, slots=True)
class Product:
 name: str
 product_code: int


def radix_sort_product_code(products: list[Product]) -> None:
 for exp in (1, 10):
 n = len(products)
 out: list[Product | None] = [None] * n
 count = [0] * 10
 for p in products:
 count[(p.product_code // exp) % 10] += 1
 for i in range(1, 10):
 count[i] += count[i - 1]
 for i in range(n - 1, -1, -1):
 d = (products[i].product_code // exp) % 10
 count[d] -= 1
 out[count[d]] = products[i]
 products[:] = [p for p in out if p is not None]
```

| | |
| --- | --- |
| **Time** | Θ(d · n) for *d* digits |
| **Space** | O(n) per pass |

---

## Trace: product codes LSD

Sort `[89, 12, 12, 45]` by product code (two decimal digits).

**exp = 1** (ones): buckets → stable order by ones digit 
**exp = 10** (tens): complete sort → `[12, 12, 45, 89]`

Equal codes **12** stay in input order → **stable**.

---

## Versus `list.sort()` / `sorted()` / `heapq`

| | Radix | `sort` |
| --- | --- | --- |
| Float scores | Needs fixed-point scaling | Native |
| Bounded ints | Linear in digits | O(n log n) |
| Strings (product names) | MSD radix on chars | `sort` |

```python
df.sort_values("product_code")
```

---

## When to use / avoid

| Use | Avoid |
| --- | --- |
| Fixed-width `record_id` ints | Arbitrary float scores without quantization |
| Millions of keys, small digit count | Small *n* (overhead) |
| Stable digit passes needed | Negative floats without offset handling |

```python
score_micro = (df["score"] * 1_000_000).astype("int64")
```

---

## Master complexity table

| | Best | Average | Worst | Space |
| --- | --- | --- | --- | --- |
| LSD radix | Θ(d·n) | Θ(d·n) | Θ(d·n) | O(n + σ) per pass |

σ = radix size (10 for decimal digit).

---

## Pitfalls

| Pitfall | Fix |
| --- | --- |
| Unstable digit pass | Breaks LSD correctness |
| Negative numbers | Offset or MSD with sign |
| Variable-length strings | Pad or MSD |
| Treating floats as exact | Use integers or comparison sort |

---

## Related pages

| Page | Note |
| --- | --- |
| [Bucket sort](../bucket-sort/index.md) | Range bins vs digit passes |
| [Merge sort](../merge-sort/index.md) | Comparison stable |
| [Complexity](../../complexity/index.md) | |

---

## Quick reference

```python
radix_sort_lsd(product_code_ints)
radix_sort_product_code(catalog)
df.sort_values("product_code")
```

**Radix sort:** stable, non-comparison, **Θ(d·n)** for fixed digits—ideal for **bounded integers**, not raw **float leaderboards** without scaling.
