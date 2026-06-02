# [String prefixes](https://docs.python.org/3/reference/lexical_analysis.html#string-prefixes)

String literals in Python can have one or more optional **prefixes** before the opening quote, which change how the string is interpreted. Examples:

```python
b"data"        # bytes literal
f'{result=}'   # formatted string (f-string)
r"C:\path"     # raw string (backslashes not escaped)
```

**Allowed prefixes:**

| Prefix | Meaning                                 |
|--------|------------------------------------------|
| `b`    | Bytes literal                           |
| `r`    | Raw string (no escape processing)       |
| `f`    | Formatted string literal (“f-string”)   |
| `t`    | Template string literal (“t-string”)    |
| `u`    | Unicode literal (no effect, legacy)     |

- Prefixes are **case-insensitive** (`B"..."` = `b"..."`).
- Some prefixes can be **combined**. Valid combinations include:
  - Raw + bytes: `rb"..."` or `br"..."`
  - Raw + formatted: `rf"..."` or `fr"..."`
  - Raw + template: `rt"..."` or `tr"..."`
- See linked sections for details on each prefix and their behavior.

> **Note (Python 3.3+):**  
> The `rb` and `br` prefixes are equivalent for raw bytes literals.

> **Legacy support:**  
> The `u"..."` prefix (Unicode literal) was reintroduced for smoother compatibility between Python 2 and 3 codebases. See [PEP 414](https://peps.python.org/pep-0414/) for details.


## Examples

### Basic prefixes

```python
>>> "hello"
'hello'
>>> b"data"
b'data'
>>> r"C:\new\text.txt"
'C:\\new\\text.txt'
>>> f"{2 + 2}"
'4'
>>> type(t"Hello")  # template string (3.14+); yields Template, not str
<class 'string.templatelib.Template'>
>>> u"legacy"  # same as a plain str in Python 3
'legacy'
```

### Case-insensitive prefixes

```python
>>> B"bytes" == b"bytes"
True
>>> R"raw" == r"raw"
True
>>> F"{1}" == f"{1}"
True
```

### Raw vs ordinary strings (escapes)

Without `r`, backslash escapes are processed; with `r`, they are kept literally (except when escaping the quote):

```python
>>> "\n"          # newline (one character)
'\n'
>>> r"\n"         # backslash + letter n (two characters)
'\\n'
>>> r'\d{4}-\d{2}-\d{2}'   # handy for regex patterns
'\\d{4}-\\d{2}-\\d{2}'
```

### Combined prefixes

Order does not matter for two-letter combinations:

```python
>>> rb"\x41" == br"\x41"
True
>>> type(rb"\x41")
<class 'bytes'>

>>> path = "docs"
>>> rf"C:\{path}\readme.txt"   # raw f-string: literal backslashes + interpolation
'C:\\docs\\readme.txt'

>>> rt"C:\logs\{id}.txt"        # raw + template (3.14+); backslashes stay literal
```

### F-string features

```python
>>> who = "nobody"
>>> nationality = "Spanish"
>>> f"{who.title()} expects the {nationality} Inquisition!"
'Nobody expects the Spanish Inquisition!'

>>> x = 42
>>> f"{x=}"          # debug specifier: name and value
'x=42'

>>> print(f"{{literal braces}}")
{literal braces}
```

### Bytes literals and non-ASCII

Bytes literals hold ASCII; values 128+ need escape sequences:

```python
>>> b'\x89PNG\r\n\x1a\n'
b'\x89PNG\r\n\x1a\n'
>>> list(b'\x89PNG\r\n\x1a\n')
[137, 80, 78, 71, 13, 10, 26, 10]
```

### Invalid prefix usage

The prefix must sit immediately before the opening quote—no whitespace:

```python
>>> b "data"   # SyntaxError
```

A raw string cannot end with a lone backslash (it would escape the closing quote):

```python
>>> r"\\"      # valid: two backslashes
'\\\\'
>>> r"\"       # SyntaxError: unterminated string
```

