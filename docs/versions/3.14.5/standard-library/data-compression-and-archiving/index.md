# [Data Compression and Archiving](https://docs.python.org/3/library/archiving.html)

Python’s standard library covers **lossless compression** (zlib, gzip, bzip2, lzma, zstd) and **archive formats** (ZIP, tar). Use [`zlib`](zlib-compression-compatible-with-gzip/index.md) for raw deflate streams and checksums; [`gzip`](gzip-support-for-gzip-files/index.md), [`bz2`](bz2-support-for-bzip2-compression/index.md), [`lzma`](lzma-compression-using-the-lzma-algorithm/index.md), and [`compression.zstd`](compressionzstd-compression-compatible-with-the-zstandard-format/index.md) for file-oriented wrappers; [`zipfile`](zipfile-work-with-zip-archives/index.md) and [`tarfile`](tarfile-read-and-write-tar-archive-files/index.md) for bundling many files. Since 3.14, canonical imports live under the [`compression`](the-compression-package/index.md) package while legacy top-level module names remain. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/archiving.html); see also [`shutil`](../file-and-directory-access/shutil-high-level-file-operations/index.md) for high-level archive helpers.

Related material: [`codecs`](../binary-data-services/codecs-codec-registry-and-base-classes/python-specific-encodings/binary-transforms/index.md) binary transforms for base64/hex/zlib in codec form, and [`io`](../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) buffered I/O for stream wrappers.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`compression`](the-compression-package/index.md) | Canonical namespace for compression modules (3.14+) |
| [`compression.zstd`](compressionzstd-compression-compatible-with-the-zstandard-format/index.md) | Zstandard compression and `.zst` files (3.14+) |
| [`zlib`](zlib-compression-compatible-with-gzip/index.md) | Raw deflate, CRC32/Adler-32, gzip-compatible streams |
| [`gzip`](gzip-support-for-gzip-files/index.md) | Read/write `.gz` files and gzip HTTP payloads |
| [`bz2`](bz2-support-for-bzip2-compression/index.md) | bzip2 compression and `.bz2` files |
| [`lzma`](lzma-compression-using-the-lzma-algorithm/index.md) | LZMA/XZ compression and `.xz` files |
| [`zipfile`](zipfile-work-with-zip-archives/index.md) | ZIP archives (store, deflate, bzip2, lzma) |
| [`tarfile`](tarfile-read-and-write-tar-archive-files/index.md) | POSIX tar archives (optionally gzip/bz2/xz compressed) |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Fast in-memory deflate for protocols | [`zlib.compress`](zlib-compression-compatible-with-gzip/index.md) / `decompress` |
| Single compressed file on disk | [`gzip.open`](gzip-support-for-gzip-files/index.md), `bz2.open`, `lzma.open`, or `compression.zstd.open` |
| Bundle many files with random access | [`zipfile`](zipfile-work-with-zip-archives/index.md) |
| Unix-style directory tree archive | [`tarfile`](tarfile-read-and-write-tar-archive-files/index.md) |
| Best speed/ratio trade-off (modern) | [`compression.zstd`](compressionzstd-compression-compatible-with-the-zstandard-format/index.md) |
| Integrity checksum only (no compression) | [`zlib.crc32`](zlib-compression-compatible-with-gzip/index.md) or `adler32` |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Pick **one layer** (zlib vs gzip vs archive) | Double-wrapping wastes CPU and confuses tools |
| Use **context managers** (`with gzip.open(...)`) | Ensures trailers and file handles flush/close |
| Prefer **`shutil.copyfileobj`** for large streams | Avoids loading entire files into memory |
| Set **`compresslevel`** explicitly for reproducible output | Default levels can differ across Python builds |
| Validate **archive paths** before extract | Tar/zip slip attacks use `../` member names |
| Treat compression modules as **optional** on some builds | Distributors may omit bz2, lzma, or zstd |

```python
# Goal: round-trip bytes through zlib deflate
import zlib

data = b"payload for a wire protocol"
compressed = zlib.compress(data, level=zlib.Z_BEST_SPEED)
assert zlib.decompress(compressed) == data
```

```python
# Goal: write and read a gzip text file
import gzip
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "log.txt.gz"
    with gzip.open(path, "wt", encoding="utf-8") as f:
        f.write("line one\n")
    with gzip.open(path, "rt", encoding="utf-8") as f:
        assert f.read() == "line one\n"
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Wrong `wbits` on zlib raw streams | `error` on decompress | Match compressor/decompressor window and header flags |
| Extracting untrusted tar/zip | Overwrite outside target dir | Filter `member.name` or use `filter=` (tarfile 3.12+) |
| Assuming `.gz` is seekable for random writes | Must rewrite from start | Use zip for in-place member updates |
| Mixing text and binary modes on wrappers | Encoding errors or corruption | Use `"t"`/`"b"` consistently with `encoding=` |
| Huge files with `read()` | Memory exhaustion | Stream with `copyfileobj` or incremental compressors |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [The compression package](the-compression-package/index.md) | Canonical 3.14 namespace re-exporting gzip, bz2, lzma, zlib, zstd |
| [compression.zstd — Compression compatible with the Zstandard format](compressionzstd-compression-compatible-with-the-zstandard-format/index.md) | One-shot and streaming Zstandard, dictionaries, `.zst` files |
| [zlib — Compression compatible with **gzip**](zlib-compression-compatible-with-gzip/index.md) | Deflate, CRC32/Adler-32, incremental compress/decompress objects |
| [gzip — Support for **gzip** files](gzip-support-for-gzip-files/index.md) | `.gz` file objects, mtime metadata, HTTP-friendly compression |
| [bz2 — Support for **bzip2** compression](bz2-support-for-bzip2-compression/index.md) | bzip2 one-shot and file interfaces |
| [lzma — Compression using the LZMA algorithm](lzma-compression-using-the-lzma-algorithm/index.md) | LZMA/XZ filters, presets, `.xz` files |
| [zipfile — Work with ZIP archives](zipfile-work-with-zip-archives/index.md) | Create/read ZIP, `ZipInfo`, password-protected entries |
| [tarfile — Read and write tar archive files](tarfile-read-and-write-tar-archive-files/index.md) | ustar/pax/gnu tar, compression modes, safe extraction |
