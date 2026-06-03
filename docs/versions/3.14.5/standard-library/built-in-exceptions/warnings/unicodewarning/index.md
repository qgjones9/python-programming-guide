# [UnicodeWarning](https://docs.python.org/3/library/exceptions.html#UnicodeWarning)

`UnicodeWarning` covers **Unicode-related** conditions that are not hard encoding failures (those use [`UnicodeError`](../../concrete-exceptions/unicodeerror/index.md) subclasses). Canonical docs: [exceptions.html#UnicodeWarning](https://docs.python.org/3/library/exceptions.html#UnicodeWarning).

---

## Purpose

Surface questionable Unicode handling—deprecated codecs, odd normalization, or legacy `str`/`bytes` paths—without aborting the operation when a warning suffices.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | `"default"` |
| Distinction | Failures raise `UnicodeDecodeError` / `UnicodeEncodeError`; warnings flag recoverable oddities |
| `"error"` | Raises `UnicodeWarning(message)` |

---

## When to emit

- Legacy code paths that assume a platform-specific narrow encoding.
- APIs that accept ill-formed text but proceed with a replacement strategy.
- Rare in new code; prefer explicit `encoding="utf-8"` and strict error handlers.

For default-encoding issues in 3.10+, see [`EncodingWarning`](encodingwarning/index.md).

---

## Best practices

- Prefer exceptions with `errors="strict"` when corrupt data must not pass silently.
- Name the encoding, input type, and recommended fix in the message.
- Use `stacklevel=2` in codec wrapper functions.

---

## Example — soft notice on legacy path

```python
import warnings

def decode_legacy(data: bytes):
    warnings.warn(
        "decode_legacy uses replacement; migrate to utf-8",
        UnicodeWarning,
        stacklevel=2,
    )
    return data.decode("utf-8", errors="replace")

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    text = decode_legacy(b"hello \xff world")
    assert "hello" in text
    assert issubclass(log[-1].category, UnicodeWarning)
```

---

## See also

- [EncodingWarning](../encodingwarning/index.md)
- [Unicode HOWTO](https://docs.python.org/3/howto/unicode.html)
