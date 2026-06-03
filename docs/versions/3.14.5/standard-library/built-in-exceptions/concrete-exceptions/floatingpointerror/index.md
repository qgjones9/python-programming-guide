# [FloatingPointError](https://docs.python.org/3/library/exceptions.html#FloatingPointError)

Subclass of [`ArithmeticError`](../base-classes/arithmeticerror/index.md) reserved for floating-point failures. Upstream notes it is **not currently used** by CPython ([docs.python.org](https://docs.python.org/3/library/exceptions.html#FloatingPointError)).

---

## When it is raised

| Situation | Notes |
|-----------|-------|
| CPython float exception hook | **Not used** in current CPython |
| Third-party numeric libraries | May raise for platform float faults |
| Manual raise in tests | Verify `except ArithmeticError` handlers |

---

## Role in the hierarchy

| Type | Relationship |
|------|--------------|
| Parent | [`ArithmeticError`](../base-classes/arithmeticerror/index.md) |
| Siblings | [`OverflowError`](overflowerror/index.md), [`ZeroDivisionError`](zerodivisionerror/index.md) |
| Typical use today | Rarely raised; catch `ArithmeticError` if you model numeric libraries that might raise it |

---

## Demonstrating the type

```python
# Goal: confirm hierarchy; manual raise for handler tests
assert issubclass(FloatingPointError, ArithmeticError)
caught = None
try:
    raise FloatingPointError('platform float fault')
except ArithmeticError as exc:
    caught = type(exc).__name__
assert caught == 'FloatingPointError'
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except ArithmeticError` | Library may raise any arithmetic subclass |
| Do not catch for ordinary float math | `inf` / `nan` are normal, not errors |
| Manual raise in tests | Stub handlers for extension integration |

Related: [`OverflowError`](overflowerror/index.md), [`ZeroDivisionError`](zerodivisionerror/index.md).

---

## Best practices

- Do not expect CPython to raise this during ordinary float math (`inf` / `nan` are normal values).
- Third-party extensions linked against platform float exception machinery may still use it.
- Prefer catching [`ArithmeticError`](../base-classes/arithmeticerror/index.md) only when you truly intend to handle all numeric failure modes together.
