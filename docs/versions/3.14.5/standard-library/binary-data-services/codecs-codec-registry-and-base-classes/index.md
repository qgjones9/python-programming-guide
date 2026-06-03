# [codecs — Codec registry and base classes](https://docs.python.org/3/library/codecs.html)

The [`codecs`](https://docs.python.org/3/library/codecs.html) module is Python’s **codec infrastructure**: a global registry of encoders/decoders, standardized error handlers, and base classes for stateless, incremental, and stream-oriented transforms. Most day-to-day text work uses `str.encode` / `bytes.decode`, which delegate here; you call `codecs` directly when registering custom codecs, streaming chunks, or applying binary transforms (base64, hex, zlib). Full API details remain on [docs.python.org](https://docs.python.org/3/library/codecs.html).

---

## Registry and lookup — [Module contents](https://docs.python.org/3/library/codecs.html#module-contents)

| Function | Returns |
|----------|---------|
| `codecs.encode(obj, encoding='utf-8', errors='strict')` | Encoded object (usually `bytes`) |
| `codecs.decode(obj, encoding='utf-8', errors='strict')` | Decoded object (usually `str`) |
| `codecs.lookup(encoding)` | `CodecInfo` with encode/decode factories |
| `codecs.getencoder(encoding)` / `getdecoder(encoding)` | Stateless callables |
| `codecs.getincrementalencoder(encoding)` / `getincrementaldecoder(encoding)` | Incremental classes |
| `codecs.getreader(encoding)` / `getwriter(encoding)` | Stream wrapper classes |
| `codecs.register(search_function)` | Add a custom codec search hook |
| `codecs.unregister(search_function)` | Remove hook and clear cache (3.10+) |

Encoding names are normalized: hyphens and spaces become underscores, case is ignored.

```python
# Goal: inspect a registered codec
import codecs

info = codecs.lookup("utf-8")
assert info.name == "utf-8"
text, _ = info.encode("hello")
assert text == b"hello"
```

```python
# Goal: register a trivial identity bytes codec for teaching
import codecs

def search(name):
    if name == "identity_bytes":
        return codecs.CodecInfo(
            name="identity_bytes",
            encode=lambda o, e="strict": (bytes(o), len(o)),
            decode=lambda o, e="strict": (bytes(o), len(o)),
        )
    return None

codecs.register(search)
raw = codecs.encode(b"data", "identity_bytes")
assert raw == b"data"
codecs.unregister(search)
```

---

## CodecInfo — [CodecInfo](https://docs.python.org/3/library/codecs.html#codecs.CodecInfo)

`codecs.lookup()` returns a `CodecInfo` object bundling the factories a codec implements. Not every codec provides all interfaces (for example `rot_13` has no incremental decoder).

| Attribute | Role |
|-----------|------|
| `name` | Canonical encoding name |
| `encode` / `decode` | Stateless callables `(input, errors='strict') → (output, length)` |
| `incrementalencoder` / `incrementaldecoder` | Factory for chunked codecs |
| `streamwriter` / `streamreader` | Factory for file-like wrappers |

See [Codec Base Classes](codec-base-classes/index.md) for the method contracts each factory must satisfy.

```python
# Goal: compare stateless vs incremental UTF-8 paths
import codecs

info = codecs.lookup("utf-8")
whole, _ = info.encode("naïve")
inc = info.incrementalencoder()
parts = inc.encode("na") + inc.encode("ïve", final=True)
assert whole == parts
```

---

## Utility helpers

| Function | Role |
|----------|------|
| `codecs.iterencode(iterator, encoding, errors='strict')` | Incrementally encode `str` chunks from an iterator |
| `codecs.iterdecode(iterator, encoding, errors='strict')` | Incrementally decode `bytes` chunks |
| `codecs.open(filename, mode='r', encoding=None, errors='strict')` | `StreamReaderWriter` around a binary file (**deprecated 3.14** — use `open(encoding=...)`) |
| `codecs.EncodedFile(file, data_encoding, file_encoding=None, errors='strict')` | Transcode between two encodings via `StreamRecoder` |
| `codecs.charmap_build(string)` | Build a 256-char → byte mapping for custom charmap codecs |
| `codecs.readbuffer_encode(buffer, errors=None)` | Return `(bytes, length)` for buffer protocol objects |

```python
# Goal: incremental encode without loading entire text
import codecs

chunks = list(codecs.iterencode(iter(["ab", "cd"]), "utf-8"))
assert b"".join(chunks) == b"abcd"
```

```python
# Goal: readbuffer_encode for buffer-protocol objects
import codecs

raw, length = codecs.readbuffer_encode(b"Zito")
assert raw == b"Zito" and length == 4
```

```python
# Goal: build a custom single-byte charmap table
import codecs

# ordinals 0–255 map to themselves for this demo
table = "".join(chr(i) for i in range(256))
mapping = codecs.charmap_build(table)
assert len(table) == 256 and mapping is not None
```

---

## BOM constants

| Constant | Meaning |
|----------|---------|
| `codecs.BOM_UTF8` | UTF-8 signature bytes |
| `codecs.BOM_UTF16` / `BOM_UTF16_BE` / `BOM_UTF16_LE` | UTF-16 BOM variants |
| `codecs.BOM_UTF32` / `BOM_UTF32_BE` / `BOM_UTF32_LE` | UTF-32 BOM variants |
| `codecs.BOM` / `BOM_BE` / `BOM_LE` | UTF-16 BOM aliases (platform-dependent) |

Use these when detecting or emitting byte-order marks; prefer explicit UTF-8 without BOM for new formats.

```python
# Goal: detect UTF-8 BOM prefix
import codecs

payload = codecs.BOM_UTF8 + "hi".encode("utf-8")
assert payload.startswith(codecs.BOM_UTF8)
assert payload[len(codecs.BOM_UTF8) :].decode("utf-8") == "hi"
```

---

## Codec categories

| Category | Input → output | Examples |
|----------|----------------|----------|
| Text encodings | `str` ↔ `bytes` | `utf-8`, `latin-1`, `cp1252` |
| Binary transforms | `bytes` → `bytes` | `base64_codec`, `hex_codec`, `zlib_codec` |
| Text transforms | `str` → `str` | `rot_13` |
| Python-specific | Mixed | `unicode_escape`, [`idna`](encodings-idna/index.md), [`mbcs`](encodings-mbcs/index.md) (Windows) |

For wire-format packing of numeric fields (not text), use [`struct`](../struct-interpret-bytes-as-packed-binary-data/index.md) instead of a codec.

---

## Related modules

| Module | Relationship |
|--------|--------------|
| [`struct`](../struct-interpret-bytes-as-packed-binary-data/index.md) | Fixed-width binary layouts; complements byte transforms |
| [`bytes` / `bytearray` / `memoryview`](../../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) | Codec inputs/outputs for binary data |
| [`re`](../../text-processing-services/re-regular-expression-operations/index.md) | Pattern matching on `str` and `bytes` after decode |
| [Error handlers](codec-base-classes/error-handlers/index.md) | `strict`, `replace`, `surrogateescape`, and custom handlers |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`open(..., encoding='utf-8')`** for text files | Handles newlines; `codecs.open()` is deprecated |
| Keep **`errors='strict'`** for inbound data | Fail fast on mojibake |
| Use **`surrogateescape`** for undecodable OS paths (PEP 383) | Round-trip arbitrary bytes as `str` on Unix |
| Call **`lookup()` once**, reuse `CodecInfo` | Avoid repeated registry scans |
| Match **`iterencode` vs `iterdecode`** to codec direction | Bytes-to-bytes codecs cannot `iterdecode` str |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Assuming all aliases are optimized | CPython fast-paths only common names (`utf-8`, `latin-1`, …) |
| `iterdecode` on `rot_13` | Use `iterencode` for text-to-text |
| Custom search functions returning partial `CodecInfo` | Provide all required factories or `None` |
| Ignoring incremental **`final=True`** | Incomplete multibyte sequences at chunk boundaries need flush |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Codec Base Classes](codec-base-classes/index.md) | Error handlers, stateless/incremental/stream interfaces |
| [Encodings and Unicode](encodings-and-unicode/index.md) | How strings map to bytes, BOM, UTF variants |
| [Standard Encodings](standard-encodings/index.md) | Built-in charset catalog and aliases |
| [Python Specific Encodings](python-specific-encodings/index.md) | `unicode_escape`, base64, rot13, etc. |
| [encodings — Encodings package](encodings-encodings-package/index.md) | `normalize_encoding`, search functions |
| [encodings.idna](encodings-idna/index.md) | IDNA / punycode domain labels |
| [encodings.mbcs](encodings-mbcs/index.md) | Windows ANSI code page |
| [encodings.utf_8_sig](encodings-utf-8-sig/index.md) | UTF-8 with BOM on encode, strip on decode |
