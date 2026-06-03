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

### Option 4: `default=` when the iterable may be empty

```python
assert max([], default=0) == 0
assert max([5], default=0) == 5
```

## Best practices

- Provide `default=` when the iterable may be empty to avoid `ValueError`.

  ```python
  assert max([], default=0) == 0
  assert max([5, 9, 3], default=0) == 9

  try:
      max([])
  except ValueError:
      pass
  else:
      raise AssertionError("expected ValueError")
  ```

- When several items tie for max, the first encountered wins (stable behavior).

  ```python
  scores = [88, 92, 75, 92]
  assert max(scores) == 92
  assert max(scores, key=lambda s: (s, scores.index(s))) == 92
  ```

- For repeated top-k selection on a changing collection, consider `heapq.nlargest` instead of sorting the whole iterable each time.

  ```python
  import heapq

  values = [3, 1, 4, 1, 5, 9, 2, 6]
  top_three = heapq.nlargest(3, values)
  assert top_three == [9, 6, 5]
  assert max(values) == 9
  ```
