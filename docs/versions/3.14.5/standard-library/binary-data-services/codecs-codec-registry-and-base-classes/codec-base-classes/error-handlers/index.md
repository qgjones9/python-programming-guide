# [Error Handlers](https://docs.python.org/3/library/codecs.html#error-handlers)

Codec operations accept an **`errors`** argument naming how to react when a character cannot be encoded or a byte sequence is invalid. Python ships built-in handlers (implemented as `codecs.strict_errors`, `replace_errors`, …) and lets you **`register_error()`** for custom names. Full semantics remain on [docs.python.org](https://docs.python.org/3/library/codecs.html#error-handlers).

---

## Standard handlers (encoding and decoding)

| Value | On encode | On decode |
|-------|-----------|-----------|
| `'strict'` | Raise `UnicodeEncodeError` (default) | Raise `UnicodeDecodeError` |
| `'ignore'` | Drop unencodable characters | Skip malformed bytes |
| `'replace'` | Insert `?` (ASCII) | Insert U+FFFD (�) |
| `'backslashreplace'` | `\x`, `\u`, `\U` escapes | `\xhh` per bad byte |
| `'surrogateescape'` | N/A for most encoders | Map bytes 0x80–0xFF to U+DC80–U+DCFF (PEP 383) |

```python
# Goal: compare strict vs replace on encode
import codecs

text = "a\u2665b"
strict_failed = False
try:
    text.encode("ascii", errors="strict")
except UnicodeEncodeError:
    strict_failed = True
assert strict_failed
assert text.encode("ascii", errors="replace") == b"a?b"
```

```python
# Goal: surrogateescape round-trip for arbitrary bytes as str
import codecs

raw = b"file\xffname"
s = raw.decode("ascii", errors="surrogateescape")
round_trip = s.encode("ascii", errors="surrogateescape")
assert round_trip == raw
```

---

## Encoding-only handlers

| Value | Effect |
|-------|--------|
| `'xmlcharrefreplace'` | Replace with `&#...;` numeric character references |
| `'namereplace'` | Replace with `\N{UNICODE NAME}` escapes (3.5+) |

```python
# Goal: XML-safe ASCII fallback
import codecs

out = "Price: \u20ac".encode("ascii", errors="xmlcharrefreplace")
assert b"&#8364;" in out
```

---

## Codec-specific handlers

| Value | Codecs | Effect |
|-------|--------|--------|
| `'surrogatepass'` | utf-8, utf-16*, utf-32* | Allow surrogate code points U+D800–U+DFFF through encode/decode |

Use `'surrogatepass'` only when you intentionally handle UTF-16 data containing surrogate pairs as raw code units.

---

## Custom error handlers

`codecs.register_error(name, handler)` binds a callable invoked with `UnicodeEncodeError`, `UnicodeDecodeError`, or `UnicodeTranslateError`. The handler must **raise** or return `(replacement, new_index)` where `replacement` is `str` or `bytes`.

| Function | Role |
|----------|------|
| `codecs.register_error(name, handler)` | Install named handler |
| `codecs.lookup_error(name)` | Retrieve handler (raises `LookupError` if missing) |

```python
# Goal: minimal custom handler that skips one bad code point
import codecs

def skip_one(exc):
    if not isinstance(exc, UnicodeEncodeError):
        raise exc
    return ("", exc.start + 1)

codecs.register_error("skipone", skip_one)
out = "a\u2665b".encode("ascii", errors="skipone")
assert out == b"ab"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Default to **`strict`** for untrusted input | Silent replacement hides attacks and data loss |
| Use **`surrogateescape`** for filesystem APIs on Unix | Preserves opaque byte paths in `str` |
| Use **`backslashreplace`** for debug logs | Human-readable without losing information |
| Avoid **`ignore`** in production pipelines | Length and checksum drift |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| `'surrogateescape'` on wire formats | Meant for OS interfaces, not JSON/HTTP |
| Changing `errors` mid-stream on incremental codec | Set on constructor; attribute is mutable but confusing |
| Assuming `'namereplace'` works on decode | Encoding-only handler |
