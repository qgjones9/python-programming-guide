# [functools — Higher-order functions and operations on callable objects](https://docs.python.org/3/library/functools.html)

`functools` supplies **higher-order utilities** for callables: memoization, argument binding, generic single-dispatch, comparison-to-key adapters, and decorator metadata. Any callable can be treated as a function here. Canonical reference: [functools.html](https://docs.python.org/3/library/functools.html).

---

## Purpose

Use `functools` when you need to **reuse computation** (`cache`, `lru_cache`), **simplify signatures** (`partial`, `partialmethod`), **preserve wrapped function identity** (`wraps`, `update_wrapper`), or **branch on runtime types** (`singledispatch`, `singledispatchmethod`). Pair with [`itertools`](../itertools-functions-creating-iterators-for-efficient-looping/index.md) and [`operator`](../operator-standard-operators-as-functions/index.md) for iterator pipelines and key functions.

---

## API overview

| Category | Names | Role |
|----------|-------|------|
| Memoization | `cache`, `lru_cache`, `cached_property` | Store results keyed by arguments or per-instance attribute |
| Binding | `partial`, `partialmethod`, `Placeholder` (3.14+) | Freeze positional/keyword args; fill placeholders at call time |
| Ordering | `total_ordering`, `cmp_to_key` | Fill rich comparisons from one method; adapt legacy comparators |
| Reduction | `reduce` | Left-fold iterable to one value (see also `itertools.accumulate`) |
| Dispatch | `singledispatch`, `singledispatchmethod` | Type-based overload on first argument (or first non-`self` arg) |
| Decorator helpers | `wraps`, `update_wrapper` | Copy `__name__`, `__doc__`, `__annotations__`, `__wrapped__` |

---

## Memoization — [`cache`](https://docs.python.org/3/library/functools.html#functools.cache) and [`lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache)

| Decorator | Behavior |
|-----------|----------|
| `@cache` | Unbounded dict cache; equivalent to `lru_cache(maxsize=None)` |
| `@lru_cache(maxsize=128, typed=False)` | Evicts least-recently-used entries when `maxsize` is set |
| `cache_info()`, `cache_clear()` | Introspection and invalidation on wrapped function |

Arguments must be **hashable** (cache keys). Thread-safe, but concurrent calls may compute the same miss twice before caching.

**Do not cache:** functions with side effects, generators, async functions, or time/random-dependent results.

```python
import functools

@functools.lru_cache(maxsize=32)
def slugify(word):
    return word.strip().lower().replace(" ", "-")

assert slugify("Hello World") == "hello-world"
assert slugify.cache_info().hits == 0
assert slugify("Hello World") == "hello-world"
assert slugify.cache_info().hits == 1
slugify.cache_clear()
```

---

## Binding — [`partial`](https://docs.python.org/3/library/functools.html#functools.partial) and [`partialmethod`](https://docs.python.org/3/library/functools.html#functools.partialmethod)

`partial(func, *args, **keywords)` returns a callable that prepends frozen args and merges keywords. **`Placeholder`** (3.14+) marks positional slots filled on the outer call—useful when the argument to freeze is not leftmost.

`partialmethod` is for **class methods**: binds like `partial` but integrates with descriptors (`classmethod`, `staticmethod`).

```python
import functools
from functools import partial, partialmethod

basetwo = partial(int, base=2)
assert basetwo("1010") == 10

class Cell:
    def __init__(self):
        self._alive = False

    def set_state(self, state):
        self._alive = bool(state)

    set_alive = partialmethod(set_state, True)

c = Cell()
c.set_alive()
assert c._alive is True
```

---

## Ordering and keys

| Tool | Use when |
|------|----------|
| `@total_ordering` | You implement one of `__lt__`, `__le__`, `__gt__`, `__ge__` plus `__eq__`; other rich comparisons are synthesized |
| `cmp_to_key(cmp)` | Legacy three-way comparator → `key=` for `sorted`, `heapq`, `itertools.groupby` |

`total_ordering` is convenient but **slower** than hand-written six methods if comparisons are hot.

```python
import functools

@functools.total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) < (other.major, other.minor)

versions = sorted([Version(3, 11), Version(3, 10), Version(2, 7)])
assert [v.minor for v in versions] == [7, 10, 11]
```

---

## Reduction — [`reduce`](https://docs.python.org/3/library/functools.html#functools.reduce)

Applies a two-argument function left-to-right over an iterable. Optional **`initial`** seeds the accumulator and handles empty iterables (positional; keyword form added in 3.14).

For **all intermediate values**, prefer [`itertools.accumulate`](../itertools-functions-creating-iterators-for-efficient-looping/index.md).

```python
import functools
import operator

assert functools.reduce(operator.add, [1, 2, 3, 4], 10) == 20
assert functools.reduce(operator.mul, range(1, 5)) == 24
```

---

## Generic functions — [`singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch)

Dispatch uses the **type of the first argument**. Register implementations with `@fun.register` or `@fun.register(int)`. Inspect with `fun.dispatch(type)` and `fun.registry`.

```python
import functools
from io import StringIO

@functools.singledispatch
def show(value):
    return str(value)

@show.register
def _(value: int):
    return f"int:{value}"

@show.register
def _(value: list):
    return f"list:{len(value)}"

assert show(42) == "int:42"
assert show([1, 2, 3]) == "list:3"
assert show.dispatch(int)(7) == "int:7"
```

---

## Decorator metadata — [`wraps`](https://docs.python.org/3/library/functools.html#functools.wraps)

`@wraps(f)` applies `update_wrapper` so the wrapper exposes the wrapped function’s metadata and sets **`__wrapped__`** for bypassing caches or testing the original.

```python
import functools

def log_calls(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper

@log_calls
def greet(name):
    """Say hello."""
    return f"Hello, {name}"

assert greet.__name__ == "greet"
assert greet.__doc__ == "Say hello."
assert greet.__wrapped__("Ada") == "Hello, Ada"
```

---

## Instance caching — [`cached_property`](https://docs.python.org/3/library/functools.html#functools.cached_property)

Computes an attribute once per instance, then stores it on `__dict__` like a normal attribute (writes are allowed; delete to recompute). Requires a mutable instance `__dict__` (not usable with `__slots__` unless `__dict__` is included).

---

## Best practices

| Practice | Why |
|----------|-----|
| Set `lru_cache(maxsize=…)` on long-lived servers | Prevents unbounded growth unless arguments are strictly bounded |
| Use `typed=True` when `3` and `3.0` must differ | Separate cache entries per argument types |
| Prefer `cache` only for small, pure recursion | Unbounded caches can grow with distinct inputs |
| Stack `@singledispatchmethod` **outermost** | Required when combining with `@classmethod` |
| Read `cache_info()` when tuning | Hits/misses guide `maxsize` choice |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Caching methods without considering `self` | Each instance gets separate entries keyed by `self` | Use `cached_property` or a per-instance dict |
| `lru_cache` on unhashable args | `TypeError` at call time | Normalize to tuples or use a custom cache |
| `total_ordering` without `__eq__` | Incomplete ordering protocol | Always define `__eq__`; return `NotImplemented` for unknown types |
| Forgetting `__wrapped__` bypass | Tests hit cache unexpectedly | Call `func.__wrapped__(*args)` |
| `partial` without `Placeholder` for middle args | Only leading positional args freeze | Use `Placeholder` (3.14+) or a lambda |

---

## See also

- [`itertools`](../itertools-functions-creating-iterators-for-efficient-looping/index.md) — `accumulate` as streaming `reduce`
- [`operator`](../operator-standard-operators-as-functions/index.md) — `operator.add`, `itemgetter` for `reduce` and sorting
- [Sorting HOWTO](https://docs.python.org/3/howto/sorting.html) — `key=` functions and stability
