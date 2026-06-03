# [encodings — Encodings package](https://docs.python.org/3/library/codecs.html#module-encodings)

The **`encodings`** package is the implementation home for most standard codecs. **`codecs.lookup()`** normalizes names, searches aliases, imports `encodings.<name>`, and caches `CodecInfo` from each module’s **`getregentry()`**. Application code should call **`codecs.lookup()`**, not import search functions directly—except for tests. Reference: [docs.python.org](https://docs.python.org/3/library/codecs.html#module-encodings).

---

## Public helpers

| Function | Role |
|----------|------|
| `encodings.normalize_encoding(encoding)` | Collapse punctuation to underscores; strip edges |
| `encodings.search_function(encoding)` | Default registry search (imports submodules) |
| `encodings.win32_code_page_search_function(encoding)` | `cpXXXX` Windows pages (3.14+) |

```python
# Goal: normalization rules
from encodings import normalize_encoding

assert normalize_encoding("utf-8") == "utf_8"
assert normalize_encoding("ISO-8859-1") == "ISO_8859_1"
```

```python
# Goal: lookup uses normalization internally
import codecs

assert codecs.lookup("UTF-8").name == "utf-8"
assert codecs.lookup("iso-8859-1").name == "iso8859-1"
```

---

## Module contract

Each `encodings/*.py` module may define:

| Symbol | Purpose |
|--------|---------|
| `getregentry()` | Return `codecs.CodecInfo` |
| `getaliases()` | Optional list of extra alias strings |

Invalid modules raise **`encodings.CodecRegistryError`** during registration.

---

## win32_code_page_search_function (3.14+)

On Windows, dynamic **`cp1252`**, **`cp437`**, etc. can register without a static module file. On all platforms, upstream documents expanded availability—still prefer **`utf-8`** for portable files.

---

## Best practices

| Practice | Why |
|----------|-----|
| Never **`import encodings.foo`** for encoding user data | Use `codecs.lookup` |
| Add custom codecs via **`codecs.register`** or new `encodings` submodule | Keeps cache coherent |
| Call **`codecs.unregister`** in test teardown | Clears registry cache |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Calling **`search_function`** directly | Bypasses cache semantics |
| Non-ASCII **`normalize_encoding`** input | Documented ASCII-only |
| Stale cache after **`register`** | Registry clears on register/unregister |

---

## Related notes in this repo

| Module | Topic |
|--------|-------|
| [encodings.idna](../encodings-idna/index.md) | IDNA implementation |
| [encodings.mbcs](../encodings-mbcs/index.md) | Windows ANSI |
| [encodings.utf_8_sig](../encodings-utf-8-sig/index.md) | UTF-8 BOM variant |
