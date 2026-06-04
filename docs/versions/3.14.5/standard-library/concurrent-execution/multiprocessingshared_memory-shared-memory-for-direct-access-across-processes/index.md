# [multiprocessing.shared_memory — Shared memory for direct access across processes](https://docs.python.org/3/library/multiprocessing.shared_memory.html)

The [`multiprocessing.shared_memory`](https://docs.python.org/3/library/multiprocessing.shared_memory.html) module allocates **POSIX-style shared memory** that multiple processes map into their address space — faster than piping large blobs when you need **raw byte buffers** or NumPy views. Lifecycle helpers live in [`SharedMemoryManager`](https://docs.python.org/3/library/multiprocessing.shared_memory.html#multiprocessing.managers.sharedmemorymanager) (`multiprocessing.managers`). Added in 3.8. Reference: [docs.python.org](https://docs.python.org/3/library/multiprocessing.shared_memory.html).

---

## `SharedMemory`

| Parameter | Role |
|-----------|------|
| `name` | Attach to existing block, or `None` to auto-name when creating |
| `create` | `True` = allocate new block |
| `size` | Bytes requested (may round up to page size) |
| `track` (3.13+) | Register with resource tracker (see upstream for subprocess caveats) |

| Method / attr | Role |
|---------------|------|
| `buf` | `memoryview` over the segment |
| `name`, `size` | Read-only metadata |
| `close()` | Close handle in this process |
| `unlink()` | Destroy block (once globally) |

```python
# Goal: create, write, attach second handle, cleanup
from multiprocessing import shared_memory

shm = shared_memory.SharedMemory(create=True, size=8)
try:
    shm.buf[:5] = b"hello"
    other = shared_memory.SharedMemory(name=shm.name)
    try:
        assert bytes(other.buf[:5]) == b"hello"
        other.buf[0] = ord("H")
        assert bytes(shm.buf[:1]) == b"H"
    finally:
        other.close()
finally:
    shm.close()
    shm.unlink()
```

---

## `ShareableList`

Fixed-length list backed by shared memory; stores `bool`, `int`, `float`, `str`, `bytes`, `None` only — **no append**, length fixed at creation.

```python
# Goal: mutate entries in a ShareableList
from multiprocessing import shared_memory

sl = shared_memory.ShareableList([1, 2, 3])
sl[1] = 99
assert list(sl) == [1, 99, 3]
sl.shm.close()
sl.shm.unlink()
```

**Known issue:** trailing `\x00` in `str`/`bytes` may be stripped on read ([gh-106939](https://github.com/python/cpython/issues/106939)); pad and strip in application code if needed.

---

## `SharedMemoryManager`

Starts a manager process that tracks segments; `shutdown()` / context manager calls `unlink()` on all blocks it created.

```python
# Goal: manager creates ShareableList and releases on exit
from multiprocessing.managers import SharedMemoryManager

with SharedMemoryManager() as smm:
    sl = smm.ShareableList(range(4))
    assert sl[2] == 2
# segments unlinked after context
```

---

## vs queues and pickle

| Approach | When |
|----------|------|
| `Queue` / pipes | Arbitrary picklable messages, moderate size |
| `SharedMemory` + `memoryview`/NumPy | Large arrays, tight latency, manual sync |
| `Manager().list()` | Higher overhead, simpler API |

Shared mutable data **drops GIL-level safety** — coordinate with locks or process design.

---

## See also

- [multiprocessing](../multiprocessing-process-based-parallelism/index.md) — processes and `Manager`
- [memoryview](https://docs.python.org/3/library/stdtypes.html#memoryview) — buffer protocol
