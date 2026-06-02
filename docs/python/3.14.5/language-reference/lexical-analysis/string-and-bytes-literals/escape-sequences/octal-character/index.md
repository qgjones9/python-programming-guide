# [Octal character](https://docs.python.org/3/reference/lexical_analysis.html#octal-character)

Octal escape sequences in Python take the form `\ooo`, where `ooo` represents up to three octal (base 8) digits (digits 0–7). This escape sequence allows you to include a character in your string or bytes literal by specifying its octal code point.

For example:
```python
# The octal value 120 corresponds to the character 'P'
print('\120')  # Output: P
```

A few important points to remember:
- **Up to three octal digits are recognized:** You can use one, two, or three octal digits after the backslash, but no more.
- **Context matters:**  
  - In *bytes literals* (e.g., `b'\ooo'`), the escape represents a single byte with that value.
  - In *string literals* (e.g., `'\ooo'`), it represents the Unicode character with that code point.

**Version Notes:**
- *Python 3.11:* Using octal escapes with a value greater than `0o377` (255) triggers a `DeprecationWarning`.
- *Python 3.12:* Octal escapes with values greater than `0o377` now produce a `SyntaxWarning`. In future Python releases, such escapes will result in a `SyntaxError`.

This means if you use an octal value above 255, Python will begin warning you and will eventually make this an error in upcoming versions.

