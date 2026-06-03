# [encodings.mbcs — Windows ANSI codepage](https://docs.python.org/3/library/codecs.html#module-encodings.mbcs)

**`encodings.mbcs`** implements the **ANSI code page (CP_ACP)** on Windows—the “system default” narrow charset for many legacy APIs. Aliases: **`mbcs`**, **`ansi`**, **`dbcs`**. On other platforms the codec exists but maps to a portable fallback behavior. Module notes on [docs.python.org](https://docs.python.org/3/library/codecs.html#module-encodings.mbcs).

---

## Behavior history

| Version | Error handling |
|---------|----------------|
| Before 3.2 | Encode: `'replace'`; decode: `'ignore'` (fixed) |
| 3.3+ | Any standard **`errors`** handler honored |

Encoding/decoding follows the **active Windows ANSI code page** (e.g. cp1252 on US English systems).

```python
# Goal: mbcs on Windows; latin-1 stand-in elsewhere for ASCII round-trip
import codecs
import sys

name = "mbcs" if sys.platform == "win32" else "latin-1"
info = codecs.lookup(name)
text = "hello"
encoded, _ = info.encode(text)
assert isinstance(encoded, bytes)
assert info.decode(encoded)[0] == text
```

```python
# Goal: alias names resolve when mbcs is registered
import codecs
import sys

if sys.platform == "win32":
    assert codecs.lookup("ansi").name == "mbcs"
    assert codecs.lookup("dbcs").name == "mbcs"
else:
    # Teaching note: mbcs/ansi/dbcs are not registered on this platform
    assert codecs.lookup("latin-1").name == "iso8859-1"
```

---

## vs `oem` codec

| Codec | Windows code page |
|-------|-------------------|
| `mbcs` | CP_ACP (ANSI) |
| `oem` | CP_OEMCP (console / legacy) |

Use **`utf-8`** for new cross-platform files; reserve `mbcs` for interfacing with Windows narrow-char APIs.

---

## Best practices

| Practice | Why |
|----------|-----|
| Guard Windows-specific paths with **`sys.platform == 'win32'`** | Semantic charset varies |
| Prefer **`open(encoding='utf-8')`** for new scripts | Avoids locale code page |
| Document **`errors`** when reading legacy files | 3.3+ no longer forces replace/ignore |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Assuming **same bytes on all Windows machines** | ACP depends on locale |
| Using **`mbcs` on Linux** for Windows file semantics | Not identical to CP1252 |
| Confusing **`mbcs`** with **`utf-8`** default | Python 3 source/files default UTF-8 |
