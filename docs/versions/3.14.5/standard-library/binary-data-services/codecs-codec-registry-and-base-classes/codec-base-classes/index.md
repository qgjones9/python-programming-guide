# [Codec Base Classes](https://docs.python.org/3/library/codecs.html#codec-base-classes)

Every codec registered in Python exposes up to **four interfaces**: stateless encode/decode, incremental encoder/decoder (chunked input with memory), and stream reader/writer (file-like I/O). The [`codecs`](https://docs.python.org/3/library/codecs.html#codec-base-classes) module defines abstract base classes and error-handler registration shared by all standard encodings. Full method contracts remain on [docs.python.org](https://docs.python.org/3/library/codecs.html#codec-base-classes).

---

## Interface map

| Interface | Base class | Stateful? | Typical use |
|-----------|------------|-----------|-------------|
| Stateless encode/decode | `codecs.Codec` | No | `codecs.encode`, one-shot buffers |
| Incremental | `IncrementalEncoder`, `IncrementalDecoder` | Yes | Network chunks, `iterencode` |
| Stream writer | `StreamWriter` | Yes | Writing encoded bytes to binary files |
| Stream reader | `StreamReader` | Yes | Reading decoded text from binary files |

A `CodecInfo` object bundles factory callables for whichever interfaces a codec implements.

```python
# Goal: pick the right factory from CodecInfo
import codecs

info = codecs.lookup("utf-8")
dec = info.incrementalencoder()
part1 = dec.encode("caf")
part2 = dec.encode("é", final=True)
assert part1 + part2 == "café".encode("utf-8")
```

---

## Error handling across interfaces

All interfaces accept an `errors` string (default `'strict'`). Handlers can be registered with `codecs.register_error()` and looked up via `codecs.lookup_error()`. See [Error Handlers](error-handlers/index.md) for the full table.

```python
# Goal: swap error strategy on an incremental encoder
import codecs

enc = codecs.getincrementalencoder("ascii")(errors="replace")
out = enc.encode("a\u2665b", final=True)
assert out == b"a?b"
```

---

## Designing custom codecs

| Requirement | Detail |
|-------------|--------|
| Stateless methods | Must not retain state between calls; handle empty input |
| Incremental objects | Must support `reset()`, optional `getstate()` / `setstate()` |
| Stream objects | Delegate unknown attributes to underlying stream |
| Registry entry | `getregentry()` in `encodings.*` modules returns `CodecInfo` |

Custom codecs register through `codecs.register()` or by adding a module under the [`encodings`](../encodings-encodings-package/index.md) package.

---

## Best practices

| Practice | Why |
|----------|-----|
| Implement **incremental** APIs for multibyte encodings | Single-byte charsets can wrap stateless functions |
| Stream **`reset()`** without seeking | Recover from decode errors without repositioning file |
| Document which **`errors`** values your codec supports | `surrogatepass` is UTF-specific |
| Reuse stateless encode/decode inside stream classes | Matches how `encodings.utf_8` is structured |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Error Handlers](error-handlers/index.md) | `strict`, `replace`, `surrogateescape`, custom handlers |
| [Stateless Encoding and Decoding](stateless-encoding-and-decoding/index.md) | `Codec.encode` / `Codec.decode` contract |
| [Incremental Encoding and Decoding](incremental-encoding-and-decoding/index.md) | Chunked processing with `final` flag |
| [Stream Encoding and Decoding](stream-encoding-and-decoding/index.md) | `StreamReader`, `StreamWriter`, wrappers |
