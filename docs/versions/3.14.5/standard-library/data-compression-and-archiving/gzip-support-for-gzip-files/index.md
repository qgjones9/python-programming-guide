# [gzip — Support for **gzip** files](https://docs.python.org/3/library/gzip.html)

The [`gzip`](https://docs.python.org/3/library/gzip.html) module reads and writes **GNU gzip** (`.gz`) files and one-shot gzip-wrapped byte strings. Compression uses the underlying [`zlib`](../zlib-compression-compatible-with-gzip/index.md) deflate implementation with a gzip header and CRC32 trailer. It does not handle legacy `compress`/`pack` formats. Full API details remain on [docs.python.org](https://docs.python.org/3/library/gzip.html).

**Optional module.** Depends on `zlib`; if `import gzip` fails, check your Python build.

Related: [`compression.gzip`](../the-compression-package/index.md) re-exports this module (Python 3.14+); [`zipfile`](../zipfile-work-with-zip-archives/index.md) for multi-file archives; [`shutil`](../../file-and-directory-access/shutil-high-level-file-operations/index.md) for stream copying into gzip files.

---

## API surface — overview

| Layer | Types / functions | Use when |
|-------|-------------------|----------|
| File I/O | `open()`, `GzipFile` | Read/write `.gz` on disk or wrapped file objects |
| One-shot | `compress()`, `decompress()` | Entire payload in memory; multi-member gzip streams |
| Underlying codec | `zlib` (via gzip) | Raw deflate without gzip framing — use `zlib` directly |

---

## File (de)compression — [gzip](https://docs.python.org/3/library/gzip.html)

| API | Notes |
|-----|-------|
| `gzip.open(filename, mode='rb', compresslevel=9, …)` | Preferred entry point; text modes wrap `io.TextIOWrapper` |
| `GzipFile(filename=None, mode=None, compresslevel=9, fileobj=None, mtime=None)` | Binary file object; `close()` does not close wrapped `fileobj` |
| Modes | `'r'`/`'rb'`, `'w'`/`'wb'`, `'a'`/`'ab'`, `'x'`/`'xb'`; text: `'rt'`, `'wt'`, etc. |
| `compresslevel` | **0–9** (0 = store only); default **9** |
| `mtime` | Unix timestamp in header; **`0`** for reproducible output; **`None`** uses current time (3.14 default for `compress()` is `0`) |

| Attribute / method | Role |
|--------------------|------|
| `GzipFile.peek(n)` | Read uncompressed bytes without advancing position |
| `GzipFile.mtime` | Last header timestamp when reading (`None` before first read) |
| `GzipFile.name` | Path of underlying file (3.12+) |
| `BadGzipFile` | Invalid gzip stream (subclass of `OSError`, 3.8+) |

```python
# Goal: one-shot compress/decompress round trip
import gzip

data = b"Lots of content here\n" * 10
compressed = gzip.compress(data, compresslevel=6, mtime=0)
assert gzip.decompress(compressed) == data
```

```python
# Goal: write and read a gzip text file in memory
import gzip
import io

buf = io.BytesIO()
with gzip.open(buf, "wt", encoding="utf-8", compresslevel=1) as out:
    out.write("hello gzip\n")
buf.seek(0)
with gzip.open(buf, "rt", encoding="utf-8") as inp:
    assert inp.read() == "hello gzip\n"
```

```python
# Goal: stream copy into gzip without loading entire source
import gzip
import io
import shutil

source = io.BytesIO(b"x" * 5000)
dest = io.BytesIO()
with gzip.open(dest, "wb", compresslevel=3) as gz_out:
    shutil.copyfileobj(source, gz_out)
dest.seek(0)
assert len(gzip.decompress(dest.read())) == 5000
```

---

## Choosing gzip vs alternatives

| Criterion | gzip | [`zlib`](../zlib-compression-compatible-with-gzip/index.md) | [`compression.zstd`](../compressionzstd-compression-compatible-with-the-zstandard-format/index.md) |
|-----------|------|-------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| On-disk format | `.gz` with header/trailer | Raw deflate or zlib wrapper | `.zst` frames |
| Typical speed | Fast | Fastest (no file metadata) | Often faster at similar ratios |
| HTTP / log pipelines | Common (`Content-Encoding: gzip`) | Custom framing | Emerging; not universal in older stacks |
| Multi-member streams | `decompress()` handles concatenation | Per-stream `wbits` | `compression.zstd.decompress()` |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`gzip.open()`** for files | Handles text encoding and path-like objects |
| Pass **`mtime=0`** when reproducible bytes matter | CI artifacts and cache keys stay stable (3.14+ default for `compress()`) |
| Use **`shutil.copyfileobj`** for large inputs | Avoids reading whole file into memory |
| Prefer **`zlib.decompress(data, wbits=31)`** for single-member blobs | Faster than `gzip.decompress()` when you know layout |
| Do not treat gzip as encryption | Compression does not hide content |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Expecting **`GzipFile.close()`** to close wrapped file | Underlying handle stays open | Close wrapper yourself if needed |
| **`peek()`** on file-backed gzip | May advance underlying file position | Document side effect for wrapped objects |
| Mixing **text and binary** modes | Encoding errors or mojibake | Pick `"t"`/`"b"` once; set `encoding=` for text |
| **`compresslevel=0`** | Stored blocks, not smaller wire size | Use only when CPU cost outweighs savings |
| Opening **`GzipFile` for write without `mode`** | Deprecated since 3.9 | Always pass explicit `mode='wb'` |

---

## See also

| Resource | Link |
|----------|------|
| Raw deflate | [`zlib`](../zlib-compression-compatible-with-gzip/index.md) |
| ZIP deflate members | [`zipfile`](../zipfile-work-with-zip-archives/index.md) |
| Faster deflate (third party) | [python-isal](https://pypi.org/project/isal/) |
| Section hub | [Data Compression and Archiving](../index.md) |
