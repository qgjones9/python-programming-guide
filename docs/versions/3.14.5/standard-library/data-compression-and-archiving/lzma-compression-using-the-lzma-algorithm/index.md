# [lzma — Compression using the LZMA algorithm](https://docs.python.org/3/library/lzma.html)

The [`lzma`](https://docs.python.org/3/library/lzma.html) module compresses and decompresses data with the **LZMA** algorithm, including **`.xz`** containers and legacy **`.lzma`** streams. The API parallels [`gzip`](../gzip-support-for-gzip-files/index.md) and [`bz2`](../bz2-support-for-bzip2-compression/index.md): file objects, one-shot helpers, and incremental compressor classes. **`LZMAFile` is not thread-safe** — guard shared instances with a lock. Full filter-chain and preset documentation is on [docs.python.org](https://docs.python.org/3/library/lzma.html).

**Optional module.** Requires liblzma at build time.

Related: [`compression.lzma`](../the-compression-package/index.md) (3.14+); [`tarfile`](../tarfile-read-and-write-tar-archive-files/index.md) modes `'r:xz'` / `'w:xz'`; [`zipfile`](../zipfile-work-with-zip-archives/index.md) `ZIP_LZMA`.

---

## API surface — overview

| Layer | Types / functions | Use when |
|-------|-------------------|----------|
| File I/O | `open()`, `LZMAFile` | Read/write `.xz` or `.lzma` files |
| One-shot | `compress()`, `decompress()` | Whole buffer; multi-stream concat on decompress |
| Incremental | `LZMACompressor`, `LZMADecompressor` | Streaming pipelines |
| Filters | `filters=` list of dicts | Custom LZMA2 / delta / BCJ chains |

---

## Formats and integrity — [Reading and writing compressed files](https://docs.python.org/3/library/lzma.html#reading-and-writing-compressed-files)

| Format constant | Container | Integrity checks |
|-----------------|-----------|------------------|
| `FORMAT_XZ` | `.xz` (default) | CRC64 default; optional SHA256 |
| `FORMAT_ALONE` | Legacy `.lzma` | No checks |
| `FORMAT_RAW` | Raw LZMA2 stream | Requires explicit `filters`; no auto-detect |
| `FORMAT_AUTO` | Decompress only | Detects `.xz` or `.lzma` |

| Check constant | Meaning |
|----------------|---------|
| `CHECK_NONE` | No check (required for ALONE/RAW) |
| `CHECK_CRC32` / `CHECK_CRC64` / `CHECK_SHA256` | Verified on decompress |

---

## Presets and memory — [LZMACompressor](https://docs.python.org/3/library/lzma.html#lzma.LZMACompressor)

| Preset | Trade-off |
|--------|-----------|
| `0`–`9` | Higher → smaller output, slower compression |
| `PRESET_EXTREME` (OR with preset) | Even slower; marginal gains |
| Default | `PRESET_DEFAULT` (6) |

Preset **9** can use **hundreds of MiB** of RAM during compression and decompression — avoid on memory-constrained hosts.

```python
# Goal: one-shot XZ round trip
import lzma

data = b"Insert Data Here\n" * 50
compressed = lzma.compress(data, preset=6)
assert lzma.decompress(compressed) == data
```

```python
# Goal: incremental compression with flush
import lzma

lzc = lzma.LZMACompressor(preset=3)
parts = [
    lzc.compress(b"Some data\n"),
    lzc.compress(b"Another piece\n"),
    lzc.flush(),
]
assert lzma.decompress(b"".join(parts)) == b"Some data\nAnother piece\n"
```

```python
# Goal: custom filter chain (delta + LZMA2)
import lzma

filters = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 5},
]
blob = lzma.compress(b"blah blah blah\n" * 20, filters=filters)
assert lzma.decompress(blob) == b"blah blah blah\n" * 20
```

---

## Incremental decompression — [LZMADecompressor](https://docs.python.org/3/library/lzma.html#lzma.LZMADecompressor)

| Attribute | Role |
|-----------|------|
| `eof` | End-of-stream reached |
| `unused_data` | Bytes after stream end |
| `needs_input` | Whether more input is required |
| `check` | Integrity check ID once known (`CHECK_UNKNOWN` until parsed) |

`LZMADecompressor` handles **one stream** only; use `decompress()` or `LZMAFile` for concatenated inputs. Pass `memlimit=` to cap decompressor memory.

---

## Choosing lzma vs alternatives

| Criterion | lzma | [`gzip`](../gzip-support-for-gzip-files/index.md) | [`bz2`](../bz2-support-for-bzip2-compression/index.md) |
|-----------|------|-------------------------------------------------|-----------------------------------------------------|
| Ratio | Best (slowest at high presets) | Moderate | Good |
| `.xz` tooling | `xz` utility, many packagers | N/A | N/A |
| Filter chains | Delta, BCJ, LZMA2 | No | No |
| Typical use | Release tarballs, long-term storage | Logs, HTTP | `.tar.bz2` legacy |

---

## Best practices

| Practice | Why |
|----------|-----|
| Default to **preset 6** unless profiling says otherwise | Balance of size and CPU |
| Use **`memlimit`** on untrusted decompress input | Prevents decompression bombs |
| Prefer **`FORMAT_XZ`** for new files | Integrity checks and multi-filter support |
| Use **`open()` / context managers** | Ensures trailers flush |
| Call **`is_check_supported()`** before exotic checks | CRC64/SHA256 may be absent in minimal liblzma builds |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`LZMADecompressor` on multi-stream data** | Stops after first stream | Use `lzma.decompress()` or new decompressor per stream |
| **Preset 9 on small embedded targets** | OOM or thrashing | Lower preset or use gzip/zstd |
| **`FORMAT_RAW` without matching `filters`** | `LZMAError` on decompress | Document filter chain both ways |
| **Shared `LZMAFile` without lock** | Corrupted reads/writes | One thread per file object |
| **`preset` and `filters` together** | Conflicting options | Use filters OR preset, per API docs |

---

## See also

| Resource | Link |
|----------|------|
| bzip2 counterpart | [`bz2`](../bz2-support-for-bzip2-compression/index.md) |
| Tar with xz compression | [`tarfile`](../tarfile-read-and-write-tar-archive-files/index.md) |
| Custom filter chains | [Specifying custom filter chains](https://docs.python.org/3/library/lzma.html#specifying-custom-filter-chains) |
| Section hub | [Data Compression and Archiving](../index.md) |
