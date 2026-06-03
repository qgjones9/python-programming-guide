# [ArithmeticError](https://docs.python.org/3/library/exceptions.html#ArithmeticError)

`ArithmeticError` is an intermediate base class in the built-in exception hierarchy: it groups errors that arise from numeric operations, not from bad types, bad keys, or OS failures. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ArithmeticError); the notes below focus on when to catch it and how it relates to its subclasses.

## Role in the hierarchy

- Inherits from [`Exception`](exception/index.md); subclasses inherit from `ArithmeticError`, not from each other.
- The interpreter (or library code) raises the **specific** subclass (`ZeroDivisionError`, `OverflowError`, or `FloatingPointError`); you rarely see a bare `ArithmeticError` instance in practice.
- An `except ArithmeticError` clause matches **any** of those subclasses, because exception matching walks the inheritance tree.

## What problem it solves

Use `ArithmeticError` when you want one handler for “something went wrong with arithmetic” without listing every numeric failure mode. Prefer a **narrower** type (`ZeroDivisionError`, `OverflowError`) when you know exactly what can fail and want clearer control flow.

### Subclass relationships

```python
# Goal: confirm the three built-in arithmetic failure types share this base
assert issubclass(ZeroDivisionError, ArithmeticError)
assert issubclass(OverflowError, ArithmeticError)
assert issubclass(FloatingPointError, ArithmeticError)
assert issubclass(ArithmeticError, Exception)
```

### Catching the base vs a subclass

```python
# Goal: except ArithmeticError handles ZeroDivisionError from division
def safe_ratio(numerator, denominator):
    try:
        return numerator / denominator
    except ArithmeticError as exc:
        return f"failed: {type(exc).__name__}"

assert safe_ratio(1, 0) == "failed: ZeroDivisionError"
assert safe_ratio(4, 2) == 2.0
```

### Order more specific handlers first

Handlers are tried top to bottom; the first matching type wins.

```python
# Goal: a specific except runs before a broad ArithmeticError handler
def label(exc):
    try:
        raise exc
    except ZeroDivisionError:
        return "zero division"
    except ArithmeticError:
        return "other arithmetic"

assert label(ZeroDivisionError()) == "zero division"
assert label(OverflowError()) == "other arithmetic"
```

### Typical sources of each subclass

| Subclass | Often raised when |
|----------|-------------------|
| `ZeroDivisionError` | Division or modulo with a zero divisor (`/`, `//`, `%`). |
| `OverflowError` | A numeric result cannot fit the target representation (for example converting a huge `int` to a C `ssize_t`, or some `struct`/`array` operations). |
| `FloatingPointError` | Reserved for floating-point failures; CPython almost never raises it today—see the upstream note on platform-specific float handling. |

```python
# Goal: division by zero is the most common ArithmeticError subclass in everyday code
caught = None
try:
    10 % 0
except ArithmeticError as exc:
    caught = type(exc).__name__
assert caught == "ZeroDivisionError"
```

## Best practices

- Catch `ArithmeticError` only when you truly intend to treat overflow, division-by-zero, and (theoretical) float faults the same way; otherwise catch the specific subclass.
- For user-defined errors, subclass [`Exception`](exception/index.md) (or a more specific built-in), not `ArithmeticError`, unless you are modeling a family of numeric failures.
- Remember that integer math in Python 3 does **not** raise `OverflowError` on huge `int` results—only operations that must fit a fixed-width or non-arbitrary type do.

## Sections in this repo

Concrete built-in types that inherit from `ArithmeticError`:

- [FloatingPointError](../../concrete-exceptions/floatingpointerror/index.md)
- [OverflowError](../../concrete-exceptions/overflowerror/index.md)
- [ZeroDivisionError](../../concrete-exceptions/zerodivisionerror/index.md)
