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

### Single-element and empty tuples

```python
single = (42,)
assert single == (42,)
assert tuple() == ()
assert (42) == 42  # parentheses group an int, not a one-tuple
```

## Best practices

- Use tuples for heterogeneous records; use lists when you need mutability.

  ```python
  point = (10, 20)  # record: fixed fields, no accidental append
  assert point[0] == 10

  scores = [88, 91]  # growing collection: use a list
  scores.append(79)
  assert scores[-1] == 79
  ```

- A one-element tuple requires a trailing comma: `(42,)` not `(42)`.

  ```python
  one_tuple = (42,)
  assert one_tuple == (42,)
  assert (42) == 42  # parentheses group an int, not a one-tuple
  ```

- Prefer `tuple` over `list` for hashable composite keys when all elements are hashable.

  ```python
  cache = {}
  key = ("user", 42)
  cache[key] = "Ada"
  assert cache[("user", 42)] == "Ada"
  ```
