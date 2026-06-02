# [float()](https://docs.python.org/3/library/functions.html#float)

## Description

Constructs a floating-point number from another number, a numeric string, or an object implementing `__float__()` or `__index__()`.

## What problem it solves

Data arrives as strings, integers, or custom numeric types; you need a consistent IEEE-754 float for math, serialization, or API boundaries.

## Implementation options

### Option 1: Parse numeric strings from input data

```python
values = ["1.23", "  -4.5\n", "1e-3"]
parsed = [float(v) for v in values]
assert parsed == [1.23, -4.5, 0.001]
```

### Option 2: Convert integers and custom types

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __float__(self):
        return float(self.celsius)

t = Temperature(36.6)
assert float(t) == 36.6
assert float(42) == 42.0
```

## Best practices

- Be aware of binary floating-point rounding; use `decimal.Decimal` for money and exact decimal math.
- Validate string input before conversion; invalid strings raise `ValueError`.
- Use `math.isfinite()` to detect `inf` and `nan` when parsing external data.
