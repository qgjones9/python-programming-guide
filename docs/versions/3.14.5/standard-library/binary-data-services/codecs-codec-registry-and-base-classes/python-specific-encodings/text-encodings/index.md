# [Text Encodings](https://docs.python.org/3/library/codecs.html#python-specific-encodings-text-encodings)

These codecs convert **`str` → `bytes`** (encode) and **bytes-like → `str`** (decode), like UTF-8—but implement Python-specific or platform-specific semantics. Catalog on [docs.python.org](https://docs.python.org/3/library/codecs.html#python-specific-encodings-text-encodings).

---

## Codec reference

| Codec | Aliases | Meaning |
|-------|---------|---------|
| `idna` | — | RFC 3490 IDNA; strict errors only → [encodings.idna](../../encodings-idna/index.md) |
| `mbcs` | `ansi`, `dbcs` | Windows ANSI (CP_ACP) → [encodings.mbcs](../../encodings-mbcs/index.md) |
| `oem` | — | Windows OEM code page (3.6+) |
| `punycode` | — | RFC 3492; stateful codecs not supported |
| `unicode_escape` | — | `\uXXXX` / `\UXXXXXXXX` escapes (ASCII-safe repr style) |
| `raw_unicode_escape` | — | Like above but existing backslashes untouched (pickle) |
| `undefined` | — | Always raises (testing) |
| `palmos` | — | PalmOS 3.5 charset |

```python
# Goal: unicode_escape for ASCII-safe representation
s = "α".encode("unicode_escape").decode("ascii")
assert "\\u" in s or "\\x" in s
assert s.encode("ascii").decode("unicode_escape") == "α"
```

```python
# Goal: punycode label encoding (ASCII output)
import codecs

label = "bücher"
ascii_label = codecs.encode(label, "punycode").decode("ascii")
assert ascii_label.isascii()
assert codecs.decode(ascii_label.encode("ascii"), "punycode") == label
```

---

## unicode_escape vs raw_unicode_escape

| Codec | Backslashes in input |
|-------|----------------------|
| `unicode_escape` | Interpreted as escapes on decode |
| `raw_unicode_escape` | Left literal (pickle protocol compatibility) |

Source files default to **UTF-8** (PEP 3120)—do not assume `unicode_escape` matches file bytes.

```python
# Goal: raw_unicode_escape vs unicode_escape on decode
import codecs

assert codecs.decode(b"\\u03b1", "unicode_escape") == "\u03b1"
# raw_unicode_escape does not interpret \u as escape when doubled in source bytes
assert len(codecs.decode(b"\\\\x41", "raw_unicode_escape")) >= 1
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`idna` codec** for host labels in apps | Pairs with [socket](https://docs.python.org/3/library/socket.html) IDNA support |
| Guard **`mbcs` / `oem`** with platform checks | Meaningful on Windows |
| Prefer **`repr(bytes)`** or **`escape_encode`** for debug | Clearer than manual escapes |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| **`idna` with non-strict errors** | Only `'strict'` supported |
| **`undefined` in production** | Test-only codec |
| Confusing **`unicode_escape`** with UTF-8 file encoding | Different purposes |
