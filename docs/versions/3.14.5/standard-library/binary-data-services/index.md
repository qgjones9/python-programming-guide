# [Binary Data Services](https://docs.python.org/3/library/binary.html)

Python’s standard library groups **byte packing** and **codec-based transforms** under **Binary Data Services**. The [`struct`](struct-interpret-bytes-as-packed-binary-data/index.md) module maps Python values to C-compatible byte layouts; [`codecs`](codecs-codec-registry-and-base-classes/index.md) provides the registry, error handlers, and interfaces for text encodings, binary transforms, and stream wrappers. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/binary.html); this hub orients you to each module and when to reach for it.

Related material outside this section: built-in [`bytes`](../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md), file/network protocols elsewhere in the library, and text modules such as [`re`](../text-processing-services/re-regular-expression-operations/index.md) that also accept `bytes`.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`struct`](struct-interpret-bytes-as-packed-binary-data/index.md) | Pack/unpack fixed-width binary fields (headers, wire formats, C struct interchange) |
| [`codecs`](codecs-codec-registry-and-base-classes/index.md) | Encode/decode registry, error handlers, incremental and stream codec APIs |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Parse a fixed binary header or network packet | [`struct`](struct-interpret-bytes-as-packed-binary-data/index.md) with explicit endianness (`<`, `>`, `!`) |
| Convert text ↔ bytes (UTF-8, Latin-1, …) | [`codecs`](codecs-codec-registry-and-base-classes/index.md) or `str.encode` / `bytes.decode` |
| Stream large encoded files chunk-by-chunk | `codecs.getincrementaldecoder()` or `open(..., encoding=...)` |
| Base64, hex, zlib on raw bytes | [`binary transforms`](codecs-codec-registry-and-base-classes/python-specific-encodings/binary-transforms/index.md) via `codecs.encode` |
| Internationalized domain names | [`encodings.idna`](codecs-codec-registry-and-base-classes/encodings-idna/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Use **standard formats** (`<`, `>`, `!`) for wire/storage | Native `@` layout depends on CPU, compiler, and alignment |
| Call **`struct.calcsize()`** before slicing buffers | Prevents partial reads and silent misalignment |
| Prefer **`open(path, encoding='utf-8')`** over `codecs.open()` | `codecs.open()` is deprecated since 3.14 |
| Default to **`errors='strict'`** for untrusted input | Surrogate escapes and replacements hide data corruption |
| Reuse a compiled **`struct.Struct`** in hot loops | Format string is parsed once |
| Treat **BOM** encodings (`utf-8-sig`) as a detection aid, not a default | UTF-8 BOM is discouraged except for legacy Windows tools |

```python
# Goal: explicit endianness for a portable 32-bit header
import struct

magic, version, length = struct.unpack(">III", b"\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x0c")
assert (magic, version, length) == (1, 2, 12)
```

```python
# Goal: registry lookup with strict error handling
import codecs

encoded = codecs.encode("café", "utf-8", errors="strict")
assert codecs.decode(encoded, "utf-8") == "café"
```

```python
# Goal: combine struct headers with UTF-8 payload bytes
import codecs
import struct

header = struct.pack(">II", 0xCAFEBABE, 12)
payload = codecs.encode("hello", "utf-8")
blob = header + payload
magic, length = struct.unpack(">II", blob[:8])
text = codecs.decode(blob[8 : 8 + length], "utf-8")
assert magic == 0xCAFEBABE and text == "hello"
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Assuming `@` matches another machine | Wrong field offsets on decode | Document `<`/`>`/`!` in your protocol |
| Forgetting padding in standard mode | Shorter buffers than C peers expect | Insert explicit `'x'` pad bytes |
| Using `latin-1` for “binary-safe” Unicode | Code points U+0100+ cannot encode | Use UTF-8 or keep data as `bytes` |
| `iterdecode` on `rot_13` | Text-to-text codecs need `iterencode` | Match iterator element type to codec direction |
| Mixing BOM and non-BOM UTF-8 readers | Double-skipped or visible `\ufeff` | Pick one convention per file format |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [struct — Interpret bytes as packed binary data](struct-interpret-bytes-as-packed-binary-data/index.md) | Format strings, endianness, `Struct` objects |
| [codecs — Codec registry and base classes](codecs-codec-registry-and-base-classes/index.md) | Registry, BOM constants, utility helpers |
| [Codec Base Classes](codecs-codec-registry-and-base-classes/codec-base-classes/index.md) | Stateless, incremental, and stream interfaces |
| [Error Handlers](codecs-codec-registry-and-base-classes/codec-base-classes/error-handlers/index.md) | `strict`, `replace`, `surrogateescape`, custom handlers |
| [Stateless Encoding and Decoding](codecs-codec-registry-and-base-classes/codec-base-classes/stateless-encoding-and-decoding/index.md) | `Codec.encode` / `Codec.decode` contract |
| [Incremental Encoding and Decoding](codecs-codec-registry-and-base-classes/codec-base-classes/incremental-encoding-and-decoding/index.md) | Chunked processing with `final` flag |
| [IncrementalEncoder Objects](codecs-codec-registry-and-base-classes/codec-base-classes/incremental-encoding-and-decoding/incrementalencoder-objects/index.md) | `encode`, `reset`, `getstate` / `setstate` |
| [IncrementalDecoder Objects](codecs-codec-registry-and-base-classes/codec-base-classes/incremental-encoding-and-decoding/incrementaldecoder-objects/index.md) | `decode`, buffer flush, error recovery |
| [Stream Encoding and Decoding](codecs-codec-registry-and-base-classes/codec-base-classes/stream-encoding-and-decoding/index.md) | `StreamReader`, `StreamWriter`, wrappers |
| [StreamWriter Objects](codecs-codec-registry-and-base-classes/codec-base-classes/stream-encoding-and-decoding/streamwriter-objects/index.md) | `write`, `writelines`, `reset` |
| [StreamReader Objects](codecs-codec-registry-and-base-classes/codec-base-classes/stream-encoding-and-decoding/streamreader-objects/index.md) | `read`, `readline`, `readlines` |
| [StreamReaderWriter Objects](codecs-codec-registry-and-base-classes/codec-base-classes/stream-encoding-and-decoding/streamreaderwriter-objects/index.md) | Combined read/write wrapper (`codecs.open`) |
| [StreamRecoder Objects](codecs-codec-registry-and-base-classes/codec-base-classes/stream-encoding-and-decoding/streamrecoder-objects/index.md) | Transcoding between two encodings |
| [Encodings and Unicode](codecs-codec-registry-and-base-classes/encodings-and-unicode/index.md) | How strings map to bytes, BOM, UTF variants |
| [Standard Encodings](codecs-codec-registry-and-base-classes/standard-encodings/index.md) | Built-in charset catalog and aliases |
| [Python Specific Encodings](codecs-codec-registry-and-base-classes/python-specific-encodings/index.md) | `unicode_escape`, base64, rot13, etc. |
| [Text Encodings](codecs-codec-registry-and-base-classes/python-specific-encodings/text-encodings/index.md) | `unicode_escape`, `idna`, `mbcs`, punycode |
| [Binary Transforms](codecs-codec-registry-and-base-classes/python-specific-encodings/binary-transforms/index.md) | base64, hex, bz2, zlib, uu, quopri |
| [Standalone Codec Functions](codecs-codec-registry-and-base-classes/python-specific-encodings/standalone-codec-functions/index.md) | `escape_encode` / `escape_decode` |
| [Text Transforms](codecs-codec-registry-and-base-classes/python-specific-encodings/text-transforms/index.md) | `rot_13` |
| [encodings — Encodings package](codecs-codec-registry-and-base-classes/encodings-encodings-package/index.md) | `normalize_encoding`, search functions |
| [encodings.idna](codecs-codec-registry-and-base-classes/encodings-idna/index.md) | IDNA / punycode domain labels |
| [encodings.mbcs](codecs-codec-registry-and-base-classes/encodings-mbcs/index.md) | Windows ANSI code page |
| [encodings.utf_8_sig](codecs-codec-registry-and-base-classes/encodings-utf-8-sig/index.md) | UTF-8 with BOM on encode, strip on decode |
