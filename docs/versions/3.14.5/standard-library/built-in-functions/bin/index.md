# [bin()](https://docs.python.org/3/library/functions.html#bin)

## Description

`bin()` converts an integer to a binary string prefixed with `0b`. The result is a valid Python expression you could paste back into code. Non-`int` objects work if they implement `__index__()`.

## What problem it solves

Debugging bit masks, teaching two's complement, or inspecting low-level flags is easier when you see base-2 form. `bin()` is the quick built-in for that representation without manual division loops.

## Implementation options

### Integer to binary literal

```python
assert bin(3) == "0b11"
assert bin(-10) == "-0b1010"
assert int(bin(255), 0) == 255  # parse back with base 0
```

### Controlling format with `format()`

```python
n = 14
assert bin(n) == "0b1110"
assert format(n, "#b") == "0b1110"
assert format(n, "b") == "1110"  # no prefix
assert f"{n:#b}" == "0b1110"
```

### Bit masks and fixed-width display

```python
flags = 0b1010
assert bin(flags) == "0b1010"
assert format(flags, "08b") == "00001010"
masked = flags | 0b0100
assert bin(masked) == "0b1110"
```

## Best practices

- Use `format(n, "b")` or f-strings when you do not want the `0b` prefix.

  ```python
  n = 14
  assert bin(n) == "0b1110"
  assert format(n, "b") == "1110"
  assert f"{n:b}" == "1110"
  ```

- For fixed-width bit patterns (e.g. 8-bit display), combine formatting instead of `bin()`.

  ```python
  flags = 0b1010
  assert format(flags, "08b") == "00001010"
  # bin(flags) has no width control: "0b1010"
  ```

- Negative values show a signed `-0b...` form; for unsigned bit views of fixed width, mask first.

  ```python
  n = -1
  assert bin(n).startswith("-0b")
  unsigned_byte = n & 0xFF
  assert format(unsigned_byte, "08b") == "11111111"
  ```
