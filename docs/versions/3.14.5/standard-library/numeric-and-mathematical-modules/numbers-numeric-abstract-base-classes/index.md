# [numbers — Numeric abstract base classes](https://docs.python.org/3/library/numbers.html)

The [`numbers`](https://docs.python.org/3/library/numbers.html) module (PEP 3141) defines an **abstract numeric tower** — a hierarchy of ABCs from general `Number` down through `Complex`, `Real`, `Rational`, and `Integral`. None of these classes are meant to be instantiated directly; they document expected operations and support `isinstance` checks and `register()` for custom types. Full implementer notes (mixed-mode arithmetic, hashing) are on [docs.python.org](https://docs.python.org/3/library/numbers.html).

Built-in `int`, `float`, `complex`, and stdlib [`Fraction`](../fractions-rational-numbers/index.md) / [`Decimal`](../decimal-decimal-fixed-point-and-floating-point-arithmetic/index.md) participate in this tower.

---

## The numeric tower

| ABC | Extends | Typical members / operations |
|-----|---------|------------------------------|
| [`Number`](https://docs.python.org/3/library/numbers.html#numbers.Number) | — | Any numeric; use for “is numeric?” checks |
| [`Complex`](https://docs.python.org/3/library/numbers.html#numbers.Complex) | `Number` | `real`, `imag`, `conjugate()`, `+`, `-`, `*`, `/`, `**`, `abs` |
| [`Real`](https://docs.python.org/3/library/numbers.html#numbers.Real) | `Complex` | Ordering (`<`, `<=`, …), `//`, `%`, `floor`, `ceil`, `trunc` |
| [`Rational`](https://docs.python.org/3/library/numbers.html#numbers.Rational) | `Real` | `numerator`, `denominator` (lowest terms, positive denominator) |
| [`Integral`](https://docs.python.org/3/library/numbers.html#numbers.Integral) | `Rational` | `int` conversion, bitwise ops (`<<`, `&`, `^`, …) |

```python
# Goal: classify built-in and stdlib numeric types
import numbers
from decimal import Decimal
from fractions import Fraction

assert isinstance(42, numbers.Integral)
assert isinstance(Fraction(3, 4), numbers.Rational)
assert isinstance(2.5, numbers.Real)
assert isinstance(1 + 2j, numbers.Complex)
assert isinstance(Decimal("9.99"), numbers.Number)
assert not isinstance("42", numbers.Number)
```

---

## Type checks in APIs

| Check | Use when |
|-------|----------|
| `isinstance(x, numbers.Number)` | Any numeric operand accepted |
| `isinstance(x, numbers.Real)` | Ordering or `math` functions expected |
| `isinstance(x, numbers.Rational)` | Exact ratio semantics (`Fraction`-like) |
| `isinstance(x, numbers.Integral)` | Bitwise ops or index-like values |

Prefer ABC checks over concrete types (`int`, `float`) when third-party numeric types may appear.

```python
# Goal: accept any Real for a tolerance comparison
import numbers
import math

def near_zero(x, *, tol=1e-9):
    if not isinstance(x, numbers.Real):
        raise TypeError("expected a Real number")
    return math.isclose(x, 0.0, abs_tol=tol)

assert near_zero(1e-12) and not near_zero(0.01)
```

---

## Notes for type implementers — [Notes for type implementers](https://docs.python.org/3/library/numbers.html#notes-for-type-implementers)

| Topic | Guidance |
|-------|----------|
| **Equality and hashing** | Equal values must hash equal; watch float vs rational collisions |
| **Mixed-mode ops** | Return `NotImplemented` to delegate to partner’s reflected method |
| **Registering ABCs** | `MyFoo.register(Real)` inserts a custom ABC without breaking MRO |
| **Boilerplate fallbacks** | Coerce to built-in `int`/`float`/`complex` only as last resort |

Custom numeric types should implement `__add__` / `__radd__` pairs that recognize peer types first, then return `NotImplemented` so Python tries the other operand’s methods.

```python
# Goal: register an existing type on the tower without subclassing ABCs
import numbers

class TaggedFloat:
    __slots__ = ("_value",)

    def __init__(self, value):
        self._value = float(value)

    def __float__(self):
        return self._value

numbers.Real.register(TaggedFloat)
assert isinstance(TaggedFloat(1.5), numbers.Real)
assert float(TaggedFloat(2.0)) == 2.0
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Check **`numbers.Real`** before passing values to **`math`** | Rejects strings and arbitrary objects early |
| Keep **`numerator`/`denominator`** in lowest terms for `Rational` | Matches `Fraction` invariants and hash semantics |
| Return **`NotImplemented`**, not raise, for unknown operand types | Enables symmetric mixed-type dispatch |
| Document whether your type is **`Real`** or only **`Complex`** | Ordering ops are invalid on general complex numbers |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `isinstance(x, int)` excludes `numpy.int64` etc. | False negatives in scientific code | Use `numbers.Integral` or explicit union |
| Subclassing ABCs without registering | `isinstance` fails on instances | Call `ABC.register()` or inherit properly |
| Implementing only `__add__` without `__radd__` | `int + MyType` fails | Mirror reflected operators |
| Hash unequal-but-float-equal rationals incorrectly | Dict/set surprises | Follow `Fraction.__hash__` pattern in docs |
