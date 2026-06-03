# [min()](https://docs.python.org/3/library/functions.html#min)

## Description

`min()` returns the smallest item. With one iterable, it scans for the minimum; with multiple arguments, it compares them directly. Supports optional `key` and `default` like `max()`.

## What problem it solves

Finding lower bounds—earliest date, cheapest option, closest match threshold—in one readable call.

## Implementation options

### Minimum of a list

```python
temps = [72, 68, 75, 65]
assert min(temps) == 65
```

### Compare multiple scalars

```python
assert min(10, 3, 7) == 3
```

### key= for custom ordering

```python
records = [("Ada", 36), ("Grace", 45)]
youngest = min(records, key=lambda r: r[1])
assert youngest == ("Ada", 36)
```

### Option 4: `default=` avoids `ValueError` on empty input

```python
assert min([], default=99) == 99
assert min([3, 1, 4], default=99) == 1
```

## Best practices

- Use `default=` when the iterable might be empty.

  ```python
  assert min([], default=99) == 99
  assert min([3, 1, 4], default=99) == 1

  try:
      min([])
  except ValueError:
      pass
  else:
      raise AssertionError("expected ValueError")
  ```

- Ties return the first minimal element encountered.

  ```python
  temps = [72, 68, 75, 65, 68]
  assert min(temps) == 65
  assert min(temps, key=lambda t: (t, temps.index(t))) == 65
  ```

- For complex selection (top-k smallest), use `heapq.nsmallest` instead of sorting the whole iterable.

  ```python
  import heapq

  values = [3, 1, 4, 1, 5, 9, 2, 6]
  bottom_three = heapq.nsmallest(3, values)
  assert bottom_three == [1, 1, 2]
  assert min(values) == 1
  ```
