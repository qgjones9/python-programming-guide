# [divmod()](https://docs.python.org/3/library/functions.html#divmod)

## Description

Takes two numbers and returns a tuple of their quotient and remainder from integer division.

## What problem it solves

Many algorithms need both the quotient and remainder in one step—time conversions, pagination, or splitting items into groups—without calling `//` and `%` separately.

## Implementation options

### Option 1: Split seconds into minutes and seconds

```python
total_seconds = 754
minutes, seconds = divmod(total_seconds, 60)
assert minutes == 12
assert seconds == 34
```

### Option 2: Paginate a list of items

```python
items = list(range(23))
page_size = 5
for page_num in range(divmod(len(items) + page_size - 1, page_size)[0]):
    start = page_num * page_size
    chunk = items[start : start + page_size]
    assert len(chunk) <= page_size
```

## Best practices

- For integers, `divmod(a, b)` equals `(a // b, a % b)` but reads more clearly when both values are needed.
- With floats, the quotient may differ slightly from `a // b`; trust `divmod` for the paired result.
- Ensure the divisor is non-zero to avoid `ZeroDivisionError`.
