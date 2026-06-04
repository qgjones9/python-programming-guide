# [mmap — Memory-mapped file support](https://docs.python.org/3/library/mmap.html)

The [`mmap`](https://docs.python.org/3/library/mmap.html) module maps files or **anonymous memory** into a mutable byte-like object supporting slicing, `find`, `seek`, and `read`/`write`. Useful for **large-file random access** and **same-machine IPC** without copying entire files into RAM. **Not available on WASI.**

Related: built-in [`memoryview`](../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md), [`os.open`](../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) for raw fds.

---

## Constructor — [mmap.mmap](https://docs.python.org/3/library/mmap.html#mmap.mmap)

| Argument | Role |
|----------|------|
| `fileno` | Open file descriptor, or **`-1`** for anonymous mapping |
| `length` | Bytes to map; `0` often means entire file (platform rules apply) |
| `access` | `ACCESS_READ`, `ACCESS_WRITE`, `ACCESS_COPY`, `ACCESS_DEFAULT` |
| `offset` | Start offset (multiple of allocation granularity) |

```python
# Goal: map a small file and read via slice notation
import mmap
import tempfile
import os

with tempfile.NamedTemporaryFile("w+b", delete=False) as tmp:
    tmp.write(b"Hello Python!\n")
    path = tmp.name

with open(path, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    assert mm[:5] == b"Hello"
    assert mm.readline() == b"Hello Python!\n"
    mm.close()
os.remove(path)
```

```python
# Goal: in-place slice update with same-length replacement
import mmap
import tempfile
import os

with tempfile.NamedTemporaryFile("w+b", delete=False) as tmp:
    tmp.write(b"Hello Python!\n")
    path = tmp.name

with open(path, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    mm[6:13] = b" world!"
    mm.seek(0)
    assert mm.readline() == b"Hello  world!\n"
    mm.close()
os.remove(path)
```

---

## Access modes — [mmap.mmap access](https://docs.python.org/3/library/mmap.html#mmap.mmap)

| Constant | Behavior |
|----------|----------|
| `ACCESS_READ` | Read-only; assignment raises `TypeError` |
| `ACCESS_WRITE` | Writes affect memory and underlying file |
| `ACCESS_COPY` | Copy-on-write; file on disk unchanged |
| `ACCESS_DEFAULT` | Defer to `prot` / platform default |

**Flush** writable buffered files before mapping so stdio buffers reach disk.

```python
# Goal: anonymous mapping with context manager
import mmap

with mmap.mmap(-1, 13) as mm:
    mm.write(b"Hello world!")
    mm.seek(0)
    assert mm.read(5) == b"Hello"
```

---

## Methods — [Memory-mapped file objects](https://docs.python.org/3/library/mmap.html#memory-mapped-file-objects)

| Method | Role |
|--------|------|
| `find(sub)` / `rfind(sub)` | Search bytes (like `bytes`) |
| `read(n)` / `readline()` | Sequential read; advances position |
| `write(bytes)` / `write_byte(n)` | Write at current position |
| `seek(pos, whence)` | Absolute/relative seek (3.13+: returns new pos) |
| `flush()` | Push changes to backing store |
| `resize(newsize)` | Grow/shrink map and file (constraints apply) |
| `close()` | Release mapping; further ops raise `ValueError` |

```python
# Goal: find and tell/seek within a mapping
import mmap
import tempfile
import os

with tempfile.NamedTemporaryFile("w+b", delete=False) as tmp:
    tmp.write(b"abcxyzabc")
    path = tmp.name

with open(path, "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    assert mm.find(b"xyz") == 3
    mm.seek(3)
    assert mm.tell() == 3
    mm.close()
os.remove(path)
```

---

## Unix vs Windows

| Topic | Unix | Windows |
|-------|------|---------|
| `flags` / `prot` | `MAP_SHARED`, `MAP_PRIVATE`, `PROT_READ`, … | Use `access=` keyword |
| `tagname` | N/A | Named shared mappings |
| Empty file map | `length=0` uses file size | Empty file raises on Windows |
| `trackfd=False` (3.13+) | Skip fd dup; `size()`/`resize()` fail | Same concept |

---

## Best practices

| Practice | Why |
|----------|-----|
| **`flush()`** before destroying writable maps | Kernel may not persist without it |
| Match **slice assignment length** | In-place updates require equal size |
| Use **`ACCESS_READ`** for read-only sharing | Prevents accidental writes |
| **`with mmap.mmap(...)`** (3.2+) | Ensures `close()` |
| Prefer **`mmap` over reading whole file** for huge random access | OS pages in data on demand |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Mapping before `flush()` on buffered `io` | Flush file object first |
| `ACCESS_READ` + assignment | Use write access or copy-on-write |
| Windows empty file | Write at least one byte first |
| `resize` with `ACCESS_COPY` | Raises `TypeError` |

---

## See also

- [`re`](../text-processing-services/re-regular-expression-operations/index.md) — can search mmap objects like `bytearray`
