# [zlib — Compression compatible with **gzip**](https://docs.python.org/3/library/zlib.html)

The [`zlib`](https://docs.python.org/3/library/zlib.html) module wraps the zlib library for **deflate compression**, **CRC32/Adler-32 checksums**, and optional **gzip-compatible headers** via the `wbits` parameter. Use it for protocol payloads and in-memory buffers; for `.gz` files prefer [`gzip`](../gzip-support-for-gzip-files/index.md). This is an optional module on some builds. Full option matrices remain on [docs.python.org](https://docs.python.org/3/library/zlib.html).

---

## One-shot API

| Function | Role |
|----------|------|
| `compress(data, level=-1, wbits=15)` | Return compressed `bytes` |
| `decompress(data, wbits=15, bufsize=...)` | Return original `bytes` |
| `crc32(data, value=0)` | 32-bit CRC checksum (unsigned) |
| `adler32(data, value=1)` | Faster checksum for streams |

`level` ranges from `0` (`Z_NO_COMPRESSION`) through `9` (`Z_BEST_COMPRESSION`); `-1` is default.

---

## Incremental objects

| Factory | Methods / attrs |
|---------|-----------------|
| `compressobj(...)` | `compress()`, `flush(mode=Z_FINISH)`, `copy()` |
| `decompressobj(wbits=15)` | `decompress()`, `flush()`, `unused_data`, `unconsumed_tail`, `eof` |

Use incremental APIs when input arrives in chunks or exceeds available memory.

```python
# Goal: one-shot compress and verify CRC32
import zlib

payload = b"zlib works on bytes"
compressed = zlib.compress(payload, level=1)
restored = zlib.decompress(compressed)
checksum = zlib.crc32(payload) & 0xFFFFFFFF
assert restored == payload and zlib.crc32(restored) & 0xFFFFFFFF == checksum
```

```python
# Goal: stream compression with compressobj
import zlib

chunks = [b"part-a-", b"part-b"]
co = zlib.compressobj(level=1)
out = b"".join(co.compress(c) for c in chunks) + co.flush()
assert zlib.decompress(out) == b"".join(chunks)
```

```python
# Goal: incremental decompression with leftover handling
import zlib

raw = zlib.compress(b"hello world", level=1)
do = zlib.decompressobj()
first = do.decompress(raw[:5])
second = do.decompress(raw[5:]) + do.flush()
assert first + second == b"hello world"
assert do.unused_data == b""
```

---

## wbits cheat sheet

| wbits range | Meaning |
|-------------|---------|
| +9 … +15 | zlib header + trailer (default `MAX_WBITS=15`) |
| −9 … −15 | Raw deflate, no header/checksum |
| +25 … +31 | gzip header + trailer (`16 + window`) |
| +40 … +47 | Auto-detect zlib or gzip on decompress |

Mismatch between compress and decompress `wbits` raises `zlib.error`.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`gzip` module** for `.gz` files | Handles mtime, filename metadata, and edge cases |
| Reuse **`compressobj.copy()`** for shared prefixes | Saves re-initialization on similar streams |
| Mask CRC with **`& 0xFFFFFFFF`** on 32-bit hosts | Keeps checksums unsigned |
| Check **`decompressobj.eof`** for truncated streams | Distinguishes complete vs partial input |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Raw deflate with default `wbits` | Header expected on decompress | Pass negative `wbits` on both sides |
| Forgetting `flush(Z_FINISH)` | Truncated output stream | Always finish incremental compression |
| Using CRC/Adler for security | Not collision-resistant | Use `hashlib` for integrity guarantees |

---

## See also

- [gzip](../gzip-support-for-gzip-files/index.md) — `.gz` file interface
- [Data Compression and Archiving hub](../index.md)
