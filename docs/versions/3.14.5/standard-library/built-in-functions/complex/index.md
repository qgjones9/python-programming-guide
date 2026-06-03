# [complex()](https://docs.python.org/3/library/functions.html#complex)

## Description

`complex()` builds a complex number from one numeric or string argument, or from separate real and imaginary parts (keyword or positional). It follows numeric conversion protocols (`__complex__`, then `__float__`, then `__index__`).

## What problem it solves

Scientific code, signal processing, and geometry use complex arithmetic. `complex()` parses string literals like `"-1.23+4.5j"` and coerces other numeric types without manual real/imag unpacking.

## Implementation options

### From strings and components

```python
assert complex("1+2j") == (1 + 2j)
assert complex("-4.5j") == -4.5j
assert complex(1.23) == (1.23 + 0j)
assert complex(real=-1, imag=4.5) == (-1 + 4.5j)
```

### Coercion from integers and floats

```python
assert complex(5) == (5 + 0j)
assert complex(2.5, 0) == (2.5 + 0j)

z = complex(3, 4)
assert abs(z) == 5.0
assert z.real == 3 and z.imag == 4
```

### Arithmetic with literals

```python
z = (1 + 2j) * (3 - 1j)
assert complex(z.real, z.imag) == z
assert (1 + 2j).conjugate() == (1 - 2j)
```

## Best practices

- String forms must not contain spaces around `+`/`-` and `j` (`complex("1 + 2j")` raises `ValueError`).

  ```python
  assert complex("1+2j") == 1 + 2j
  try:
      complex("1 + 2j")
      raise AssertionError("expected ValueError")
  except ValueError:
      pass
  ```

- Prefer `1j` literals in code; use `complex()` for parsing external data.

  ```python
  z = 3 + 4j  # idiomatic in source code
  assert z.real == 3 and z.imag == 4

  parsed = complex("3+4j")  # from config or wire format
  assert parsed == z
  ```

- Use separate real and imag arguments only when both are known numerics—not for string parsing.

  ```python
  assert complex(3, 4) == 3 + 4j
  # complex("3", "4")  # TypeError — strings are not valid as separate parts
  ```
