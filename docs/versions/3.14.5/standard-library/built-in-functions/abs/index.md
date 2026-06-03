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
        # Allow abs() to be called on Temperature, so users can get a
        # Temperature instance representing the magnitude regardless of sign.
        # This enables idioms like abs(temp1 - temp2) if subtraction is defined,
        # or just abs(temp) to express the unsigned distance from 0 °C.
        return Temperature(abs(self.celsius))

# Example usage: abs(Temperature(-10)) returns a new Temperature(10)
# This pattern is helpful when you want your custom class to "just work"
# with built-in numeric tools and maximize interoperability.
assert abs(Temperature(-10)).celsius == 10
```

## Best practices

**Good vs Bad Use Cases for `abs()`**

**Good: Using `abs()` directly for readability and extensibility**
```python
x = -3
result = abs(x)  # 👍 Clear, idiomatic, and works for custom types with __abs__()
```

**Bad: Re-implementing absolute value manually**
```python
x = -3
# 👎 Manual branching, not extensible to custom types, easy to get wrong:
result = x if x >= 0 else -x
```
*Why bad?*  
This only works for types supporting `>=` and unary `-`, skips `__abs__`, and gets tricky with complex numbers or custom types.

---

**Good: Complex numbers with `abs()`**
```python
z = complex(3, 4)
magnitude = abs(z)  # 👍 Returns 5.0, the magnitude (not a complex)
```

**Bad: Expecting abs() on complex to return a 'component-wise' abs**
```python
z = complex(-3, 4)
wrong = complex(abs(z.real), abs(z.imag))  # 👎 Not the same as abs(z); this loses direction
```
*Why bad?*  
`abs(z)` returns the magnitude, not a new complex. The "component-wise" operation is not a true absolute value for complex numbers.

---

**Good: Use Decimal’s methods for financial calculations**
```python
from decimal import Decimal
amount = Decimal('-1.25')
# 👍 Use Decimal's absolute value handling:
clean = abs(amount) # returns a new Decimal object representing the magnitude
print(clean) # prints 1.25
```

**Bad: Mixing Decimal with float before calling abs()**
```python
from decimal import Decimal
amount = Decimal('-1.25')
# 👎 Mixing with float can lose precision:
bad = abs(float(amount)) # returns 1.0, loses precision
print(bad) # prints 1.0
```
*Why bad?*  
Mixing Decimal with float discards precision and can introduce rounding errors. Always use Decimal operations for financial work.
