# [memoryview()](https://docs.python.org/3/library/functions.html#func-memoryview)

## Description

`memoryview(object)` returns a memory view over bytes-like or buffer-exporting objects. Views expose slicing and casting without copying the underlying buffer.

## What problem it solves

Efficient binary I/O, parsing protocols, and sharing large byte buffers between libraries without duplicating memory.

## Implementation options

### Slice a bytes object without copying

```python
data = bytearray(b"hello world")
view = memoryview(data)
chunk = view[6:11]
assert bytes(chunk) == b"world"
```

### Mutate through a view

```python
buf = bytearray(b"abc")
mv = memoryview(buf)
mv[0] = ord("x")
assert buf == bytearray(b"xbc")
```

### Release the view before resizing the buffer

```python
payload = bytearray(b"1234")
view = memoryview(payload)
view.release()
payload.append(5)
assert len(payload) == 5
```

## Best practices

- Call `release()` on views when done if the underlying buffer may be resized or freed.

  ```python
  payload = bytearray(b"1234")
  view = memoryview(payload)
  view.release()
  payload.append(5)
  assert len(payload) == 5
  ```

- Prefer `memoryview` for parsing fixed binary layouts over repeated slicing that copies.

  ```python
  data = bytearray(b"\x00\x01\x00\x02")
  view = memoryview(data)
  first = int.from_bytes(view[0:2], "big")
  second = int.from_bytes(view[2:4], "big")
  assert first == 1
  assert second == 2
  assert data == bytearray(b"\x00\x01\x00\x02")  # buffer unchanged
  ```

- Not all buffer operations allow mutation—check `readonly` on the view before writing.

  ```python
  data = b"abc"
  view = memoryview(data)
  assert view.readonly is True

  mutable = bytearray(b"abc")
  writable = memoryview(mutable)
  assert writable.readonly is False
  writable[0] = ord("x")
  assert mutable == bytearray(b"xbc")
  ```
