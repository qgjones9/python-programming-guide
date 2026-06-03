# [Triple-quoted strings](https://docs.python.org/3/reference/lexical_analysis.html#triple-quoted-strings)

Python supports multi-line string literals using triple quotes—either three single (`'''`) or double (`"""`) quote characters. These are called *triple-quoted strings*.

Example:
```python
"""This is a triple-quoted string."""
```

Triple-quoted strings allow:
- Unescaped quote characters (of the *other* kind, or fewer than three consecutive quotes of the same kind), which are part of the string value.
- Embedded newlines—line breaks inside the triple-quoted string are preserved.

For example:
```python
"""This string contains "quotes" and spans
multiple lines."""
```
or
```python
'''You can use single quotes or double quotes.'''
```

A sequence of three matching quote characters (`'''` or `"""`) terminates the string.

---

## String Prefixes

String literals may have a prefix (before the opening quote) that alters how the content is interpreted. Common prefixes:

- `b`: **Bytes literal**  
  Example: `b"data"`
- `r`: **Raw string** (backslashes are not processed as escape characters)  
  Example: `r"C:\path\to\file"`
- `f`: **Formatted string literal** (“f-string”, allows embedded expressions)  
  Example: `f"{value=}"`  
- `t`: **Template string literal** (“t-string”)
- `u`: *No effect; for backward compatibility with Python 2*  
  Example: `u"text"`

See related sections for more on each prefix.

Prefixes are case-insensitive (`B` = `b`). Some prefixes can be combined, and the following combinations are permitted:

- Raw + bytes: `rb"..."` or `br"..."`  
- Raw + formatted: `rf"..."`
- Formatted + raw: `fr"..."`
- Raw + template: `rt"..."`, `tr"..."`

> **New in Python 3.3:** The `rb` and `br` prefixes are synonyms for “raw bytes” literals.

Support for the legacy Unicode literal (`u"value"`) was restored for compatibility between Python 2 and 3. See [PEP 414](https://peps.python.org/pep-0414/) for details.