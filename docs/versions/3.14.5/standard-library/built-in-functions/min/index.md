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

## Best practices

- Use `default=` when the iterable might be empty.
- Ties return the first minimal element encountered.
- For complex selection (top-k), use `heapq.nsmallest` instead of sorting the whole iterable.
