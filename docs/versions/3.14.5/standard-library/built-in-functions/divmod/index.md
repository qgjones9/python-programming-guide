# [divmod()](https://docs.python.org/3/library/functions.html#divmod)

## Description

`divmod(a, b)` returns `(a // b, a % b)`—the quotient and remainder from integer division in one tuple. It works with integers and floats (float results may differ slightly from separate `//` and `%`).

## What problem it solves

Time conversions, pagination, grid layout, and cyclic indexing often need both how many whole groups fit and what is left over. `divmod()` expresses that pairing without two separate operations.

## Implementation options

### Split seconds into minutes and seconds

```python
total_seconds = 754
minutes, seconds = divmod(total_seconds, 60)
assert minutes == 12
assert seconds == 34
```

### Negative dividend (floor division semantics)

```python
q, r = divmod(-10, 3)
assert q == -4 and r == 2  # -10 == (-4) * 3 + 2
assert q * 3 + r == -10
```

### Page count for a fixed page size

```python
items = list(range(23))
page_size = 5
page_count, remainder = divmod(len(items), page_size)
if remainder:
    page_count += 1
assert page_count == 5
```

## Best practices

- For integers, `divmod(a, b)` equals `(a // b, a % b)` but reads more clearly when both values are needed.

  ```python
  total, size = 17, 5
  pages, remainder = divmod(total, size)
  assert (pages, remainder) == (3, 2)
  assert pages * size + remainder == total
  ```

- With floats, the quotient may differ slightly from `a // b`; trust `divmod` for the paired result.

  ```python
  a, b = 7.0, 2.0
  q, r = divmod(a, b)
  assert q == 3.0 and r == 1.0
  assert q * b + r == a
  ```

- Ensure the divisor is non-zero to avoid `ZeroDivisionError`.

  ```python
  try:
      divmod(10, 0)
      raise AssertionError("expected ZeroDivisionError")
  except ZeroDivisionError:
      pass
  ```
