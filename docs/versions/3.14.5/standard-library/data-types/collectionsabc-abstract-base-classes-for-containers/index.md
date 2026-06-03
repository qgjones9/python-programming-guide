# [collections.abc — Abstract Base Classes for Containers](https://docs.python.org/3/library/collections.abc.html)

The [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) module (split from `collections` in 3.3) defines **abstract base classes (ABCs)** for container interfaces: sized, iterable, mapping, sequence, set, async, and buffer protocols. Use them in `isinstance` / `issubclass` checks and as mixins that supply default method implementations. Full ABC tables and mixin notes are on [docs.python.org](https://docs.python.org/3/library/collections.abc.html).

---

## Registration vs inheritance

| Approach | When to use |
|----------|-------------|
| Subclass ABC directly | New types that should satisfy the full interface |
| `ABC.register(concrete)` | Existing classes/builtins as virtual subclasses |
| Structural checks | Simple ABCs (`Iterable`) may match without register |

Complex ABCs (`Sequence` vs `Mapping`) require semantic methods — not just name presence.

```python
# Goal: virtual registration for a minimal sequence
import collections.abc as abc

class Row:
    def __init__(self, cells):
        self._cells = list(cells)

    def __getitem__(self, index):
        return self._cells[index]

    def __len__(self):
        return len(self._cells)

abc.Sequence.register(Row)
assert isinstance(Row([1, 2, 3]), abc.Sequence)
```

---

## Core ABC families — [Collections Abstract Base Classes](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes)

| ABC | Extends | Abstract methods (typical) |
|-----|---------|----------------------------|
| `Container` | — | `__contains__` |
| `Iterable` | — | `__iter__` |
| `Sized` | — | `__len__` |
| `Collection` | Sized, Iterable, Container | Combined container |
| `Sequence` | Reversible, Collection | `__getitem__`, `__len__` |
| `MutableSequence` | Sequence | `__setitem__`, `insert`, … |
| `Mapping` | Collection | `__getitem__`, `__iter__`, `__len__` |
| `MutableMapping` | Mapping | `__setitem__`, `__delitem__` |
| `Set` / `MutableSet` | Collection | set algebra hooks |
| `Buffer` | — | `__buffer__` (PEP 688, 3.12+) |
| `Awaitable`, `Coroutine`, `AsyncIterable`, … | async stack | awaitable protocols |

`ByteString` is **deprecated** (3.12+); use `Buffer` or explicit `bytes | bytearray | memoryview` in annotations.

---

## Typing with generics (PEP 585)

| Pattern | Example |
|---------|---------|
| Callable parameters | `def consume(items: collections.abc.Iterable[str]) -> None` |
| Mapping keys/values | `collections.abc.Mapping[str, int]` |
| Mutable sequence | `collections.abc.MutableSequence[bytes]` |

```python
# Goal: accept any mapping without dict-only type hints
import collections.abc as abc
from collections import UserDict

def total_values(table: abc.Mapping[str, int]) -> int:
    return sum(table.values())

assert total_values({"a": 1, "b": 2}) == 3
assert total_values(UserDict({"x": 10})) == 10
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Annotate with **ABCs** in public APIs | Accepts `dict`, `UserDict`, custom mappings |
| Use **`iter(obj)`** to test iterability | `isinstance(..., Iterable)` misses `__getitem__` iterables |
| Override slow mixins when `__getitem__` is O(n) | Default `index`/`count` may become quadratic |
| Prefer **`Buffer`** over deprecated `ByteString` | Matches memoryview and PEP 688 |
| Register builtins sparingly | Virtual subclasses must implement full semantics |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `isinstance(x, Iterable)` false negatives | Old-style sequence iteration | Call `iter(x)` in try/except |
| Confusing `Sequence` with `Mapping` | Both have `__getitem__` + `__len__` | Check required abstract methods |
| Generator-based coroutines vs `Coroutine` ABC | `isinstance` false for `@types.coroutine` | Use `inspect.isawaitable` |
| Subclassing `Set` mixin without `_from_iterable` | Set ops build wrong type | Override `_from_iterable` classmethod |

---

## See also

- [`collections`](../collections-container-datatypes/index.md) — concrete container types
- [`abc`](https://docs.python.org/3/library/abc.html) — ABC machinery
- [PEP 3119](https://peps.python.org/pep-3119/) — introduction of ABCs
