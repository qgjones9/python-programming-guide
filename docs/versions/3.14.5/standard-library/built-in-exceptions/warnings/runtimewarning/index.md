# [RuntimeWarning](https://docs.python.org/3/library/exceptions.html#RuntimeWarning)

`RuntimeWarning` reports **dubious runtime behavior** that is still defined and usually runs to completion—coercion surprises, deprecated interpreter idioms at runtime, or numerically odd but legal operations. Canonical docs: [exceptions.html#RuntimeWarning](https://docs.python.org/3/library/exceptions.html#RuntimeWarning).

---

## Purpose

Separate “something looks wrong while executing” from hard failures ([`ValueError`](../../concrete-exceptions/valueerror/index.md), [`TypeError`](../../concrete-exceptions/typeerror/index.md)) and from compile-time [`SyntaxWarning`](../syntaxwarning/index.md). The interpreter and extension modules emit `RuntimeWarning` for edge cases in numeric and platform code.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | `"default"` — first matching occurrence per location is printed |
| Not ignored by default | Visible in normal application runs unless filtered |
| `"error"` | Raises `RuntimeWarning(message)` |

---

## When to emit

- Behavior that works but violates documented assumptions (e.g. overflow in a cast that succeeds with a lossy result).
- Soft signals from C extensions surfaced to Python.
- Library code when the operation completes but the input or environment is suspicious.

Use [`UserWarning`](../userwarning/index.md) for generic application notices; use `RuntimeWarning` when the issue is specifically “this runtime operation is fishy.”

---

## Best practices

- Include what was attempted and why it is suspicious.
- Use `stacklevel=2+` when the check lives in an internal helper.
- In numerical code, consider whether a exception is clearer than a warning for unrecoverable bad input.

---

## Example — explicit runtime notice

```python
import warnings

def divide_nonzero(a, b):
    if b == 0:
        warnings.warn("division with zero denominator returns inf", RuntimeWarning, stacklevel=2)
        return float("inf")
    return a / b

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    result = divide_nonzero(1.0, 0.0)
    assert result == float("inf")
    assert issubclass(log[-1].category, RuntimeWarning)
```

---

## See also

- [UserWarning](../userwarning/index.md)
- [`warnings` module](https://docs.python.org/3/library/warnings.html)
