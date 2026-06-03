# [ord()](https://docs.python.org/3/library/functions.html#ord)

## Description

`ord(character)` returns the integer Unicode code point for a one-character string, or the byte value for a length-1 `bytes`/`bytearray` object. It is the inverse of `chr()`.

## What problem it solves

Character encoding work, validating ASCII, building translation tables, and converting between characters and numeric code points.

## Implementation options

### ASCII letters

```python
assert ord("A") == 65
assert ord("z") == 122
assert chr(65) == "A"
```

### Single byte from bytes

```python
assert ord(b"a") == 97
```

### Build a simple Caesar shift for lowercase letters

```python
def shift(char, delta):
    base = ord("a")
    idx = (ord(char) - base + delta) % 26
    return chr(base + idx)

assert shift("a", 3) == "d"
assert shift("y", 3) == "b"
```

## Best practices

- `ord()` requires exactly one character—multi-character strings raise `TypeError`.
- For full Unicode handling beyond BMP, prefer str methods and the `unicodedata` module.
- Pair `ord`/`chr` for teaching encodings; use `.encode()`/`.decode()` for real I/O.
