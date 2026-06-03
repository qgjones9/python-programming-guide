# [oct()](https://docs.python.org/3/library/functions.html#oct)

## Description

`oct(integer)` converts an integer to a lowercase octal string with an `0o` prefix. Non-integers must define `__index__()`. The result is a valid Python literal.

## What problem it solves

Debugging low-level values, Unix file permissions, and teaching base-8 representation without manual division loops.

## Implementation options

### Positive and negative integers

```python
assert oct(8) == "0o10"
assert oct(-8) == "-0o10"
```

### Round-trip with int(base=8)

```python
text = oct(511)
assert int(text, 8) == 511
```

### File mode style bitmask

```python
mode = 0o755
assert oct(mode) == "0o755"
assert int("755", 8) == 493
```

## Best practices

- Use `format(n, "o")` or f-strings when you need octal without the `0o` prefix.

  ```python
  n = 511
  assert format(n, "o") == "777"
  assert f"{n:o}" == "777"
  assert oct(n) == "0o777"
  ```

  ```python
  # oct() always includes 0o—strip only when you need bare digits:
  assert oct(8)[2:] == "10"  # careful: not the same as format(8, "o") for negatives
  ```

- Remember Python 3 uses `0o` prefix; do not confuse with old C-style leading zero literals.

  ```python
  assert oct(9) == "0o11"
  assert int("0o11", 8) == 9
  ```

  ```python
  # Incorrect—leading zero alone is a syntax error in Python 3, not octal:
  # n = 011
  ```

- For user-facing output, label the base explicitly so values are not misread as decimal.

  ```python
  mode = 0o755
  display = f"mode {oct(mode)} (octal)"
  assert "0o755" in display
  ```

  ```python
  # Ambiguous for users—755 looks like decimal:
  # print(f"mode {int('755', 8)}")  # prints 493 without saying octal
  ```
