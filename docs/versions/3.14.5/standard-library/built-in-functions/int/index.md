# [int()](https://docs.python.org/3/library/functions.html#int)

## Description

Constructs an integer from a number, a string in a given base, or objects implementing `__int__()` / `__index__()`.

## What problem it solves

User input, file data, and floats arrive as strings or approximate numbers; programs need exact integer values for indexing, IDs, and bitwise work.

## Implementation options

### Option 1: Parse decimal and base-16 strings

```python
assert int("123") == 123
assert int("face", 16) == 64206
assert int("0xface", 0) == 64206
assert int("01110011", 2) == 115
```

### Option 2: Truncate floats and convert custom types

```python
assert int(3.99) == 3
assert int(-3.99) == -3

class Counter:
    def __index__(self):
        return 7

assert int(Counter()) == 7
```

### Option 3: Base `0` accepts `0b`, `0o`, and `0x` prefixes

```python
assert int("0b1010", 0) == 10
assert int("0o17", 0) == 15
assert int("0x10", 0) == 16
```

### Option 4: Readable literals with underscores

```python
assert int("1_000_000") == 1_000_000
assert int("0x_FF_FF", 0) == 0xFFFF
```

## Best practices

- Use `int(text, 0)` to accept `0b`, `0o`, and `0x` prefixes in config strings.

  ```python
  assert int("42") == 42
  assert int("0b1010", 0) == 10
  assert int("0o17", 0) == 15
  assert int("0xface", 0) == 64206
  ```

- Underscores in numeric strings improve readability since Python 3.6.

  ```python
  assert int("1_000_000") == 1_000_000
  assert int("0x_FF_FF", 0) == 0xFFFF
  ```

- For booleans, `int(True)` is 1; prefer explicit `True`/`False` logic rather than int coercion.

  ```python
  assert int(True) == 1
  assert int(False) == 0

  flag = True
  if flag:  # idiomatic
      result = "on"
  else:
      result = "off"
  assert result == "on"
  ```
