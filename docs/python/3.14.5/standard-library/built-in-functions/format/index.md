# [format()](https://docs.python.org/3/library/functions.html#format)

## Description

Converts a value to a formatted string according to a format specification, delegating to `type(value).__format__()`.

## What problem it solves

Displaying numbers, dates, and aligned columns requires controlled string representation beyond plain `str()`.

## Implementation options

### Option 1: Format numbers with precision and grouping

```python
pi = 3.14159265
assert format(pi, ".2f") == "3.14"
assert format(1_000_000, ",") == "1,000,000"
```

### Option 2: Pad and align text in columns

```python
rows = [("Alice", 95), ("Bob", 87)]
lines = [f"{name:<10}{format(score, '3d')}" for name, score in rows]
assert lines[0] == "Alice      95"
```

## Best practices

- f-strings (`f'{value:.2f}'`) are usually more readable than `format()` for simple cases.
- Learn the [format specification mini-language](https://docs.python.org/3/library/string.html#formatspec) for reusable patterns.
- Custom classes can implement `__format__()` to support format specs in f-strings and `format()`.
