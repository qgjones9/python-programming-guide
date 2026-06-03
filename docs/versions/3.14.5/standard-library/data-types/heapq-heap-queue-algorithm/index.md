# [heapq — Heap queue algorithm](https://docs.python.org/3/library/heapq.html)

The [`heapq`](https://docs.python.org/3/library/heapq.html) module implements **binary heap** operations on Python lists. By default it maintains a **min-heap** (`heap[0]` is smallest). Since 3.14, **max-heap** helpers use a `_max` suffix (`heapify_max`, `heappush_max`, …). The API uses **zero-based indexing** and only the `<` operator for comparisons. Priority queues, streaming medians, and merging sorted logs are common uses; full theory and recipes are on [docs.python.org](https://docs.python.org/3/library/heapq.html).

---

## Min-heap operations — [Heap queue algorithm](https://docs.python.org/3/library/heapq.html#basic-examples)

| Function | Effect |
|----------|--------|
| `heapify(x)` | In-place min-heap, O(n) |
| `heappush(heap, item)` | Push preserving invariant |
| `heappop(heap)` | Pop smallest; `IndexError` if empty |
| `heappushpop(heap, item)` | Push then pop — efficient replace-smallest |
| `heapreplace(heap, item)` | Pop then push |

Access smallest without pop: `heap[0]`.

```python
# Goal: streaming smallest-first with tuple priorities
import heapq

h = []
for priority, task in [(3, "low"), (1, "urgent"), (2, "normal")]:
    heapq.heappush(h, (priority, task))
order = [heapq.heappop(h)[1] for _ in range(3)]
assert order == ["urgent", "normal", "low"]
```

---

## Max-heap (3.14+)

| Function | Effect |
|----------|--------|
| `heapify_max(x)` | In-place max-heap |
| `heappush_max` / `heappop_max` | Push/pop largest |
| `heappushpop_max` / `heapreplace_max` | Combined variants |

Largest element at `heap[0]` for max-heaps.

```python
# Goal: top two scores — nlargest avoids full sort; negation builds a max-heap on min-heap API
import heapq

scores = [10, 3, 25, 7, 25]
top_two = heapq.nlargest(2, scores)
assert top_two == [25, 25]

max_heap = [-s for s in scores]
heapq.heapify(max_heap)
assert -heapq.heappop(max_heap) == 25
```

---

## Utility functions

| Function | Use |
|----------|-----|
| `merge(*iterables, key=None, reverse=False)` | Lazy merge of **already sorted** inputs |
| `nlargest(n, iterable, key=None)` | n greatest elements |
| `nsmallst(n, iterable, key=None)` | n smallest elements |

For large `n`, prefer `sorted(iterable)[:n]`; for `n == 1`, use built-in `min`/`max`.

```python
# Goal: merge sorted runs without materializing full list
import heapq

a = [1, 4, 7]
b = [2, 3, 8]
merged = list(heapq.merge(a, b))
assert merged == [1, 2, 3, 4, 7, 8]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Store **(priority, tie_breaker, payload)** tuples | Stable ordering when priorities tie |
| Use **`dataclass(order=True)`** with `compare=False` fields | Clean priority items (3.7+) |
| Call **`heapify` once** on bulk data | Cheaper than repeated `heappush` |
| Mark removed tasks in priority queues | Heaps lack efficient arbitrary delete |
| Choose **`nlargest`** only for small n | Sort wins for large n |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Comparing incomparable task objects | `TypeError` on equal priorities | Add monotonic tie-breaker counter |
| Using `merge` on unsorted iterables | Wrong global order | Pre-sort each input |
| Mixing min- and max-heap ops | Broken invariant | Separate lists or one convention |
| Expecting stable heapsort | Equal elements may reorder | Not stable unlike `sorted` |
| Updating priorities in-place | Heap does not resort automatically | Lazy deletion pattern from docs |

---

## See also

- [`bisect`](../bisect-array-bisection-algorithm/index.md) — sorted list insertion
- [`queue.PriorityQueue`](https://docs.python.org/3/library/queue.html) — thread-safe wrapper
