# [tuple()](https://docs.python.org/3/library/functions.html#func-tuple)

## Description

`tuple()` returns an immutable sequence type. Tuples can be built from iterables or literal syntax `(a, b)`. Once created, length and elements (of immutable items) are fixed.

## What problem it solves

Fixed collections that should not change—return multiple values, dict keys, protect data from accidental mutation, and slightly more compact storage than lists for static data.

## Implementation options

### From literal syntax

```python
point = (10, 20)
assert point[0] == 10
assert len(point) == 2
```

### From an iterable

```python
assert tuple([1, 2, 2, 3]) == (1, 2, 2, 3)
assert tuple("hi") == ("h", "i")
```

### Unpacking and returning multiple values

```python
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([3, 1, 4, 1, 5])
assert (lo, hi) == (1, 5)
```

## Best practices

- Use tuples for heterogeneous records; lists when you need mutability.
- A one-element tuple requires a trailing comma: `(42,)` not `(42)`.
- Prefer `tuple` over `list` for hashable composite keys when all elements are hashable.
