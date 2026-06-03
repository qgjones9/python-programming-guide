# [itertools — Functions creating iterators for efficient looping](https://docs.python.org/3/library/itertools.html)

`itertools` implements **iterator building blocks**—fast, memory-efficient tools for looping, grouping, and combinatorics. Functions return iterators (many infinite); truncate with loops, `islice`, or `takewhile`. Canonical reference: [itertools.html](https://docs.python.org/3/library/itertools.html) and official [Itertools Recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes).

---

## Purpose

Treat iterators as an **algebra**: combine `map`, `filter`, and `itertools` to express pipelines without materializing full sequences. Use with [`functools`](../functools-higher-order-functions-and-operations-on-callable-objects/index.md) (`reduce`, caching) and [`operator`](../operator-standard-operators-as-functions/index.md) (`add`, `mul`, `itemgetter`).

---

## General iterators (selected)

| Function | Result stream | Typical use |
|----------|---------------|-------------|
| [`accumulate`](https://docs.python.org/3/library/itertools.html#itertools.accumulate) | Running reduction | Running sums, products, mins |
| [`batched`](https://docs.python.org/3/library/itertools.html#itertools.batched) | Fixed-size tuples (3.12+) | Chunk bytes/lines for batch APIs |
| [`chain`](https://docs.python.org/3/library/itertools.html#itertools.chain) | Concatenated inputs | Flatten a few iterables |
| [`compress`](https://docs.python.org/3/library/itertools.html#itertools.compress) | Filter by selector flags | Masked selection |
| [`count`](https://docs.python.org/3/library/itertools.html#itertools.count) | Infinite counter | With `map` for `f(0), f(1), …` |
| [`cycle`](https://docs.python.org/3/library/itertools.html#itertools.cycle) | Repeat sequence forever | Round-robin templates (bounded externally) |
| [`dropwhile`](https://docs.python.org/3/library/itertools.html#itertools.dropwhile) / [`takewhile`](https://docs.python.org/3/library/itertools.html#itertools.takewhile) | Prefix/skip while predicate true | Stateful scans |
| [`filterfalse`](https://docs.python.org/3/library/itertools.html#itertools.filterfalse) | Elements where predicate fails | Inverse filter |
| [`groupby`](https://docs.python.org/3/library/itertools.html#itertools.groupby) | Consecutive groups by key | Requires sorted input for global groups |
| [`islice`](https://docs.python.org/3/library/itertools.html#itertools.islice) | Slice iterator by index | Window without indexing sequences |
| [`pairwise`](https://docs.python.org/3/library/itertools.html#itertools.pairwise) | Overlapping pairs (3.10+) | Adjacent differences |
| [`repeat`](https://docs.python.org/3/library/itertools.html#itertools.repeat) | Repeat value n times or forever | Constants stream |
| [`starmap`](https://docs.python.org/3/library/itertools.html#itertools.starmap) | `func(*item)` | Unpack tuple arguments |
| [`tee`](https://docs.python.org/3/library/itertools.html#itertools.tee) | n independent iterators | Expensive; prefer one pass when possible |
| [`zip_longest`](https://docs.python.org/3/library/itertools.html#itertools.zip_longest) | Parallel iterables, pad short | Unequal-length columns |

---

## Combinatoric iterators

| Function | Yields |
|----------|--------|
| [`product`](https://docs.python.org/3/library/itertools.html#itertools.product) | Cartesian product (nested-for equivalent) |
| [`permutations`](https://docs.python.org/3/library/itertools.html#itertools.permutations) | All r-length orderings |
| [`combinations`](https://docs.python.org/3/library/itertools.html#itertools.combinations) | r-length subsets, sorted order |
| [`combinations_with_replacement`](https://docs.python.org/3/library/itertools.html#itertools.combinations_with_replacement) | Subsets with repeated elements |

```python
import itertools

hands = list(itertools.combinations("ABCD", 2))
assert hands == [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D")]

grid = list(itertools.product((0, 1), repeat=2))
assert grid == [(0, 0), (0, 1), (1, 0), (1, 1)]
```

---

## Chaining and batching

```python
import itertools

flat = list(itertools.chain("AB", "CD"))
assert flat == ["A", "B", "C", "D"]

chunks = list(itertools.batched(range(7), 3))
assert chunks == [(0, 1, 2), (3, 4, 5), (6,)]
```

---

## Running aggregates — [`accumulate`](https://docs.python.org/3/library/itertools.html#itertools.accumulate)

Defaults to addition; pass `min`, `max`, or `operator.mul`. Optional **`initial`** prepends a seed and lengthens output by one.

```python
import itertools
import operator

assert list(itertools.accumulate([1, 2, 3, 4])) == [1, 3, 6, 10]
assert list(itertools.accumulate([1, 2, 3, 4], operator.mul)) == [1, 2, 6, 24]
assert list(itertools.accumulate([1, 2, 3], initial=100)) == [100, 101, 103, 106]
```

---

## Grouping — [`groupby`](https://docs.python.org/3/library/itertools.html#itertools.groupby)

Groups **consecutive** items with the same key. For global grouping, **`sorted(iterable, key=key)`** (or `sorted` + `itemgetter`) first.

```python
import itertools
from operator import itemgetter

rows = [
    ("east", "A"),
    ("east", "B"),
    ("west", "C"),
    ("west", "D"),
]
grouped = {k: [name for _, name in g] for k, g in itertools.groupby(rows, key=itemgetter(0))}
assert grouped == {"east": ["A", "B"], "west": ["C", "D"]}
```

---

## Slicing infinite streams — [`islice`](https://docs.python.org/3/library/itertools.html#itertools.islice)

```python
import itertools

first_five = list(itertools.islice(itertools.count(10, 2), 5))
assert first_five == [10, 12, 14, 16, 18]
```

---

## Pairwise windows

```python
import itertools

pairs = list(itertools.pairwise([1, 4, 9, 16]))
assert pairs == [(1, 4), (4, 9), (9, 16)]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| **Sort before `groupby`** | Otherwise same key splits across multiple groups |
| Consume each **group iterator fully** before advancing | Partial consumption leaves internal state inconsistent |
| Avoid **`tee`** on large iterators | Caches values in memory for sibling iterators |
| Bound **`count` / `cycle`** with `islice` or `takewhile` | Prevents accidental infinite loops |
| Prefer **`batched`** over manual index slicing (3.12+) | Clear intent and correct tail handling |
| Use **`starmap`** for iterable-of-tuples | Cleaner than `map` with star-args lambdas |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `groupby` on unsorted data | Duplicate keys in separate groups | `sorted(data, key=key)` first |
| Reusing a consumed iterator | Silent empty results | Create fresh iterator or use `tee` sparingly |
| `product` without `repeat` limit | Exponential blow-up | Estimate size; use `islice` on output |
| Assuming `zip_longest` stops at longest | Stops when *any* exhausted unless `fillvalue` set | Pass `fillvalue` for padding |
| Building `list(chain(...))` on huge inputs | Defeats laziness | Iterate once in a for-loop |

---

## Recipes

The official docs include copy-paste **recipes** (sliding windows, flatten, round-robin, etc.) built from these primitives. See [itertools recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes) on docs.python.org.

---

## See also

- [`functools.reduce`](../functools-higher-order-functions-and-operations-on-callable-objects/index.md) — fold to a single value
- [`operator`](../operator-standard-operators-as-functions/index.md) — `add`, `mul`, `itemgetter` for `accumulate` and `groupby`
- [`heapq`](../../data-types/heapq-heap-queue-algorithm/index.md) — `nlargest` / `nsmallest` with key functions
