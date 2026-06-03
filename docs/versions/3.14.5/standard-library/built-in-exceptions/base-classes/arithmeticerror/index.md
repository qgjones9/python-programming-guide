# [ArithmeticError](https://docs.python.org/3/library/exceptions.html#ArithmeticError)

`ArithmeticError` is an intermediate base class for built-in exceptions raised by **numeric operations**—division by zero, overflow when a value must fit a fixed representation, and (rarely) floating-point faults. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#ArithmeticError); this page focuses on when to catch it and how it relates to its subclasses.

---

## Role in the hierarchy

`ArithmeticError` inherits from [`Exception`](../exception/index.md). The three concrete subclasses inherit from `ArithmeticError`, not from each other. The interpreter usually raises the **specific** subclass; bare `ArithmeticError` instances are uncommon in application code.

| Subclass | Often raised when |
|----------|-------------------|
| [`ZeroDivisionError`](../../concrete-exceptions/zerodivisionerror/index.md) | Division or modulo with a zero divisor (`/`, `//`, `%`) |
| [`OverflowError`](../../concrete-exceptions/overflowerror/index.md) | Result cannot fit the target type (for example huge `int` → `ssize_t`, some `struct`/`array` paths) |
| [`FloatingPointError`](../../concrete-exceptions/floatingpointerror/index.md) | Reserved for float failures; CPython almost never raises it today |

An `except ArithmeticError` clause matches **all** of the above because matching walks the inheritance tree.

```python
# Goal: confirm the three built-in arithmetic failure types share this base
assert issubclass(ZeroDivisionError, ArithmeticError)
assert issubclass(OverflowError, ArithmeticError)
assert issubclass(FloatingPointError, ArithmeticError)
assert issubclass(ArithmeticError, Exception)
```

---

## What problem it solves

Use `ArithmeticError` when one recovery path should handle **any** built-in numeric failure. Prefer a **narrower** type when you know what can fail—`ZeroDivisionError` for divisors, `OverflowError` for fixed-width conversions—so control flow and messages stay precise.

```python
def safe_ratio(numerator, denominator):
    try:
        return numerator / denominator
    except ArithmeticError as exc:
        return f"failed: {type(exc).__name__}"

assert safe_ratio(1, 0) == "failed: ZeroDivisionError"
assert safe_ratio(4, 2) == 2.0
```

### Handler order

Handlers are evaluated top to bottom; the **first** matching type wins.

```python
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

```python
# Goal: division by zero is the most common ArithmeticError subclass in everyday code
caught = None
try:
    10 % 0
except ArithmeticError as exc:
    caught = type(exc).__name__
assert caught == "ZeroDivisionError"
```

---

## When to use `ArithmeticError`

| Use `ArithmeticError` | Use a concrete subclass |
|-----------------------|---------------------------|
| Generic numeric pipeline with several failure modes | Validating a single division or modulo |
| Logging “math failed” at a framework boundary | Converting to fixed-width C integers |
| Teaching inheritance (`issubclass` demos) | User-facing error messages naming the operation |

---

## Best practices

- Catch `ArithmeticError` only when overflow, division-by-zero, and theoretical float faults truly share the same recovery.
- For custom errors, subclass [`Exception`](../exception/index.md) (or a specific built-in), not `ArithmeticError`, unless you model a family of numeric failures.
- Remember that **arbitrary-precision `int`** math in Python 3 does not raise `OverflowError` on huge results—only operations that must fit a fixed-width or non-arbitrary type do.
- Place `except ZeroDivisionError` **before** `except ArithmeticError` in the same block.

---

## Common pitfalls

- Expecting **`OverflowError` from `2 ** 10**9`** on plain ints — it succeeds; overflow applies to constrained representations.
- Relying on **`FloatingPointError`** on CPython — platform float code paths rarely surface it.
- Catching **`ArithmeticError`** when the real bug is **`TypeError`** (for example dividing str by int).
- Subclassing **`ArithmeticError`** for non-numeric domain errors — confuses readers and `except` clauses.

---

## Sections in this repo

Concrete built-in types that inherit from `ArithmeticError`:

| Type | Page |
|------|------|
| [FloatingPointError](../../concrete-exceptions/floatingpointerror/index.md) | Rare float-domain failures |
| [OverflowError](../../concrete-exceptions/overflowerror/index.md) | Fixed-width overflow |
| [ZeroDivisionError](../../concrete-exceptions/zerodivisionerror/index.md) | Division or modulo by zero |

---

## Related pages

| Topic | Link |
|-------|------|
| Application error base | [Exception](../exception/index.md) |
| Parent index | [Base classes](../index.md) |
