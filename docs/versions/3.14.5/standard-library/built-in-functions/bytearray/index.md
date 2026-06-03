# [bytearray()](https://docs.python.org/3/library/functions.html#func-bytearray)

## Description

`bytearray()` constructs a mutable sequence of integers in the range 0–255. You can initialize it from an integer size, an iterable of byte values, a buffer-exporting object, or a string plus encoding.

## What problem it solves

Binary protocols and file chunks often need in-place edits—patching headers, building packets incrementally, or decoding streams without copying to an immutable `bytes` object each time. `bytearray` is the standard mutable byte container.

## Implementation options

### Build and mutate in place

```python
buf = bytearray(b"hello")
buf[0] = ord("H")
assert buf == bytearray(b"Hello")

buf.extend(b"!")
assert bytes(buf) == b"Hello!"
```

### From size, iterable, or encoded text

```python
zeros = bytearray(4)
assert len(zeros) == 4 and all(b == 0 for b in zeros)

from_list = bytearray([65, 66, 67])
assert from_list == b"ABC"

text = bytearray("café", encoding="utf-8")
assert "é".encode("utf-8") in text
```

### Decode slice without copying the whole buffer

```python
buf = bytearray(b"prefix:payload")
start = buf.index(b":") + 1
chunk = bytes(buf[start:])
assert chunk.decode("ascii") == "payload"
```

## Best practices

- Convert to `bytes()` when passing to APIs that require immutability (dict keys, some crypto functions).

  ```python
  buf = bytearray(b"key:value")
  key = bytes(buf[:3])
  mapping = {key: "payload"}
  assert mapping[b"key"] == "payload"
  # bytearray is not hashable: {buf: 1}  # TypeError
  ```

- Prefer `bytearray` over repeated `bytes` concatenation in loops—extend or slice-assign instead.

  ```python
  parts = [b"a", b"b", b"c"]

  # idiomatic
  buf = bytearray()
  for part in parts:
      buf.extend(part)
  assert bytes(buf) == b"abc"

  # slow: re-allocates each iteration
  # out = b""
  # for part in parts:
  #     out += part
  ```

- Use slice assignment for in-place edits without creating new objects.

  ```python
  buf = bytearray(b"hello")
  buf[0:5] = b"HELLO"
  assert buf == bytearray(b"HELLO")
  ```
