# [Numeric Types — int, float, complex](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)

Python has three main numeric types:

- **Integer (`int`)**: Whole numbers with unlimited precision (no fractional part).  
  - *Example*: `42`, `0x10` (hex), `0b1001` (binary)
  - **Booleans (`bool`)** are a subtype of integer; `True` is `1` and `False` is `0`.
- **Floating-point (`float`)**: Approximate real numbers, implemented in C as `double`.  
  - *Example*: `3.14`, `2e-4`
  - For details about internal representation or precision, see `sys.float_info`.
- **Complex (`complex`)**: Numbers with real and imaginary parts, each a float.  
  - *Example*: `1 + 2j`
  - Access parts using `z.real` and `z.imag`.

*Note*: The standard library also offers:
- [fractions.Fraction](https://docs.python.org/3/library/fractions.html) for exact rationals
- [decimal.Decimal](https://docs.python.org/3/library/decimal.html) for user-definable-precision decimals

---

### Creating Numbers (Explanatory Terms)

| Syntax/Constructor     | Meaning (Explanatory)                                                                 |
|------------------------|---------------------------------------------------------------------------------------|
| `42`, `0x2A`, `0o52`   | Integer literals (decimal, hexadecimal, octal) → yields integer                       |
| `3.0`, `2e4`           | Literal includes decimal point or exponent → yields float                             |
| `2j`, `5.1J`           | `j` or `J` appended: imaginary number (complex with zero real part)                   |
| `int(value)`           | Creates an integer from value                                                         |
| `float(value)`         | Converts value to float                                                               |
| `complex(re, im)`      | Complex with real part `re` and imaginary part `im` (defaults to zero if omitted)     |

Numbers can result from **literals** or **built-in functions** (as above), and arithmetic operations.

---

### Mixed Numeric Arithmetic Rules

When using a binary arithmetic operator (`+`, `-`, `*`, etc.) on mixed types:

- If **both** arguments are `complex`, no conversion
- If **one** is `complex` or `float`, the **other** is converted to `float`
- Otherwise, both are `int` (no conversion)

**Explanatory Example:**
- `3 + 2.5` → `float` (result: `5.5`)  
- `5 + 2j` → `complex` (result: `(5+2j)`)

Arithmetic formulas with complex and real types follow mathematical rules:

```python
x + complex(u, v)  →  complex(x + u, v)
x * complex(u, v)  →  complex(x * u, x * v)
```

**Comparisons** between numbers of different types use their *actual values* (not types) for equality/ordering.

---

### Common Numeric Operations (with Explanatory Terms)

All standard numeric types except `complex` support these core operations:

| Operation       | Meaning (Explanatory)                     |
|-----------------|-------------------------------------------|
| `x + y`         | **sum** of `x` and `y`                    |
| `x - y`         | **difference** between `x` and `y`         |
| `x * y`         | **product** (`x` times `y`)                |
| `x / y`         | **quotient** (`x` divided by `y`)          |
| `x // y`        | **floored quotient** (rounds down to int)  |
| `x % y`         | **remainder** of `x / y`                   |
| `-x`            | **negation** (the opposite of `x`)         |
| `+x`            | **identity** (returns `x` unchanged)       |
| `abs(x)`        | **absolute value** or magnitude            |
| `int(x)`        | Converts `x` to **integer**                |
| `float(x)`      | Converts `x` to **floating point**         |
| `complex(x, y)` | **Complex number** from real (`x`) and imaginary (`y`); `y` defaults to zero |
| `c.conjugate()` | **Conjugate** of complex number `c`         |
| `divmod(x, y)`  | Pair (`x // y`, `x % y`)                  |
| `pow(x, y)`     | **Exponentiation** (`x` raised to `y`)     |
| `x ** y`        | Same as above                              |

**Notes (Explanatory):**
- `x // y` (floored division):  
    - *Integer operands*: result is an integer  
    - *Float operands*: result is a float  
    - *Always rounds toward minus infinity*: `-1 // 2 == -1`
- `x % y` is not supported for `complex`.
- `int(float_val)` truncates toward zero.
- `float()` accepts "nan", "inf", "+inf", "-inf" as input.
- By definition: `pow(0, 0)` and `0 ** 0` yield `1` in Python.
- Numeric literals can use digits `0-9` or Unicode equivalents.

---

### Further Operations for Real Numbers (`int`, `float`):

| Operation                 | Meaning (Explanatory)               |
|---------------------------|-------------------------------------|
| `math.trunc(x)`           | **Truncate** to integer part        |
| `round(x[, n])`           | **Round** `x` to `n` digits; if `n` omitted, rounds to nearest integer (ties to even) |
| `math.floor(x)`           | **Largest integer <= x**            |
| `math.ceil(x)`            | **Smallest integer >= x**           |

See the [math](https://docs.python.org/3/library/math.html) and [cmath](https://docs.python.org/3/library/cmath.html) modules for additional numeric operations.


| Subject | Description |
|---------|-------------|
| [Bitwise Operations on Integer Types](bitwise-operations-on-integer-types/index.md) | Bitwise `|`, `^`, `&`, shifts, and `~` on integers, including operator priority and two's complement semantics. |
| [Additional Methods on Integer Types](additional-methods-on-integer-types/index.md) | Extra `int` methods such as `bit_length()`, `bit_count()`, `to_bytes()`, and `from_bytes()`. |
| [Additional Methods on Float](additional-methods-on-float/index.md) | Extra `float` methods including `as_integer_ratio()`, `is_integer()`, `hex()`, and `fromhex()`. |
| [Additional Methods on Complex](additional-methods-on-complex/index.md) | Complex-specific helpers such as `complex.from_number()` for converting other numbers to complex values. |
| [Hashing of numeric types](hashing-of-numeric-types/index.md) | Rules ensuring `hash(x) == hash(y)` when `x == y` across `int`, `float`, and related numeric types. |
