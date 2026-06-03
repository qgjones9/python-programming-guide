# [Named Unicode character](https://docs.python.org/3/reference/lexical_analysis.html#named-unicode-character)

To insert a specific Unicode character in a string based on its official Unicode name, use the escape sequence `\N{name}` within a string literal. The name must match an entry in the Unicode character database (official name or, since Python 3.3, a [name alias](https://www.unicode.org/Public/UCD/latest/ucd/NameAliases.txt)).

**Syntax:** `\N{OFFICIAL UNICODE NAME}` — all caps, spaces between words, inside curly braces.

> **Note:** The `\N{name}` escape sequence is **not** processed in bytes literals (see [String prefixes](../../string-prefixes/index.md)) or in [raw strings](../../string-prefixes/index.md) (`r"..."`).

**Version note (Python 3.3):** Support for Unicode name aliases was introduced in this version.

## Examples

### Basic usage

```python
>>> '\N{LATIN CAPITAL LETTER P}'
'P'
>>> '\N{SNAKE}'
'🐍'
>>> '\N{BLACK HEART SUIT}'
'♥'
>>> '\N{POUND SIGN}'
'£'
>>> '\N{EURO SIGN}'
'€'
>>> '\N{GREEK SMALL LETTER PI}'
'π'
```

### Combining characters in one string

```python
>>> "Hello \N{LATIN SMALL LETTER E WITH ACUTE}!\N{EXCLAMATION MARK}"
'Hello é!!'
>>> "\N{GREEK SMALL LETTER ALPHA}\N{GREEK SMALL LETTER BETA}\N{GREEK SMALL LETTER GAMMA}"
'αβγ'
>>> f"Price: \N{POUND SIGN}5"
'Price: £5'
```

### Name aliases (Python 3.3+)

Several names can refer to the same character. These all produce a newline (`U+000A`):

```python
>>> '\N{LINE FEED}' == '\N{NEW LINE}' == '\N{LF}'
True
>>> repr('\N{LINE FEED}')
'\\n'
```

Other useful names:

```python
>>> '\N{NULL}'
'\x00'
>>> '\N{ZERO WIDTH SPACE}'
'\u200b'
```

### Inspecting the result

```python
>>> c = '\N{SNAKE}'
>>> len(c)
1
>>> hex(ord(c))
'0x1f40d'
>>> '\N{SNAKE}' == '\U0001f40d'   # same code point, different escape
True
```

### Not processed in raw or bytes literals

In a raw string, `\N{...}` is kept as literal characters (no escape processing):

```python
>>> r'\N{SNAKE}'
'\\N{SNAKE}'
```

In a bytes literal, `\N` is not a recognized bytes escape—the backslash is preserved:

```python
>>> b'\N{SNAKE}'
b'\\N{SNAKE}'
>>> list(b'\N{SNAKE}')
[92, 78, 123, 83, 78, 65, 75, 69, 125]
```

### Invalid names

If `{name}` does not match any known character name or alias, Python reports an error when decoding the literal:

```python
>>> '\N{NOT A REAL NAME}'   # SyntaxError: unknown Unicode character name
```

Look up official names in the [Unicode Character Database](https://www.unicode.org/charts/) or with `unicodedata.name()`:

```python
>>> import unicodedata
>>> unicodedata.name('🐍')
'SNAKE'
>>> unicodedata.name('\u00e9')
'LATIN SMALL LETTER E WITH ACUTE'
```
