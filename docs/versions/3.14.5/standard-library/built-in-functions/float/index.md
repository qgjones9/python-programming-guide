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

### Option 3: Special values and scientific notation

```python
import math

assert float("inf") == math.inf
assert float("-inf") == -math.inf
assert math.isnan(float("nan"))
assert float("1.5e2") == 150.0
```

### Option 4: Boolean and integer coercion

```python
assert float(True) == 1.0
assert float(False) == 0.0
assert float(10**20) == 10**20  # exact at this magnitude in IEEE double
```

## Best practices

- Binary floating-point cannot represent every decimal exactly; use `decimal.Decimal` for money and other exact decimal math.

  ```python
  from decimal import Decimal

  price = Decimal("0.1") + Decimal("0.2")
  assert price == Decimal("0.3")

  # Float rounding surprise:
  assert 0.1 + 0.2 != 0.3
  ```

- Validate string input before conversion; invalid strings raise `ValueError`.

  ```python
  def parse_float(text: str) -> float:
      text = text.strip()
      if not text:
          raise ValueError("empty input")
      return float(text)

  assert parse_float("  3.14  ") == 3.14

  try:
      float("not-a-number")
  except ValueError:
      pass
  else:
      raise AssertionError("expected ValueError")
  ```

- Use `math.isfinite()` to reject `inf` and `nan` when parsing external data.

  ```python
  import math

  def safe_float(text: str) -> float:
      value = float(text)
      if not math.isfinite(value):
          raise ValueError("non-finite float")
      return value

  assert safe_float("42.0") == 42.0
  assert not math.isfinite(float("inf"))
  ```
