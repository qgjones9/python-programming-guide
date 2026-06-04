# [bz2 — Support for **bzip2** compression](https://docs.python.org/3/library/bz2.html)

The [`bz2`](https://docs.python.org/3/library/bz2.html) module provides **bzip2 compression** with one-shot helpers and file objects for `.bz2` files. bzip2 typically achieves **better compression than gzip** at the cost of **higher CPU and memory** use. The module is optional on minimal Python builds. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/bz2.html).

---

## API surface

| API | Role |
|-----|------|
| `compress(data, compresslevel=9)` | One-shot compression to `bytes` |
| `decompress(data)` | One-shot decompression |
| `open(filename, mode='rb', compresslevel=9, encoding=None, ...)` | File wrapper (binary or text) |
| `BZ2File(filename, mode='r', compresslevel=9)` | Underlying binary file object |
| `BZ2Compressor(9)` | Incremental compression (level is positional, 1–9) |
| `BZ2Decompressor()` | Incremental decompression |

`compresslevel` ranges from `1` (fastest) to `9` (best compression).

```python
# Goal: one-shot bzip2 round-trip
import bz2

text = b"bzip2 favors redundant text payloads"
wire = bz2.compress(text, compresslevel=1)
assert bz2.decompress(wire) == text
```

```python
# Goal: write and read a .bz2 text file
import bz2
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "notes.txt.bz2"
    with bz2.open(path, "wt", encoding="utf-8") as f:
        f.write("compressed notes\n")
    with bz2.open(path, "rt", encoding="utf-8") as f:
        assert "notes" in f.read()
```

```python
# Goal: incremental compression for chunked input
import bz2

comp = bz2.BZ2Compressor(1)
parts = [comp.compress(b"abc"), comp.compress(b"def"), comp.flush()]
blob = b"".join(parts)
assert bz2.decompress(blob) == b"abcdef"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **gzip or zstd** for hot paths | bzip2 is slower on small payloads |
| Use **`compresslevel=1`** when experimenting | Level 9 can be very slow on large inputs |
| Handle **`ModuleNotFoundError`** in portable tools | bz2 may be omitted by distributors |
| Stream with **`BZ2Compressor`** for large data | Avoids one giant `bytes` allocation |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Calling `compress()` after `flush()` on compressor | `ValueError` | Create a new `BZ2Compressor` |
| Mixing bzip2 and gzip extensions | Decompress fails mysteriously | Match file suffix to module |
| Small payload overhead | bzip2 block headers dominate | Use gzip/zlib for tiny blobs |

---

## See also

- [gzip](../gzip-support-for-gzip-files/index.md) — faster deflate wrapper
- [compression.zstd](../compressionzstd-compression-compatible-with-the-zstandard-format/index.md) — modern alternative
- [Data Compression and Archiving hub](../index.md)
