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
- Prefer `memoryview` for parsing fixed binary layouts over repeated slicing that copies.
- Not all buffer operations allow mutation—check `readonly` on the view when writing.
