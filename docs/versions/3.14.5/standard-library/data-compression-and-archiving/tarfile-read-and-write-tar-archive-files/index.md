# [tarfile — Read and write tar archive files](https://docs.python.org/3/library/tarfile.html)

The [`tarfile`](https://docs.python.org/3/library/tarfile.html) module reads and writes **tar archives** (ustar, GNU, and pax formats), optionally wrapped in **gzip**, **bzip2**, **lzma**, or **Zstandard** compression. Use [`zipfile`](../zipfile-work-with-zip-archives/index.md) for PKZIP `.zip` files; use [`shutil`](../../file-and-directory-access/shutil-high-level-file-operations/index.md) for convenience helpers. Full mode tables and filter semantics are on [docs.python.org](https://docs.python.org/3/library/tarfile.html).

**Optional compression.** gzip/bz2/lzma/zstd backends require their respective modules at runtime.

Related: [`compression.zstd`](../compressionzstd-compression-compatible-with-the-zstandard-format/index.md) for `'r:zst'` / `'w:zst'` (3.14+); security filters changed in **3.12** (explicit `filter=`) and **3.14** (default `'data'` filter on extract).

---

## Opening archives — [tarfile.open](https://docs.python.org/3/library/tarfile.html#tarfile.open)

| Mode pattern | Meaning |
|--------------|---------|
| `'r'` or `'r:*'` | Read with **transparent** compression (recommended) |
| `'r:'`, `'r:gz'`, `'r:bz2'`, `'r:xz'`, `'r:zst'` | Read uncompressed or specific codec |
| `'w:'`, `'w:gz'`, `'w:bz2'`, `'w:xz'`, `'w:zst'` | Write (truncate/create) with optional compression |
| `'x:'`, `'x:gz'`, … | Exclusive create (`FileExistsError` if exists) |
| `'a:'` | Append **without** compression only (`'a:gz'` invalid) |
| `'r\|*'`, `'w\|gz'`, … | **Stream** mode (pipe/socket); no random seek |

Use **`tarfile.open()`** rather than constructing `TarFile` directly.

| Function | Role |
|----------|------|
| `tarfile.is_tarfile(name)` | Probe tar magic (path or file-like, 3.9+) |

---

## Members and formats — [TarFile objects](https://docs.python.org/3/library/tarfile.html#tarfile-objects)

| Type constant | Entry kind |
|---------------|------------|
| `REGTYPE` / `DIRTYPE` | Regular file / directory |
| `LNKTYPE` / `SYMTYPE` | Hard link / symbolic link |
| `FIFOTYPE`, `CHRTYPE`, `BLKTYPE` | FIFO, char device, block device |

| Format constant | When writing |
|-----------------|--------------|
| `USTAR_FORMAT` | POSIX ustar |
| `GNU_FORMAT` | GNU extensions (long names, sparse) |
| `PAX_FORMAT` | POSIX.1-2001 pax (default since 3.8) |

Key methods: `add(name, arcname=…)`, `addfile(tarinfo, fileobj)`, `extractall(path, *, filter=…)`, `extract(member, path, *, filter=…)`, `getmembers()`, `gettarinfo(name)`.

---

## Extraction filters — [Extraction filters](https://docs.python.org/3/library/tarfile.html#tarfile-extraction-filter)

Since **3.12**, `extract` / `extractall` accept a **`filter`** callable or named strategy. Since **3.14**, the default filter is **`'data'`** (blocks absolute paths, path traversal, and dangerous special files).

| Filter | Behavior |
|--------|----------|
| `'data'` | Default (3.14+): files and directories only; safe paths |
| `'tar'` | POSIX-style; allows more metadata |
| `'fully_trusted'` | Legacy permissive behavior — only for trusted archives |
| Custom callable | `(tarinfo, path) → tarinfo \| None` to drop or rewrite members |

Filter exceptions include `AbsolutePathError`, `OutsideDestinationError`, `SpecialFileError`, `AbsoluteLinkError`, `LinkOutsideDestinationError`.

```python
# Goal: create and read an uncompressed tar in memory
import io
import tarfile

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:") as tf:
    data = b"hello tar\n"
    info = tarfile.TarInfo(name="greeting.txt")
    info.size = len(data)
    tf.addfile(info, io.BytesIO(data))
buf.seek(0)
with tarfile.open(fileobj=buf, mode="r:") as tf:
    member = tf.getmember("greeting.txt")
    assert tf.extractfile(member).read() == data
```

```python
# Goal: gzip-compressed tar round trip
import io
import tarfile

payload = b"log line\n" * 5
raw = io.BytesIO()
with tarfile.open(fileobj=raw, mode="w:gz", compresslevel=6) as tf:
    info = tarfile.TarInfo("app.log")
    info.size = len(payload)
    tf.addfile(info, io.BytesIO(payload))
raw.seek(0)
with tarfile.open(fileobj=raw, mode="r:*") as tf:
    assert tf.extractfile("app.log").read() == payload
```

```python
# Goal: safe extract with custom filter callback
import io
import tarfile
import tempfile
from pathlib import Path

def reject_absolute_and_dotdot(tarinfo, path):
    dest = Path(path) / tarinfo.name
    try:
        dest.resolve().relative_to(Path(path).resolve())
    except ValueError:
        raise tarfile.TarError(f"unsafe member: {tarinfo.name!r}")
    return tarinfo

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:") as tf:
    data = b"ok"
    info = tarfile.TarInfo(name="safe.txt")
    info.size = len(data)
    tf.addfile(info, io.BytesIO(data))
buf.seek(0)
with tempfile.TemporaryDirectory() as tmp:
    with tarfile.open(fileobj=buf, mode="r:") as tf:
        tf.extractall(tmp, filter=reject_absolute_and_dotdot)
    assert (Path(tmp) / "safe.txt").read_bytes() == b"ok"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`mode='r:*'`** for unknown compression | Avoids `ReadError` from wrong `:gz` / `:xz` suffix |
| Pass **`filter='data'`** (or stricter) on untrusted archives | Mitigates tar slip and symlink attacks |
| Prefer **`extractfile` + manual write** when you only need one member | Avoids touching filesystem layout |
| Set **`arcname=`** in `add()` to control member paths | Prevents leaking absolute source paths |
| Call **`close()`** or use **`with`** on write | Unclosed write archives may lack end blocks |
| Use **stream modes (`\|`)** only for pipes/tapes | No random access; different error class (`StreamError`) |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`extractall` without filter** on hostile input | Writes outside target dir | `filter='data'` or validate `member.name` |
| **`'a:gz'`** mode | Not supported | Append uncompressed or recreate archive |
| **Non-seekable read + wrong mode** | `ReadError` | Use `'r:*'` or stream `'r\|*'` |
| **Assuming `TarFile.close()` finalizes on exception** | Partial archive on disk | Use `try/finally` or delete partial output |
| **Duplicate member names** | Last wins on extract | Inspect `getmembers()` ordering |
| Forgetting **`TarInfo.size`** on `addfile` | Truncated/padded members | Set size to payload length |

---

## See also

| Resource | Link |
|----------|------|
| ZIP archives | [`zipfile`](../zipfile-work-with-zip-archives/index.md) |
| High-level unpack | [`shutil.unpack_archive`](../../file-and-directory-access/shutil-high-level-file-operations/index.md) |
| Compression codecs | [Data Compression and Archiving hub](../index.md) |
| GNU tar format | [Basic Tar Format](https://www.gnu.org/software/tar/manual/html_node/Standard.html) |
