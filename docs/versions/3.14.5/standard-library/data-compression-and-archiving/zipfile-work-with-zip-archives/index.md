# [zipfile — Work with ZIP archives](https://docs.python.org/3/library/zipfile.html)

The [`zipfile`](https://docs.python.org/3/library/zipfile.html) module creates and reads **ZIP archives** — random-access bundles of compressed or stored files. Compression methods include **store** (0), **deflate** (8), **bzip2** (12), **lzma** (14), and **zstd** (93, 3.14+). Use `ZipFile` as a context manager; inspect members with `namelist()` and `infolist()`. Full security and path semantics remain on [docs.python.org](https://docs.python.org/3/library/zipfile.html).

---

## ZipFile essentials

| Method / attr | Role |
|---------------|------|
| `write(filename, arcname=None, compress_type=ZIP_DEFLATED)` | Add file from disk |
| `writestr(zinfo_or_arcname, data, compress_type=...)` | Add bytes/str member |
| `read(name)` | Read member bytes |
| `open(name, mode='r', pwd=None)` | Stream a member |
| `extract(member, path=None, pwd=None)` | Extract to filesystem |
| `extractall(path=None, members=None, pwd=None)` | Extract many (validate paths!) |
| `namelist()` / `infolist()` | Member discovery |

`ZipInfo` carries metadata: `filename`, `compress_type`, `file_size`, `CRC`, `date_time`.

---

## Compression constants

| Constant | Method |
|----------|--------|
| `ZIP_STORED` | No compression |
| `ZIP_DEFLATED` | zlib deflate (requires zlib) |
| `ZIP_BZIP2` | bzip2 (requires bz2) |
| `ZIP_LZMA` | LZMA (requires lzma) |
| `ZIP_ZSTD` | Zstandard (3.14+, requires zstd) |

```python
# Goal: create an in-memory ZIP and read a member back
import io
import zipfile

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("hello.txt", "zip contents")
buf.seek(0)
with zipfile.ZipFile(buf, "r") as zf:
    assert zf.read("hello.txt") == b"zip contents"
    assert "hello.txt" in zf.namelist()
```

```python
# Goal: add a file from disk with a renamed archive path
import tempfile
import zipfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    src = root / "data.txt"
    src.write_text("from disk", encoding="utf-8")
    archive = root / "bundle.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.write(src, arcname="inner/data.txt")
    with zipfile.ZipFile(archive, "r") as zf:
        assert zf.read("inner/data.txt") == b"from disk"
```

```python
# Goal: reject path traversal in member names before extract
import io
import zipfile
from pathlib import Path

def safe_namelist(zf):
    for name in zf.namelist():
        if name.startswith("/") or ".." in Path(name).parts:
            raise ValueError(f"unsafe member: {name!r}")
    return zf.namelist()

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as zf:
    zf.writestr("ok.txt", "fine")
buf.seek(0)
with zipfile.ZipFile(buf, "r") as zf:
    assert safe_namelist(zf) == ["ok.txt"]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`with ZipFile(...)`** | Closes central directory record reliably |
| Validate **member paths** before `extract` | Prevents zip-slip writes outside target |
| Pick **`ZIP_DEFLATED`** as default | Wide compatibility; stored for pre-compressed media |
| Use **`Path.open` + `writestr`** for generated content | Avoids temp files on disk |
| Test **password-protected** archives explicitly | Weak legacy crypto; not a security boundary |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Missing optional codec | `RuntimeError` on ZIP_BZIP2/LZMA/ZSTD | Catch and fall back to DEFLATED |
| `extractall` on untrusted input | Arbitrary file write | Filter names or extract to isolated dir |
| Assuming UTF-8 names on old ZIPs | Mojibake in `ZipInfo.filename` | Respect `flag_bits` UTF-8 flag (3.11+) |

---

## See also

- [tarfile](../tarfile-read-and-write-tar-archive-files/index.md) — streaming tree archives
- [shutil.unpack_archive](https://docs.python.org/3/library/shutil.html#shutil.unpack_archive) — format sniffing helper
- [Data Compression and Archiving hub](../index.md)
