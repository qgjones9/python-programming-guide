# [compression.zstd — Compression compatible with the Zstandard format](https://docs.python.org/3/library/compression.zstd.html)

Added in Python 3.14, [`compression.zstd`](https://docs.python.org/3/library/compression.zstd.html) wraps the **Zstandard (zstd)** algorithm for fast, high-ratio lossless compression. It supports **one-shot** `compress()` / `decompress()`, **streaming** `ZstdCompressor` / `ZstdDecompressor`, **`.zst` files** via `open()` and `ZstdFile`, and optional **trained dictionaries** (`train_dict()`, `ZstdDict`). The module is optional on some builds. Full parameter lists remain on [docs.python.org](https://docs.python.org/3/library/compression.zstd.html).

---

## API overview

| API | Role |
|-----|------|
| `compress(data, level=None, options=None, zstd_dict=None)` | One-shot compression |
| `decompress(data, zstd_dict=None, options=None)` | One-shot decompression |
| `open(file, mode='rb', level=None, ...)` | File wrapper (binary/text) |
| `ZstdFile` | Underlying `.zst` stream |
| `ZstdCompressor` / `ZstdDecompressor` | Incremental (de)compression |
| `train_dict(samples, dict_size)` | Build dictionary from sample corpus |
| `CompressionParameter` / `DecompressionParameter` | Advanced tuning enums |

`compression.zstd.ZstdError` is raised on malformed data or invalid parameters.

---

## When to choose zstd

| Compared to | zstd advantage |
|-------------|----------------|
| gzip/zlib | Often faster decompression at similar ratios |
| bzip2/lzma | Much faster compression with competitive size on many workloads |
| Custom | Standard `.zst` tooling interoperates with the `zstd` CLI |

```python
# Goal: one-shot zstd round-trip (Python 3.14+ with zstd support)
import importlib
import sys

if sys.version_info >= (3, 14):
    zstd = importlib.import_module("compression.zstd")
    payload = b"zstd targets speed and ratio together"
    wire = zstd.compress(payload, level=3)
    assert zstd.decompress(wire) == payload
```

```python
# Goal: write and read a .zst file via open()
import importlib
import sys
import tempfile
from pathlib import Path

if sys.version_info >= (3, 14):
    zstd = importlib.import_module("compression.zstd")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.zst"
        with zstd.open(path, "wb") as f:
            f.write(b"stored in zstandard format")
        with zstd.open(path, "rb") as f:
            assert f.read() == b"stored in zstandard format"
```

```python
# Goal: streaming compression with ZstdCompressor
import importlib
import sys

if sys.version_info >= (3, 14):
    zstd = importlib.import_module("compression.zstd")
    comp = zstd.ZstdCompressor(level=1)
    chunks = [comp.compress(b"hel"), comp.compress(b"lo"), comp.flush()]
    blob = b"".join(chunks)
    assert zstd.decompress(blob) == b"hello"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`level=3`** as a balanced default | Official docs cite good speed/ratio trade-off |
| Train **dictionaries** for repetitive small records | Amortizes header cost across many similar messages |
| Guard imports with **`ModuleNotFoundError`** | Optional module may be absent |
| Prefer **`open()` context managers** | Ensures frames flush on close |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Passing `level` when reading | `TypeError` | Use `options` / `zstd_dict` on read paths only |
| Mixing trained dict on wrong corpus | Poor ratio or errors | Ship dict with compatible data profile |
| Expecting module on **≤3.13** | ImportError | Feature-gate or fall back to gzip/zlib |

---

## See also

- [The compression package](../the-compression-package/index.md) — canonical import path
- [Data Compression and Archiving hub](../index.md)
