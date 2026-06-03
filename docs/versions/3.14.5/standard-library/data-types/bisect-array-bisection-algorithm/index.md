# [bisect — Array bisection algorithm](https://docs.python.org/3/library/bisect.html)

The [`bisect`](https://docs.python.org/3/library/bisect.html) module maintains **sorted lists** by locating insertion points with binary search — O(log n) search, O(n) insert due to list shifting. Functions return indices suitable for `list.insert`; they use `<` comparisons only (never `==` for search). Full performance notes and lookup recipes are on [docs.python.org](https://docs.python.org/3/library/bisect.html).

**Thread safety:** not thread-safe on shared mutable sequences.

---

## Search and insert API

| Function | Insertion point |
|----------|-----------------|
| `bisect_left(a, x)` | Before existing equal values |
| `bisect_right(a, x)` / `bisect(a, x)` | After existing equal values |
| `insort_left(a, x)` | Insert using left policy |
| `insort_right(a, x)` / `insort(a, x)` | Insert using right policy |

All accept optional `lo`, `hi` slice bounds and `key=` (3.10+) for ordering by derived key.

```python
# Goal: maintain sorted unique-ish scores
import bisect

scores = [10, 20, 30]
bisect.insort(scores, 25)
assert scores == [10, 20, 25, 30]
left = bisect.bisect_left(scores, 20)
right = bisect.bisect_right(scores, 20)
assert left == 1 and right == 2
```

---

## Lookup patterns — [Searching Sorted Lists](https://docs.python.org/3/library/bisect.html#searching-sorted-lists)

| Helper intent | Built from |
|---------------|------------|
| Exact index of `x` | `bisect_left` + equality check |
| Greatest value `< x` | `bisect_left` then `a[i-1]` |
| Greatest value `≤ x` | `bisect_right` then `a[i-1]` |
| Smallest value `> x` | `bisect_right` |
| Smallest value `≥ x` | `bisect_left` |

```python
# Goal: map numeric score to letter grade via breakpoints
import bisect

breakpoints = [60, 70, 80, 90]
grades = "FDCBA"

def grade(score):
    i = bisect.bisect(breakpoints, score)
    return grades[i]

assert grade(59) == "F" and grade(90) == "A" and grade(100) == "A"
```

---

## Records with keys

When sorting objects, pass `key=` to search functions; for expensive keys, precompute a parallel key list and bisect that.

```python
# Goal: insert movie by release year into sorted table
import bisect
from collections import namedtuple

Movie = namedtuple("Movie", "title year")
films = [Movie("Jaws", 1975), Movie("Aliens", 1986)]
new = Movie("The Birds", 1963)
bisect.insort(films, new, key=lambda m: m.year)
assert films[0].title == "The Birds"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Keep array **strictly sorted** invariant | Undefined behavior otherwise |
| Use **`bisect` for ranges**, dict for point lookups | Dict O(1) for exact keys |
| **`functools.cache` on key func** in tight loops | Avoid repeated key work |
| Prefer **`sortedcontainers`** for huge dynamic sets | Bisect insert is linear |
| Document **left vs right** policy for duplicates | Affects stability of equal keys |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Concurrent `insort` on same list | Corrupted order | External lock or per-thread lists |
| Mutating list during bisect | Undefined index | Finish bisect before other writes |
| Applying `key` on insert mismatch | Wrong position | Same key function for search and sort |
| Using on `tuple` | `TypeError` on insort | Use list or custom mutable sequence |

---

## See also

- [`heapq`](../heapq-heap-queue-algorithm/index.md) — priority ordering without full sort
- [`array`](../array-efficient-arrays-of-numeric-values/index.md) — compact numeric storage (still needs bisect on values)
