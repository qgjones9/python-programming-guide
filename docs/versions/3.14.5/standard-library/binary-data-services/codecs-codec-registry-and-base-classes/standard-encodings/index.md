# [Standard Encodings](https://docs.python.org/3/library/codecs.html#standard-encodings)

Python ships dozens of **built-in text encodings**—implemented in C or via charmap tables in the [`encodings`](encodings-encodings-package/index.md) package. Names are looked up through `codecs.lookup()` with alias normalization. The complete alias list lives in upstream `encodings/aliases.py`; this page highlights categories and portability rules from [docs.python.org](https://docs.python.org/3/library/codecs.html#standard-encodings).

---

## Always-available encodings (non-Windows)

These codecs are guaranteed on **all platforms** (per upstream table note):

| Codec | Aliases (sample) | Notes |
|-------|------------------|-------|
| `ascii` | `646`, `us-ascii` | 7-bit; strict for high code points |
| `latin_1` | `iso-8859-1`, `latin1`, `8859` | Western Europe; U+00FF max |
| `utf_8` | `utf8`, `utf-8`, `cp65001` | Default for modern text |
| `utf_16` / `utf_16_be` / `utf_16_le` | `utf16`, … | BOM-aware / explicit endian |
| `utf_32` / `utf_32_be` / `utf_32_le` | `utf32`, … | Same |
| `utf_7` | `unicode-1-1-utf-7` | Legacy mail |
| `utf_8_sig` | — | UTF-8 + BOM; see dedicated note |

```python
# Goal: verify portable encodings register
import codecs

for name in ("ascii", "latin_1", "utf_8", "utf_16", "utf_32"):
    info = codecs.lookup(name)
    assert info.encode is not None and info.decode is not None
```

---

## Windows code pages

Since **3.14**, `cpXXX` codecs may register for **all Windows code pages** via `win32_code_page_search_function`. On other platforms, only documented `cp*` entries from the standard table are guaranteed.

| Codec | Region / script |
|-------|-----------------|
| `cp1252` | Western Europe (Windows) |
| `cp1251` | Cyrillic |
| `cp932` / `shift_jis` | Japanese |
| `cp949` | Korean |
| `cp950` | Traditional Chinese |

```python
# Goal: encode Western European text with cp1252 when available
import codecs

text = "Euro €"
try:
    out = text.encode("cp1252")
except UnicodeEncodeError:
    out = text.encode("latin-1", errors="replace")
assert isinstance(out, bytes)
```

---

## CJK and ISO families (sample)

| Codec | Languages |
|-------|-----------|
| `gb2312`, `gbk`, `gb18030` | Simplified / unified Chinese |
| `big5`, `big5hkscs` | Traditional Chinese |
| `euc_jp`, `euc_kr`, `shift_jis` | Japanese, Korean |
| `iso8859_2` … `iso8859_16` | Regional ISO 8859 variants |

European sets often exist in three flavors: **ISO 8859**, **Windows cp125x**, and **Mac** roman variants—code positions differ (e.g. Euro sign).

---

## CPython fast-path aliases

These names (case-insensitive, `-` ↔ `_`) may bypass generic lookup for speed:

`utf-8`, `utf8`, `latin-1`, `latin1`, `iso-8859-1`, `ascii`, `us-ascii`, `utf-16`, `utf-16-le`, `utf-16-be`, `utf-32`, …

Obscure aliases still work but may be slower.

```python
# Goal: alias normalization reaches same codec
import codecs

assert codecs.lookup("UTF-8").name == "utf-8"
assert codecs.lookup("iso8859-1").name == "iso8859-1"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Pin encoding in **file format docs** | `cp1252` ≠ `latin-1` for 0x80–0x9F |
| Use **`utf-8`** for new interchange | Cross-platform default |
| Test with **real data** from target locale | Fallback tables hide silent corruption |
| Check **`sys.getdefaultencoding()`** (UTF-8 since 3.0) | Differs from filesystem encodings |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Assuming **`cp1252` on Linux** | May exist but not be default |
| **`utf-16` surrogate** encoding (since 3.4) | Surrogates rejected unless `surrogatepass` |
| Decoding unknown bytes as **`latin-1`** “for safety” | Produces wrong characters, not errors |
