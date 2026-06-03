# [Encodings and Unicode](https://docs.python.org/3/library/codecs.html#encodings-and-unicode)

Python `str` objects hold Unicode code points (U+0000–U+10FFFF); **text encodings** define how those sequences serialize to **bytes** for storage, wire transfer, or C APIs. Decoding reverses the mapping. This page summarizes encoding families, BOM behavior, and detection limits—full narrative on [docs.python.org](https://docs.python.org/3/library/codecs.html#encodings-and-unicode).

---

## Encoding families

| Family | Code point coverage | Typical use |
|--------|---------------------|-------------|
| **Single-byte** (`latin-1`, `cp1252`, …) | Up to 256 characters per charset | Legacy Western European, charmap files |
| **UTF-8** | Full Unicode | Web, JSON, modern files |
| **UTF-16 / UTF-32** | Full Unicode | Windows APIs, some binary formats |
| **Multibyte CJK** (`gbk`, `shift_jis`, …) | Large Asian charsets | Regional legacy data |

`latin-1` maps U+0000–U+00FF to bytes 0x00–0xFF one-to-one; code points above U+00FF raise `UnicodeEncodeError`.

```python
# Goal: latin-1 bijection for first 256 code points
assert "\xff".encode("latin-1") == b"\xff"
assert b"\xff".decode("latin-1") == "\xff"
try:
    "\u0100".encode("latin-1")
except UnicodeEncodeError:
    ok = True
else:
    ok = False
assert ok
```

---

## UTF-8 structure (summary)

| Code point range | Byte pattern |
|------------------|--------------|
| U+0000–U+007F | `0xxxxxxx` |
| U+0080–U+07FF | `110xxxxx 10xxxxxx` |
| U+0800–U+FFFF | `1110xxxx 10xxxxxx 10xxxxxx` |
| U+10000–U+10FFFF | `11110xxx` + three continuation bytes |

UTF-8 has **no endianness** issue; invalid byte sequences fail decode under `'strict'`.

```python
# Goal: UTF-8 multibyte encoding and strict decode failure
assert "é".encode("utf-8") == b"\xc3\xa9"
failed = False
try:
    b"\xff\xfe".decode("utf-8", errors="strict")
except UnicodeDecodeError:
    failed = True
assert failed
```

---

## BOM and endianness

| Encoding | BOM bytes | Endianness |
|----------|-----------|------------|
| UTF-8 | EF BB BF (optional; discouraged) | N/A |
| UTF-16 | FE FF (BE) or FF FE (LE) | Declared by BOM |
| UTF-32 | 00 00 FE FF / FF FE 00 00 | Declared by BOM |

Python’s UTF-16/32 codecs use **native** endianness when no BOM is present. U+FEFF as BOM is stripped on decode; as ZWNBSP it remains in the string.

```python
# Goal: UTF-16 LE with BOM
import codecs

raw = codecs.BOM_UTF16_LE + "A".encode("utf-16-le")
assert raw.decode("utf-16") == "A"
```

---

## Detection limits

| Fact | Implication |
|------|-------------|
| Any byte sequence is valid **latin-1** | Heuristics cannot prove latin-1 vs binary |
| **UTF-8** rejects many random byte patterns | Stronger validation than single-byte charsets |
| **`utf-8-sig`** strips EF BB BF on decode | Helps Notepad-style files; see [utf_8_sig](../encodings-utf-8-sig/index.md) |

Without metadata (HTTP `charset`, file spec), prefer **explicit encoding** at API boundaries.

---

## Best practices

| Practice | Why |
|----------|-----|
| Standardize on **UTF-8** for new text | Full Unicode, no endianness |
| Normalize with **`unicodedata`** before compare | See [unicodedata](../../text-processing-services/unicodedata-unicode-database/index.md) |
| Treat **BOM** as format metadata, not content | Strip or preserve consistently |
| Never guess encoding for **security-critical** parsing | Use declared charset |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Using **`latin-1`** as “binary in str” | Only U+00FF and below round-trip |
| Mixing UTF-16 LE/BE without BOM | Specify `utf-16-le` / `utf-16-be` |
| Assuming **`utf-8-sig`** on wire protocols | BOM is for file detection, not HTTP |
