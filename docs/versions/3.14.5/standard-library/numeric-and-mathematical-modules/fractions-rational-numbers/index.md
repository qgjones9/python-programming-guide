# [fractions — Rational numbers](https://docs.python.org/3/library/fractions.html)

The [`fractions`](https://docs.python.org/3/library/fractions.html) module provides **`Fraction`**, an immutable exact rational type implementing [`numbers.Rational`](../numbers-numeric-abstract-base-classes/index.md). Numerators and denominators are stored in **lowest terms** with a **positive denominator**. Construct from integers, strings, floats, [`Decimal`](../decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md), or any object with `as_integer_ratio()`. Full constructor rules and formatting options are on [docs.python.org](https://docs.python.org/3/library/fractions.html).

---

## Construction

| Form | Example | Notes |
|------|---------|-------|
| Two integers | `Fraction(8, 10)` → `Fraction(-4, 5)` | Normalized; zero denominator raises |
| Single int | `Fraction(7)` → `Fraction(7, 1)` | |
| String | `Fraction('3/7')`, `Fraction('-1.25')` | Spaces around `/` allowed (3.12+) |
| Float | `Fraction(2.25)` → `Fraction(9, 4)` | Binary float may yield huge denominator |
| `Decimal` | `Fraction(Decimal('1.1'))` → `Fraction(11, 10)` | Exact when decimal is exact |

```python
# Goal: exact rationals from strings and reduced form
from fractions import Fraction

assert Fraction(16, -10) == Fraction(-8, 5)
assert Fraction("3/7") == Fraction(3, 7)
assert Fraction("1.414213") == Fraction(1414213, 1000000)
assert Fraction(2.25) == Fraction(9, 4)
```

---

## Properties and conversion

| Member | Meaning |
|--------|---------|
| `numerator` | Signed numerator in lowest terms |
| `denominator` | Positive denominator in lowest terms |
| `as_integer_ratio()` | `(numerator, denominator)` tuple |
| `is_integer()` | True when denominator is 1 (3.12+) |
| `limit_denominator(max=1000000)` | Best rational approx with bounded denominator |

```python
# Goal: recover human-friendly ratio from float noise
from fractions import Fraction
from math import pi

approx_pi = Fraction("3.1415926535897932").limit_denominator(1000)
assert approx_pi == Fraction(355, 113)
assert Fraction(1.1).limit_denominator() == Fraction(11, 10)
```

---

## Arithmetic and builtins integration

| Feature | Behavior |
|---------|----------|
| `+`, `-`, `*`, `/`, `//`, `%`, `**` | Exact rational math |
| `float(f)`, `math.floor`, `math.ceil` | Via `numbers.Real` |
| `round(f, ndigits)` | Half-to-even on fractional part |
| `format`, f-strings | General and float-style presentations (3.12+) |

```python
# Goal: exact addition and rounding
from fractions import Fraction
import math

third = Fraction(1, 3)
assert third + third + third == Fraction(1, 1)
assert math.floor(Fraction(355, 113)) == 3
assert round(Fraction(1, 2)) == 0
assert round(Fraction(1, 2) + Fraction(1, 1)) == 2
```

---

## Class methods

| Method | Accepts |
|--------|---------|
| `Fraction.from_float(f)` | `float` or integral |
| `Fraction.from_decimal(dec)` | `Decimal` or integral |
| `Fraction.from_number(number)` | Rational tower + `as_integer_ratio()` (3.14+) |

Prefer string or `Decimal` sources when you need predictable ratios.

```python
# Goal: percentage change with exact rational formatting
from fractions import Fraction

old_price, new_price = 499, 672
increase = Fraction(new_price, old_price) - 1
label = f"{increase:.2%} price increase"
assert label == "34.67% price increase"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`Fraction('1.1')`** not **`Fraction(1.1)`** when you mean tenths | Float literal is binary-approximated |
| Call **`limit_denominator()`** after float-derived fractions | Collapses float artifacts to small rationals |
| Keep **`Fraction`** for symbolic/exact steps; convert to **`float`** at boundaries | Performance and interoperability |
| Rely on **`math.gcd`** normalization (3.9+) | Consistent int-type gcd |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `Fraction(1.1) == Fraction(11, 10)` | False — different denominators | String/Decimal/limit_denominator |
| Division by zero denominator | `ZeroDivisionError` at construction | Validate inputs |
| Huge denominators from float conversion | Slow arithmetic | limit_denominator or use Decimal |
| Using `Fraction` in `random.choices` weights | TypeError (3.12+) | Convert weights to float |
| Expecting `Fraction` to approximate irrationally | Denominators grow without bound | Use float/decimal for display |
