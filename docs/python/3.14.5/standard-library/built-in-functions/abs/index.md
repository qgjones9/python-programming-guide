# [abs()](https://docs.python.org/3/library/functions.html#abs)

## Description

`abs()` returns the absolute value of a number. For integers and floats that means distance from zero; for complex numbers it returns the magnitude $\sqrt{re^2 + im^2}$. Objects may participate via `__abs__()`.

## What problem it solves

You often need a non-negative magnitude without branching on sign yourself—distances, deltas, error margins, or normalizing signed inputs before comparison. `abs()` centralizes that logic and respects numeric protocols.

## Implementation options

### Basic numeric use

```python
assert abs(-42) == 42
assert abs(3.14) == 3.14
assert abs(-3.14) == 3.14
assert abs(complex(3, 4)) == 5.0  # magnitude, not component-wise abs
```

### Custom types with `__abs__`

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __abs__(self):
        return Temperature(abs(self.celsius))

assert abs(Temperature(-10)).celsius == 10
```

## Best practices

- Prefer `abs()` over manual `x if x >= 0 else -x` for clarity and protocol support.
- Remember complex numbers return a float magnitude, not a complex result.
- For financial or decimal work, use `Decimal` and its own absolute-value handling rather than mixing with float `abs()` surprises.
