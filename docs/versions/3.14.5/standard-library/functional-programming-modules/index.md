# [Functional Programming Modules](https://docs.python.org/3/library/functional.html)

The standard library groups **iterator tools**, **callable utilities**, and **operator callables** under **Functional Programming Modules**. [`itertools`](itertools-functions-creating-iterators-for-efficient-looping/index.md) builds memory-efficient iterator pipelines; [`functools`](functools-higher-order-functions-and-operations-on-callable-objects/index.md) wraps and composes callables (caching, partial application, generic dispatch); [`operator`](operator-standard-operators-as-functions/index.md) exposes built-in operators as functions for use with `map`, `reduce`, and sorting. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/functional.html).

Related material: [`collections`](../data-types/collections-container-datatypes/index.md) (`defaultdict`, `Counter`), [`heapq`](../data-types/heapq-heap-queue-algorithm/index.md) (priority queues with key functions), and built-in [`map`](https://docs.python.org/3/library/functions.html#map), [`filter`](https://docs.python.org/3/library/functions.html#filter), and [`sorted`](https://docs.python.org/3/library/functions.html#sorted).

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`itertools`](itertools-functions-creating-iterators-for-efficient-looping/index.md) | Lazy iterator algebra: chaining, slicing, grouping, combinatorics |
| [`functools`](functools-higher-order-functions-and-operations-on-callable-objects/index.md) | Decorators, memoization, partials, single-dispatch, metadata preservation |
| [`operator`](operator-standard-operators-as-functions/index.md) | `operator.add`, `itemgetter`, `attrgetter`, in-place operators for functional style |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Merge or window over sequences without building full lists | [`itertools`](itertools-functions-creating-iterators-for-efficient-looping/index.md) (`chain`, `batched`, `islice`) |
| Cache expensive pure function results | [`functools.lru_cache`](functools-higher-order-functions-and-operations-on-callable-objects/index.md) or `cache` |
| Freeze arguments for callbacks | [`functools.partial`](functools-higher-order-functions-and-operations-on-callable-objects/index.md) |
| Overload on argument type (visitor-style) | [`functools.singledispatch`](functools-higher-order-functions-and-operations-on-callable-objects/index.md) |
| Sort/key functions without lambdas | [`operator.itemgetter`](operator-standard-operators-as-functions/index.md) / `attrgetter` |
| Running sum/product over a stream | `itertools.accumulate` with `operator.mul` etc. |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **lazy iterators** for large or infinite data | `itertools` avoids intermediate lists; consume once or use `tee` deliberately |
| **Sort before `groupby`** | `groupby` only groups *consecutive* equal keys |
| Cache only **pure** functions | `lru_cache` retains argument/result references; side effects and I/O break expectations |
| Use **`@wraps`** on decorators | Preserves `__name__`, `__doc__`, and `__wrapped__` for introspection |
| Pass **`key=`** to `sorted` / `heapq` | `functools.cmp_to_key` bridges legacy comparators; `operator.itemgetter` is usually clearer |
| Avoid unbounded **`cycle`** / **`count`** without truncation | Infinite iterators need `islice`, `takewhile`, or a bounded loop |

```python
# Goal: compose iterator tools with functools caching
import functools
import itertools
import operator

@functools.cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

running = list(itertools.accumulate(range(1, 6), operator.mul))
assert fib(10) == 55 and running == [1, 2, 6, 24, 120]
```

```python
# Goal: sort by field with operator getter (no lambda)
import operator

inventory = [("pear", 5), ("apple", 3), ("banana", 2)]
by_count = sorted(inventory, key=operator.itemgetter(1))
assert by_count[0][0] == "banana"
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `groupby` on unsorted data | Multiple groups for same key | `sorted(iterable, key=…)` first |
| `lru_cache` on unhashable args | `TypeError` at call time | Normalize to tuples or use manual dict cache |
| Caching **methods** includes `self` in key | Stale or bloated cache per instance | Use function-level cache or `cached_property` |
| `reduce` on empty iterable without `initial` | `TypeError` | Pass explicit initial value |
| `tee` iterators not consumed in parallel | Unbounded memory from one branch | Consume both branches or avoid `tee` |
| `operator.contains(a, b)` argument order | `b in a`, not `a in b` | Remember reversed operands |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [functools — Higher-order functions and operations on callable objects](functools-higher-order-functions-and-operations-on-callable-objects/index.md) | `lru_cache`, `partial`, `singledispatch`, `wraps`, `reduce` |
| [itertools — Functions creating iterators for efficient looping](itertools-functions-creating-iterators-for-efficient-looping/index.md) | Iterator algebra, combinatorics, recipes |
| [operator — Standard operators as functions](operator-standard-operators-as-functions/index.md) | Operator functions, `itemgetter`, in-place ops |
