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

## Best practices

- A list comprehension `[x for x in items if pred(x)]` is often clearer than `filter()` for simple cases.
- Remember `filter` returns an iterator in Python 3; wrap with `list()` if you need multiple passes.
- Use `itertools.filterfalse()` when you want elements where the predicate is false.
