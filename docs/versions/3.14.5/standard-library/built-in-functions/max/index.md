# [max()](https://docs.python.org/3/library/functions.html#max)

## Description

`max()` returns the largest item. With one iterable argument, it scans for the maximum. With multiple positional arguments, it compares them directly. Optional `key` and `default` keyword arguments customize ordering and empty-input behavior.

## What problem it solves

Finding peaks—latest timestamp, highest score, biggest file—without writing manual comparison loops.

## Implementation options

### Maximum of an iterable

```python
scores = [88, 92, 75, 92]
assert max(scores) == 92
```

### Compare several values directly

```python
assert max(3, 9, 1) == 9
```

### Use key= for derived ordering

```python
words = ["Banana", "apple", "Cherry"]
assert max(words, key=str.lower) == "Cherry"
```

## Best practices

- Provide `default=` when the iterable may be empty to avoid `ValueError`.
- When several items tie for max, the first encountered wins (stable behavior).
- For repeated max operations on a changing heap, consider `heapq.nlargest`.
