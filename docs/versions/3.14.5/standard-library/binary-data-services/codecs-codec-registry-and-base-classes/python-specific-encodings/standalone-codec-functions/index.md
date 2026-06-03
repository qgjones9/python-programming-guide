# [Standalone Codec Functions](https://docs.python.org/3/library/codecs.html#python-specific-encodings-standalone-codec-functions)

`codecs.escape_encode()` and `codecs.escape_decode()` provide **bytes ↔ escaped bytes** conversion similar to how `repr()` displays bytes, but they are **not** registered names—you cannot call `codecs.encode(..., 'escape')`. Pickle and internal machinery use these helpers. API on [docs.python.org](https://docs.python.org/3/library/codecs.html#python-specific-encodings-standalone-codec-functions).

---

## Functions

| Function | Input | Output |
|----------|-------|--------|
| `escape_encode(input, errors=None)` | `bytes` | `(escaped_bytes, length_consumed)` |
| `escape_decode(input, errors=None)` | bytes-like | `(original_bytes, length_consumed)` |

`errors` is ignored for `escape_encode`; decode uses standard handlers when invalid.

```python
# Goal: escape bytes for ASCII-only transport
import codecs

raw = b"line1\n\xff"
escaped, n = codecs.escape_encode(raw)
assert n == len(raw)
assert b"\\n" in escaped and b"\\xff" in escaped
restored, _ = codecs.escape_decode(escaped)
assert restored == raw
```

```python
# Goal: compare with repr-style backslashes
import codecs

b = b"\x00"
escaped, _ = codecs.escape_encode(b)
assert escaped == b"\\x00"
```

---

## Relation to removed `string_escape`

Python 2’s **`string_escape`** codec was removed in Python 3. For **text**, use [`unicode_escape`](text-encodings/index.md); for **raw bytes**, use these standalone functions or `codecs.decode(..., 'unicode_escape')` on appropriately encoded data.

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`repr(bytes)`** in logs | Readable and idiomatic |
| Use **`escape_encode`** when you need bytes output without quotes | Same escapes, no `b''` wrapper |
| Round-trip through **`escape_decode`** only on trusted escaped input | Not a security boundary |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Looking up **`escape`** in registry | Not a named codec |
| Expecting **`errors`** on encode | Documented as ignored |
| Mixing with **`unicode_escape`** on str | Different types and rules |
