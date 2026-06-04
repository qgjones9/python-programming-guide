# [The compression package](https://docs.python.org/3/library/compression.html)

Added in Python 3.14, the [`compression`](https://docs.python.org/3/library/compression.html) package is the **canonical namespace** for standard-library compression modules. Submodules re-export the long-standing top-level names (`gzip`, `bz2`, `lzma`, `zlib`) and add [`compression.zstd`](https://docs.python.org/3/library/compression.zstd.html) for Zstandard. Legacy imports (`import gzip`) remain supported and are not scheduled for removal without a deprecation cycle. Full details remain on [docs.python.org](https://docs.python.org/3/library/compression.html).

---

## Submodules

| Submodule | Re-exports / provides |
|-----------|----------------------|
| `compression.gzip` | Same API as [`gzip`](../gzip-support-for-gzip-files/index.md) |
| `compression.bz2` | Same API as [`bz2`](../bz2-support-for-bzip2-compression/index.md) |
| `compression.lzma` | Same API as [`lzma`](../lzma-compression-using-the-lzma-algorithm/index.md) |
| `compression.zlib` | Same API as [`zlib`](../zlib-compression-compatible-with-gzip/index.md) |
| `compression.zstd` | Zstandard compression — see [dedicated notes](../compressionzstd-compression-compatible-with-the-zstandard-format/index.md) |

---

## When to use the package namespace

| Situation | Import style |
|-----------|--------------|
| New 3.14+ code grouping compression | `from compression import gzip, zstd` |
| Libraries supporting 3.10–3.13 | Keep `import gzip` / `import zlib` |
| Type checkers and IDE discovery | Prefer `compression.*` to signal the modern layout |
| Optional zstd backend | `import compression.zstd` (module may be absent on minimal builds) |

```python
# Goal: import gzip API via the compression namespace (Python 3.14+)
import importlib
import sys

if sys.version_info >= (3, 14):
    cgzip = importlib.import_module("compression.gzip")
    data = b"hello"
    compressed = cgzip.compress(data)
    assert cgzip.decompress(compressed) == data
```

```python
# Goal: fall back to top-level gzip when compression package is unavailable
import importlib

def gzip_module():
    try:
        return importlib.import_module("compression.gzip")
    except ModuleNotFoundError:
        return importlib.import_module("gzip")

gzip = gzip_module()
assert gzip.decompress(gzip.compress(b"ok")) == b"ok"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`compression.zstd`** for new zstd code | No historical alias at top level |
| Re-export **one style** per project | Mixing `gzip` and `compression.gzip` confuses readers |
| Guard **optional** submodules | `compression.zstd` may be missing on some builds |
| Do not expect **`compression` on ≤3.13** | Feature-gate imports in portable libraries |

---

## See also

- [Data Compression and Archiving hub](../index.md)
- [compression.zstd](../compressionzstd-compression-compatible-with-the-zstandard-format/index.md)
