# [chr()](https://docs.python.org/3/library/functions.html#chr)

## Description

`chr()` returns a one-character string for a Unicode code point in the range 0 through 1,114,111 (0x10FFFF). It is the inverse of `ord()`.

## What problem it solves

Building strings from numeric code points—protocol fields, escape sequences, or table-driven encoders—needs a safe conversion from integer to character. `chr()` centralizes bounds checking and Unicode semantics.

## Implementation options

### ASCII and beyond-BMP characters

```python
assert chr(97) == "a"
assert chr(8364) == "€"
assert ord(chr(8364)) == 8364
```

### Building strings from code point lists

```python
codepoints = [72, 101, 108, 108, 111]
word = "".join(chr(cp) for cp in codepoints)
assert word == "Hello"

try:
    chr(1_114_112)  # above U+10FFFF
except ValueError:
    pass
else:
    raise AssertionError("expected ValueError")
```

### Round-trip with `ord()` for a simple codec

```python
def encode_ascii(text: str) -> list[int]:
    return [ord(ch) for ch in text]

def decode_ascii(codepoints: list[int]) -> str:
    return "".join(chr(cp) for cp in codepoints)

assert decode_ascii(encode_ascii("Hi")) == "Hi"
```

## Best practices

- Validate code points before calling `chr()` when input comes from untrusted data.

  ```python
  def safe_chr(codepoint: int) -> str:
      if not 0 <= codepoint <= 0x10FFFF:
          raise ValueError("invalid code point")
      return chr(codepoint)

  assert safe_chr(65) == "A"
  ```

- For byte values 0–255, `bytes([n]).decode("latin-1")` and `chr(n)` both yield a character—but only `chr()` accepts full Unicode.

  ```python
  assert chr(233) == "é"
  assert bytes([233]).decode("latin-1") == "é"
  assert chr(0x1F600) == "😀"
  # bytes([0x1F600])  # ValueError — byte must be 0–255
  ```

- Pair with `ord()` for round-trip character arithmetic in parsers and serializers.

  ```python
  text = "Hi"
  codes = [ord(ch) for ch in text]
  assert codes == [72, 105]
  assert "".join(chr(cp) for cp in codes) == text
  ```
