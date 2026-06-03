# [bytes()](https://docs.python.org/3/library/functions.html#func-bytes)

## Description

`bytes()` creates an immutable sequence of byte values (0–255). Constructor arguments mirror `bytearray()`: empty default, integer size, iterable of ints, buffer object, or encoded string.

## What problem it solves

Network payloads, file contents, cryptographic digests, and UTF-8 text on the wire all use bytes. `bytes()` is the canonical way to materialize binary data that must not change accidentally after creation.

## Implementation options

### Literals and construction

```python
assert bytes(b"raw") == b"raw"
assert bytes(3) == b"\x00\x00\x00"
assert bytes([72, 105]) == b"Hi"
assert bytes("π", encoding="utf-8") == "\u03c0".encode("utf-8")
```

### Encoding text for I/O

```python
def write_line(stream, text: str) -> None:
    stream.write(bytes(text + "\n", encoding="utf-8"))

import io
buf = io.BytesIO()
write_line(buf, "log message")
assert buf.getvalue() == b"log message\n"
```

### Joining byte fragments

```python
parts = [b"Hello", b", ", b"world"]
message = bytes().join(parts)
assert message == b"Hello, world"
```

## Best practices

- Use `b"..."` literals when the content is ASCII; call `bytes(..., encoding=...)` for dynamic Unicode.

  ```python
  assert bytes("hi", "ascii") == b"hi"
  label = "café"
  encoded = label.encode("utf-8")
  assert isinstance(encoded, bytes)
  # bytes(label)  # TypeError — str needs an encoding
  ```

- Immutable bytes are hashable and safe as dict keys; bytearray is not.

  ```python
  key = b"token"
  cache = {key: 42}
  assert cache[b"token"] == 42
  ```

- Decode at boundaries (UI, JSON) and keep binary layers in `bytes` end-to-end.

  ```python
  wire = b"\xc3\xa9"  # UTF-8 for "é"
  assert wire.decode("utf-8") == "é"
  assert isinstance(wire, bytes)
  ```
