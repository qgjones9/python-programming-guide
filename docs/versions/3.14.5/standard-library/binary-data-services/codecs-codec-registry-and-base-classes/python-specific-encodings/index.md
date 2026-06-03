# [Python Specific Encodings](https://docs.python.org/3/library/codecs.html#python-specific-encodings)

Beyond standard charsets, Python registers **codec names meaningful only in Python**: pickle escapes, IDNA, Windows ANSI/OEM, binary transforms (base64, hex, zlib), and the **`rot_13`** cipher. They plug into the same `codecs` registry but target different input/output types. Overview tables on [docs.python.org](https://docs.python.org/3/library/codecs.html#python-specific-encodings).

---

## By transform direction

| Direction | Section | Examples |
|-----------|---------|----------|
| `str` → `bytes` | [Text Encodings](text-encodings/index.md) | `unicode_escape`, `idna`, `mbcs` |
| `bytes` → `bytes` | [Binary Transforms](binary-transforms/index.md) | `base64_codec`, `hex_codec`, `zlib_codec` |
| `str` → `str` | [Text Transforms](text-transforms/index.md) | `rot_13` |
| Standalone helpers | [Standalone Codec Functions](standalone-codec-functions/index.md) | `escape_encode`, `escape_decode` |

Asymmetric codecs document encoding direction in upstream tables.

```python
# Goal: route by output type
import codecs

assert isinstance(codecs.encode("ab", "rot_13"), str)
assert isinstance(codecs.encode(b"ab", "hex"), bytes)
assert isinstance("x".encode("unicode_escape"), bytes)
```

---

## When to use Python-specific codecs

| Need | Codec |
|------|-------|
| Domain name ACE conversion | `idna` → [encodings.idna](../encodings-idna/index.md) |
| Windows ANSI bytes | `mbcs` → [encodings.mbcs](../encodings-mbcs/index.md) |
| Debug repr of bytes in logs | `unicode_escape` or `escape_encode` |
| Embed binary in ASCII protocols | `base64_codec`, `quopri_codec` |
| Obfuscation / puzzles | `rot_13` |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`base64` module** for strict RFC 4648 | Codec adds MIME newlines |
| Prefer **`idna` PyPI** for IDNA 2008 (RFC 5891) | Stdlib implements IDNA 2003 |
| Do not use **`undefined`** outside tests | Always raises |
| Call binary transforms via **`codecs.encode/decode`** | Not on `str.encode` |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Text Encodings](text-encodings/index.md) | `unicode_escape`, `raw_unicode_escape`, `idna`, … |
| [Binary Transforms](binary-transforms/index.md) | base64, hex, bz2, zlib, uu, quopri |
| [Standalone Codec Functions](standalone-codec-functions/index.md) | `escape_encode` / `escape_decode` |
| [Text Transforms](text-transforms/index.md) | `rot_13` |
