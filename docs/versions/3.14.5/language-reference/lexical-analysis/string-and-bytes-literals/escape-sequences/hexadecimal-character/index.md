# [Hexadecimal character](https://docs.python.org/3/reference/lexical_analysis.html#hexadecimal-character)

To represent a character (or byte) using its hexadecimal (base-16) code point in Python, use the escape sequence `\xhh`, where `hh` stands for exactly two hexadecimal digits (0–9, a–f, or A–F).

**Important:** Unlike some other languages (such as C), Python always requires *exactly* two hexadecimal digits after `\x`.

**Examples:**

- In a string literal (text strings), `\xhh` inserts the Unicode character with the code point `hh`.  
- In a bytes literal (`b''`), `\xhh` inserts a single byte with the given value.

```python
# Example in a regular (Unicode) string literal
s = '\x50'    # \x50 is hexadecimal for 80, which is 'P' in ASCII
print(s)      # Output: P

# Example in a bytes literal
b = b'\x50'
print(b)      # Output: b'P'

# Using hexadecimal escapes for non-printable characters
newline = '\x0a'     # \x0a is hexadecimal for 10, which is newline '\n'
print(f"Line1{newline}Line2")
# Output:
# Line1
# Line2
```

**Summary Table:**

| Escape   | Type         | Meaning                        | Example Output   |
|----------|--------------|--------------------------------|------------------|
| `\x50`   | string       | Unicode char U+0050 ('P')      | `'P'`            |
| `b'\x50'`| bytes        | Byte 0x50 (ASCII 'P')          | `b'P'`           |

Remember: You must provide two hex digits, such as `\x09` or `\x4A`. Writing `\x9` or `\xF` will raise a `SyntaxError` in Python.