# [EncodingWarning](https://docs.python.org/3/library/exceptions.html#EncodingWarning)

`EncodingWarning` (added in Python 3.10) is emitted when **text I/O uses the default locale encoding** instead of an explicit UTF-8 (or other) encoding. It is **opt-in** via `-X warn_default_encoding` or the `PYTHONWARNDEFAULTENCODING` environment variable. Canonical docs: [exceptions.html#EncodingWarning](https://docs.python.org/3/library/exceptions.html#EncodingWarning).

---

## Purpose

Help find implicit `encoding=None` call sites (`open()`, [`io.text_encoding()`](https://docs.python.org/3/library/io.html#io.text_encoding)) before they behave differently across platforms.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | Not enabled until opt-in flags are set |
| Enable globally | `-X warn_default_encoding` or `PYTHONWARNDEFAULTENCODING=1` |
| Library helpers | `io.text_encoding(None)` emits when `sys.flags.warn_default_encoding` is true |
| New APIs | Prefer `encoding="utf-8"` explicitly rather than relying on warnings |

---

## When to emit

- CPython and `io` when default locale encoding is selected and opt-in is active.
- Wrapper libraries via `io.text_encoding()` so **callers** get the warning, not the helper internals.

Do not use `EncodingWarning` for general Unicode issues—see [`UnicodeWarning`](unicodewarning/index.md).

---

## Best practices

- New code: pass `encoding="utf-8"` (or document a deliberate locale default).
- When wrapping `open()`, use `encoding=io.text_encoding(encoding)` so opt-in mode attributes warnings correctly.
- Test with the flag enabled in CI if you support 3.10+.

---

## Example — category and manual emit

```python
import warnings

assert issubclass(EncodingWarning, Warning)

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    warnings.warn(
        "encoding=None selects locale default; pass encoding='utf-8'",
        EncodingWarning,
        stacklevel=1,
    )
    assert issubclass(log[-1].category, EncodingWarning)
```

---

## See also

- [Opt-in EncodingWarning](https://docs.python.org/3/library/io.html#opt-in-encodingwarning)
- [`io.text_encoding()`](https://docs.python.org/3/library/io.html#io.text_encoding)
