# [filter()](https://docs.python.org/3/library/functions.html#filter)

## Description

Builds an iterator of elements from an iterable for which a predicate function returns true; with `None`, keeps truthy values.

## What problem it solves

You often need a subset of a sequence—valid records, non-empty strings, or passing scores—without building a full list in memory upfront.

## Implementation options

### Option 1: Keep only passing scores

```python
scores = [55, 72, 88, 41, 90]
passing = list(filter(lambda s: s >= 60, scores))
assert passing == [72, 88, 90]
```

### Option 2: Remove falsy values with filter(None, ...)

```python
values = [0, "", "ok", None, [], 42]
truthy = list(filter(None, values))
assert truthy == ["ok", 42]
```

### Option 3: Keep only non-empty strings

```python
lines = ["  hi  ", "", "world", "   "]
non_empty = list(filter(lambda s: s.strip(), lines))
assert non_empty == ["  hi  ", "world"]
```

### Option 4: Lazy iterator (consume once)

```python
it = filter(lambda x: x % 2 == 0, range(6))
assert next(it) == 0
assert list(it) == [2, 4]
```

## Best practices

- A list comprehension is often clearer than `filter()` for simple predicates; reserve `filter()` when you already have a named function (e.g. `str.isdigit`).

  ```python
  scores = [55, 72, 88, 41, 90]
  passing = [s for s in scores if s >= 60]
  assert passing == [72, 88, 90]
  ```

  ```python
  import operator

  lines = ["123", "abc", "456"]
  digits = list(filter(str.isdigit, lines))
  assert digits == ["123", "456"]
  ```

- Remember `filter()` returns an iterator in Python 3; consume it once or wrap with `list()` if you need multiple passes.

  ```python
  it = filter(lambda x: x % 2 == 0, range(6))
  assert next(it) == 0
  # Second pass requires materializing:
  evens = list(filter(lambda x: x % 2 == 0, range(6)))
  assert evens == [0, 2, 4]
  ```

- Use `itertools.filterfalse()` when you want elements where the predicate is **false**—the inverse of `filter()`.

  ```python
  import itertools

  values = [0, 1, 2, 3, 4]
  odds = list(itertools.filterfalse(lambda x: x % 2 == 0, values))
  assert odds == [1, 3]
  ```
