# Complexity analysis

How cost grows as input size grows—so you can compare structures and algorithms before you implement them.

| | |
| --- | --- |
| **What it is** | A way to describe **time** (steps) and **space** (extra memory) as a function of input size *n*, ignoring machine constants. |
| **Why it matters** | The same problem can be O(n) or O(n²); picking the right structure often matters more than micro-optimizing loops. |
| **In this guide** | Structure pages use **Trade-off** rows; algorithm pages use **Time & space** rows. Both assume the notation below. |

## Input size and cost

- **Input size** — Usually *n*: number of elements, nodes, vertices, or bits, depending on the problem.
- **Time complexity** — How the number of primitive steps grows with *n* (comparisons, assignments, pointer hops).
- **Space complexity** — **Extra** memory beyond the input (auxiliary arrays, recursion stack, pointers). Storing the input itself is not counted as auxiliary space.

## Asymptotic notation

**Asymptotic** means behavior in the limit—as input size *n* gets large. Notation here describes how **time** or **space** cost scales as *n* grows, without fixing exact constants or low-order terms. You care about the **growth class** (constant, logarithmic, linear, quadratic): whether work is on the order of *n*, *n* log *n*, *n*², and so on. That is why statements like “3*n* + 5 steps” are summarized as O(*n*) in [Simplifying expressions](#simplifying-expressions).

| Symbol | Meaning (informal) | Typical use |
| --- | --- | --- |
| O(g) | Grows **at most** like *g* (upper bound) | Worst-case guarantee: “search is O(n).” |
| Ω(g) | Grows **at least** like *g* (lower bound) | “Any comparison sort needs Ω(n log n) comparisons in the worst case.” |
| Θ(g) | Grows **exactly** like *g* (tight bound) | “Merge sort uses Θ(n log n) time.” |

When this guide writes Θ(n²) on [bubble sort](../algorithms/bubble-sort/index.md), it means both upper and lower bounds match that rate for the stated model (e.g. number of comparisons).

## Common growth classes

| Class | Name | Example in this guide |
| --- | --- | --- |
| O(1) | Constant | [Deque](../data-structures/dequeue-deque/index.md) push/pop at an end; hash table lookup (average case) |
| O(log n) | Logarithmic | Balanced [BST](../data-structures/binary-search-tree/index.md) search; halving a sorted range |
| O(n) | Linear | Scan a [linked list](../data-structures/linked-list/index.md); one pass over an array |
| O(n log n) | Linearithmic | [Merge sort](../algorithms/merge-sort/index.md); building a [heap](../data-structures/max-heap/index.md) |
| O(n²) | Quadratic | [Bubble sort](../algorithms/bubble-sort/index.md); nested loops over *n* items |
| O(2ⁿ) | Exponential | Naive subsets of a set; rare in basic structure pages |

Larger *n* makes slower-growing classes win: O(n log n) beats O(n²) for large enough *n*, even if the O(n²) code has a smaller constant factor.

## Simplifying expressions

When stating Big-O:

1. **Drop constants** — 3*n* + 5 is O(n).
2. **Keep the dominant term** — *n*² + *n* is O(n²).
3. **Different variables** — O(n + m) when input has *n* items and *m* edges (e.g. [graphs](../data-structures/graphs/index.md)).

## Best, average, and worst case

The **same operation** can have different costs depending on input and implementation:

| Case | Question | Example |
| --- | --- | --- |
| **Best** | What is the cheapest possible input? | Insertion sort on an already sorted array: O(n) |
| **Worst** | What is the most expensive input? | Quicksort with bad pivot choices: O(n²) |
| **Average** | What do we expect over typical or random inputs? | Hash table lookup: O(1) average; degrades if many collisions |

Always ask **which case** a statement refers to. A structure’s “O(1) lookup” often means **average** case (hash table), not worst case.

## Reading simple code

**Single loop over *n* items** — O(n):

```python
def find_max(values: list[int]) -> int:
    best = values[0]
    for x in values[1:]:
        if x > best:
            best = x
    return best
```

**Nested loops, each up to *n*** — O(n²):

```python
def has_duplicate_pair(values: list[int]) -> bool:
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] == values[j]:
                return True
    return False
```

**Halving the search space** — O(log n) (e.g. binary search on a sorted list):

```python
def binary_search(sorted_values: list[int], target: int) -> int | None:
    lo, hi = 0, len(sorted_values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_values[mid] == target:
            return mid
        if sorted_values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None
```

**Recursion** — Multiply **depth** by **work per level**. Merge sort: Θ(log n) levels, Θ(n) work per level → Θ(n log n) time and O(n) auxiliary space for the merge buffer (unless implemented in place). See [recursion](../recursion/index.md) for stack depth and when to prefer iteration.

## Amortized analysis

Some operations are **usually** cheap but **occasionally** expensive; **amortized** cost spreads that occasional cost over many cheap steps.

- **[Array-based lists](../data-structures/array-based-lists/index.md)** — Appending is O(1) amortized: most appends are one write; resizing copies all elements rarely enough that *n* appends still cost O(n) total.

Amortized O(1) is not the same as worst-case O(1) for every single append.

## How to use this in the roadmap

1. Read this page before Phase 1.
2. When you open a structure or algorithm page, map its **Time & space** / **Trade-off** row back to the table above.
3. After implementing in Python, re-check your loop structure and whether you chose the case (best / average / worst) that matches your use case.

Further reading: [Big O notation](https://en.wikipedia.org/wiki/Big_O_notation) (Wikipedia).

[Parent: Data structures and algorithms](../index.md)
