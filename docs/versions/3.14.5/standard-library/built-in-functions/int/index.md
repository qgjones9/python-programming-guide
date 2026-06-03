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

## Best practices

- Use `int(text, 0)` to accept `0b`, `0o`, and `0x` prefixes in config strings.
- Underscores in numeric strings (`int('1_000')`) improve readability since Python 3.6.
- For booleans, `int(True)` is 1; prefer explicit `True`/`False` logic rather than int coercion.
