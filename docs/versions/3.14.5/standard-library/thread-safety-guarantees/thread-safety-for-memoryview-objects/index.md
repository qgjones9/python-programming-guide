# [Thread safety for memoryview objects](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-memoryview-objects)

A **`memoryview`** exposes another object’s buffer without copying. Thread safety splits into two layers: the **view object itself** (export tracking, immutable metadata) and the **underlying exporter** (who owns the bytes). Full specification remains on [docs.python.org](https://docs.python.org/3/library/threadsafety.html#thread-safety-for-memoryview-objects); this page explains both layers and practical locking.

This page is part of the [Thread Safety Guarantees](../index.md) hub. Mutable-buffer rules for `bytearray` are detailed in [Thread safety for bytearray objects](../thread-safety-for-bytearray-objects/index.md).

---

## Scope: what the implementation guarantees

| Layer | Free-threaded guarantee |
|-------|-------------------------|
| **memoryview object** | Creating and releasing views uses **atomic** export tracking; safe from multiple threads. |
| **Immutable view attributes** | Reads of `shape`, `format`, `itemsize`, `ndim`, `strides`, `readonly`, etc. are safe while the view is alive — these fields do not change for the lifetime of the view. |
| **Buffer bytes** | Safety depends entirely on the **exporter** (`bytes`, `bytearray`, `array`, NumPy array, …). |

When the **GIL is enabled**, export bookkeeping is still correct, but concurrent reads/writes to mutable underlying storage remain a **logical data race** without your own synchronization.

---

## memoryview object: thread-safe bookkeeping

| Operation | Thread-safe? |
|-----------|--------------|
| `memoryview(obj)` | Yes — export count updated atomically in free-threaded builds. |
| `view.release()` / view going out of scope | Yes — export released atomically. |
| Reading `view.shape`, `view.format`, `view.readonly`, … | Yes — immutable for the view’s lifetime. |
| Indexing/slicing **through** the view | Depends on underlying object (see below). |

The view does **not** copy data; it only tracks that the exporter’s buffer is borrowed.

---

## Underlying object: where races happen

| Exporter | Concurrent reads | Concurrent writes | Notes |
|----------|------------------|-------------------|-------|
| **`bytes`** | Safe | N/A (immutable) | Multiple `memoryview(bytes_obj)` readers need no lock for the data itself. |
| **`bytearray`** | Not safe without sync | Not safe without sync | Per-byte races corrupt logical content even if structures stay intact. |
| **Read-only `memoryview` of mutable buffer** | **Not** safe if another thread mutates exporter | N/A via view if `readonly=True` | `readonly` blocks writes **through the view**, not writes **to the original `bytearray`**. |

```python
# Read-only view does NOT stop another thread from mutating the bytearray
data = bytearray(b"abc")
view = memoryview(data)
assert view.readonly is False
ro = view.toreadonly()
assert ro.readonly is True
# Another thread can still: data[0] = ord("z")  # data race with readers of ro
```

---

## NOT safe: concurrent writes through views

Two threads writing the same mutable region through one or more views is undefined at the application level (garbled bytes, torn updates):

```python
# Illustrative anti-pattern — do NOT run concurrently without a lock
data = bytearray(8)
view = memoryview(data)
# Thread 1: view[0:4] = b"xxxx"
# Thread 2: view[4:8] = b"yyyy"
# Use threading.Lock around all buffer mutations instead.
```

---

## `BufferError` while a view is exported

Resizing or reallocating the **exporter** while any `memoryview` (or other buffer export) is active raises **`BufferError`**, regardless of threading:

```python
def demo_buffer_error_on_resize():
    data = bytearray(b"abc")
    view = memoryview(data)
    try:
        data.extend(b"extra")
    except BufferError as exc:
        assert "cannot be re-sized" in str(exc) or "re-sized" in str(exc)
    else:
        raise AssertionError("expected BufferError")
    view.release()
    data.extend(b"extra")
    assert data == b"abcextra"

demo_buffer_error_on_resize()
```

After `view.release()` (or the view is garbage-collected), the exporter may resize again.

---

## Best practices

| Situation | Recommended approach |
|-----------|---------------------|
| Share mutable binary data across threads | One `threading.Lock` around **all** reads/writes to the exporter and any views |
| Publish read-only API | Prefer `bytes` snapshots (`bytes(ba)`) or copy-on-write, not `readonly` views alone |
| Long-lived view | Keep exporter alive; release view before `extend` / resize on `bytearray` |
| Multiple views of same `bytearray` | Same lock covers exporter and every view |
| Immutable wire format | Store as `bytes`; `memoryview` for zero-copy reads only |
| NumPy / third-party buffers | Follow that library’s threading docs in addition to these rules |

---

## Examples

### Safe concurrent reads over immutable `bytes`

```python
import threading

def demo_bytes_memoryview_reads():
    payload = b"hello"
    view = memoryview(payload)
    seen = []

    def reader():
        seen.append(view[0])

    threads = [threading.Thread(target=reader) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert seen == [ord("h")] * 5

demo_bytes_memoryview_reads()
```

### Lock pattern for shared mutable buffer

```python
import threading

def demo_lock_with_memoryview():
    data = bytearray(8)
    view = memoryview(data)
    lock = threading.Lock()

    def fill(chunk, byte_val):
        start = chunk * 4
        with lock:
            view[start : start + 4] = bytes([byte_val]) * 4

    t1 = threading.Thread(target=fill, args=(0, ord("a")))
    t2 = threading.Thread(target=fill, args=(1, ord("b")))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    with lock:
        assert len(view) == 8
        assert set(view) <= {ord("a"), ord("b")}

demo_lock_with_memoryview()
```

### Read-only view vs mutable exporter

```python
def demo_readonly_does_not_freeze_exporter():
    data = bytearray(b"abc")
    ro = memoryview(data).toreadonly()
    assert ro.readonly is True
    data[0] = ord("z")
    assert bytes(ro) == b"zbc"

demo_readonly_does_not_freeze_exporter()
```

### Release view before resize

```python
def demo_release_then_extend():
    data = bytearray(b"x")
    view = memoryview(data)
    view.release()
    data.extend(b"yz")
    assert data == b"xyz"

demo_release_then_extend()
```

---

## Related topics in this guide

| Subject | Link |
|---------|------|
| Thread Safety Guarantees hub | [thread-safety-guarantees](../index.md) |
| bytearray per-object lock and buffer-protocol compares | [thread-safety-for-bytearray-objects](../thread-safety-for-bytearray-objects/index.md) |
| Thread safety levels | [thread-safety-levels](../thread-safety-levels/index.md) |
| Binary sequence types | [bytes, bytearray, memoryview](../../built-in-types/binary-sequence-types-bytes-bytearray-memoryview/index.md) |

**See also:** [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html); [Buffer protocol](https://docs.python.org/3/c-api/buffer.html) (C API) for export semantics.
