# [BufferError](https://docs.python.org/3/library/exceptions.html#BufferError)

`BufferError` is raised when an operation involving the [buffer protocol](https://docs.python.org/3/c-api/buffer.html#bufferobjects) cannot be completed—typically problems with **memoryview**, **bytes-like** exports, or resizing constraints—not ordinary file or network I/O (those use [`OSError`](../../os-exceptions/index.md)). Full wording: [docs.python.org](https://docs.python.org/3/library/exceptions.html#BufferError).

---

## Role in the hierarchy

`BufferError` inherits directly from [`Exception`](../exception/index.md). There are no further built-in subclasses; the interpreter raises `BufferError` itself when buffer rules are violated.

```python
# Goal: BufferError is a leaf under Exception
assert issubclass(BufferError, Exception)
assert BufferError.__bases__ == (Exception,)
```

---

## Typical situations

| Situation | What goes wrong |
|-----------|-----------------|
| Resizing a buffer **while exported** | For example `array.append` with an active `memoryview` |
| Invalid **resize** or **cast** on a buffer | Shape/format incompatible with underlying object |
| C-extension buffer APIs | Underlying object cannot expose or mutate memory as requested |

These differ from **`TypeError`** (wrong Python type or read-only assignment) and **`ValueError`** (wrong value for an otherwise valid operation). When code uses `memoryview` or objects exporting `__buffer__`, expect `BufferError` for **buffer-level** constraints.

```python
import array

def demo_buffer_error_on_resize():
    data = array.array("i", [1, 2, 3])
    view = memoryview(data)
    caught = None
    try:
        data.append(4)  # cannot resize while view exports the buffer
    except BufferError as exc:
        caught = type(exc).__name__
    finally:
        view.release()
    assert caught == "BufferError"

demo_buffer_error_on_resize()
```

---

## Catching `BufferError`

Use a dedicated handler when you wrap low-level binary APIs and can retry or fall back (for example copy into a writable `bytearray`). For general application logic, catching [`Exception`](../exception/index.md) is wider than necessary.

```python
def write_byte_writable(data, index, value):
    view = memoryview(data)
    if view.readonly:
        data = bytearray(data)
        view = memoryview(data)
    view[index] = value
    return bytes(data)

assert write_byte_writable(b"abc", 0, ord("z")) == b"zbc"
```

---

## When to use or raise `BufferError`

| Do | Don't |
|----|-------|
| Let the interpreter raise it for invalid buffer mutations | Raise `BufferError` for “file not found” or bad JSON |
| Catch it around custom C extensions using the buffer API | Confuse with `MemoryError` (allocator out of memory) |
| Document buffer ownership when exposing `memoryview` to callers | Use instead of `TypeError` when the object is not bytes-like at all |

User code **may** raise `BufferError` to mirror interpreter behavior when implementing buffer exporters, but most Python-only projects never raise it explicitly.

---

## Best practices

- Prefer **writable** `bytearray` or allocate a new buffer when callers need in-place updates.
- Release `memoryview` objects when done (`view.release()`) before resizing the underlying `array`.
- Read [Buffer objects](https://docs.python.org/3/c-api/buffer.html#bufferobjects) when writing C extensions that fill `Py_buffer`.

---

## Common pitfalls

- Assuming **`bytes` is mutable** — it is not; assigning through a `memoryview` of `bytes` typically raises **`TypeError`** (“read-only memory”), not `BufferError`.
- Catching **`Exception`** and treating all failures as `BufferError` — test with `except BufferError`.
- Holding a **`memoryview`** while mutating the exporter’s size — release the view first.

---

## Related pages

| Topic | Link |
|-------|------|
| Application error base | [Exception](../exception/index.md) |
| OS / errno failures | [OS exceptions](../../os-exceptions/index.md) |
| Parent index | [Base classes](../index.md) |
