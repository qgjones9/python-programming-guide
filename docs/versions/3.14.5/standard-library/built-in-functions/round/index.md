# [round()](https://docs.python.org/3/library/functions.html#round)

## Description

`round(number, ndigits=None)` rounds to the nearest multiple of 10⁻ⁿᵈⁱᵍⁱᵗˢ. When two multiples are equally close, Python rounds to the even choice (banker's rounding). With no `ndigits`, the result is an `int`.

## What problem it solves

You need to present numeric results at a fixed precision—for display, reporting, or discrete buckets—without manual string formatting for simple cases.

## Implementation options

### Round to nearest integer

```python
assert round(3.7) == 4
assert round(2.5) == 2  # ties round to even
assert round(3.5) == 4
```

### Round to fixed decimal places

```python
assert round(3.14159, 2) == 3.14
assert round(1234.5678, -2) == 1200.0
```

### Delegate rounding to a custom type via `__round__`

```python
class HalfStep:
    def __init__(self, value):
        self.value = value

    def __round__(self, ndigits=None):
        scaled = self.value * 2
        return round(scaled) / 2

assert round(HalfStep(2.3)) == 2.5
```

## Best practices

- Binary floats cannot represent all decimals exactly—`round(2.675, 2)` may surprise you; use `decimal.Decimal` for money.

  ```python
  from decimal import Decimal, ROUND_HALF_UP

  price = Decimal("2.675")
  assert price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) == Decimal("2.68")
  ```

  ```python
  # Float surprise—not always the decimal you expect:
  assert round(2.675, 2) == 2.67  # not 2.68
  ```

- Omit `ndigits` when you need an integer; pass `ndigits` when you need a float at that precision.

  ```python
  assert round(3.7) == 4
  assert isinstance(round(3.7), int)
  assert round(3.14159, 2) == 3.14
  assert isinstance(round(3.14159, 2), float)
  ```

  ```python
  # Incorrect when you need an int result but pass ndigits=0 expecting int:
  assert isinstance(round(3.7, 0), float)  # 4.0, not int 4
  ```

- For statistically unbiased rounding over many values, banker's rounding reduces bias compared to always rounding .5 up.

  ```python
  assert round(2.5) == 2
  assert round(3.5) == 4  # ties go to even
  ```

  ```python
  # Other languages often round 0.5 away from zero—do not assume that here:
  # assert round(2.5) == 3  # fails in Python
  ```
