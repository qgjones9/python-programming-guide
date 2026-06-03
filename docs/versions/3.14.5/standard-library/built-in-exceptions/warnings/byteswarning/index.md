# [BytesWarning](https://docs.python.org/3/library/exceptions.html#BytesWarning)

`BytesWarning` relates to **`bytes` and `bytearray` misuse**—especially comparisons or conversions between text and binary data that hide bugs. Canonical docs: [exceptions.html#BytesWarning](https://docs.python.org/3/library/exceptions.html#BytesWarning).

---

## Purpose

Catch `str`/`bytes` confusion early. CPython can emit `BytesWarning` when `-b` is passed once; **`-bb`** (twice) promotes comparisons between `str` and `bytes` to errors via the warnings filter.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default release filters | **Not listed** since Python 3.7 |
| `-b` | Warn on `str`/`bytes` comparisons and related cases |
| `-bb` | Same, with filter action configured to treat `BytesWarning` as **error** |
| Manual emit | Use `warnings.warn(..., BytesWarning)` in libraries guarding binary APIs |

Configuration arrives through `sys.warnoptions` when `-b` / `-bb` is used, not the static default filter tuple alone.

---

## When to emit

- Interpreter when `-b` is enabled and code compares `str` to `bytes`.
- Libraries accepting `bytes` that detect a `str` argument where binary data is required.
- Before silently encoding unknown text as ASCII/Latin-1.

Prefer explicit `TypeError` when the API contract rejects the type outright.

---

## Best practices

- Accept either `str` or `bytes` only when documented; otherwise raise `TypeError`.
- Run sensitive code paths with `-bb` in CI to fail on comparisons.
- Message should show types involved and the decoding strategy if any.

---

## Example — library-side guard

```python
import warnings

def ensure_bytes(payload):
    if isinstance(payload, str):
        warnings.warn(
            "coercing str to ascii bytes; pass bytes instead",
            BytesWarning,
            stacklevel=2,
        )
        return payload.encode("ascii")
    return payload

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    result = ensure_bytes("data")
    assert result == b"data"
    assert issubclass(log[-1].category, BytesWarning)
```

---

## See also

- [`bytes` built-in type](https://docs.python.org/3/library/stdtypes.html#bytes)
- [Command-line `-b` option](https://docs.python.org/3/using/cmdline.html#cmdoption-b)
