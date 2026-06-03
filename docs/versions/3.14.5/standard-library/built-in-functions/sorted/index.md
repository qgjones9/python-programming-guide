# [sorted()](https://docs.python.org/3/library/functions.html#sorted)

## Description

`sorted(iterable, /, *, key=None, reverse=False)` returns a new sorted list. The sort is stable: equal elements keep their relative order. Only `<` comparisons are used between items.

## What problem it solves

You need ordered data without mutating the original iterable—especially for one-off ordering, chained sorts, or functional-style pipelines.

## Implementation options

### Basic ascending sort

```python
scores = [88, 92, 75, 92, 81]
assert sorted(scores) == [75, 81, 88, 92, 92]
assert scores == [88, 92, 75, 92, 81]  # unchanged
```

### Sort by a derived key

```python
words = ["Banana", "apple", "Cherry"]
by_lower = sorted(words, key=str.lower)
assert by_lower == ["apple", "Banana", "Cherry"]
```

### Multi-level sort with stable ordering

```python
people = [("Ada", "eng"), ("Grace", "eng"), ("Ada", "ops")]
by_dept_then_name = sorted(people, key=lambda p: (p[1], p[0]))
assert by_dept_then_name == [("Ada", "eng"), ("Grace", "eng"), ("Ada", "ops")]
```

## Best practices

- Use `list.sort()` for in-place sorting when you do not need the original order preserved in a copy.
- Prefer a `key` function over legacy `cmp`; convert old comparators with `functools.cmp_to_key`.
- Sort multiple times with different keys on a stable sort instead of one complex comparator when readability matters.
