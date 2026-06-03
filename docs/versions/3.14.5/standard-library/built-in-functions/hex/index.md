# [hex()](https://docs.python.org/3/library/functions.html#hex)

## Description

Converts an integer to a lowercase hexadecimal string prefixed with `0x`.

## What problem it solves

Debugging binary protocols, memory addresses, and color codes often requires hexadecimal representation of integers.

## Implementation options

### Option 1: Display integer values in hex

```python
value = 255
assert hex(value) == "0xff"
assert hex(-42) == "-0x2a"
```

### Option 2: Format hex without 0x prefix using format

```python
color = 0xFF5733
assert format(color, "x") == "ff5733"
assert format(color, "#06x") == "0xff5733"
```

### Option 3: Round-trip with `int()`

```python
original = 64206
as_hex = hex(original)
assert int(as_hex, 16) == original
assert int(as_hex, 0) == original  # accepts 0x prefix
```

### Option 4: Large integers and negative values

```python
big = 2**64
assert hex(big) == "0x10000000000000000"
assert hex(-1) == "-0x1"
```

## Best practices

- `hex()` always includes the `0x` prefix and uses lowercase a–f.

  ```python
  assert hex(255) == "0xff"
  assert hex(64206) == "0xface"
  assert hex(-42) == "-0x2a"
  ```

- Use `int(hex_string, 16)` or `int(hex_string, 0)` to parse hex strings back to integers.

  ```python
  original = 64206
  as_hex = hex(original)
  assert int(as_hex, 16) == original
  assert int(as_hex, 0) == original  # accepts 0x prefix
  ```

- For floats, use `float.hex()` rather than `hex()`—`hex()` only accepts integers.

  ```python
  value = 3.5
  assert "p" in value.hex()  # IEEE 754 hex format, not plain 0x integer hex

  try:
      hex(3.5)
  except TypeError:
      pass
  else:
      raise AssertionError("expected TypeError")
  ```
