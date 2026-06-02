# [Hexadecimal Unicode characters](https://docs.python.org/3/reference/lexical_analysis.html#hexadecimal-unicode-characters)

When you know a character's **Unicode code point** as a number, you can insert it directly with a hexadecimal escape—without looking up its official name (as with [`\N{name}`](../named-unicode-character/index.md)).

Python provides two forms:

| Escape | Digits | Code point range | Typical use |
|--------|--------|------------------|-------------|
| `\uxxxx` | Exactly **4** hex digits | Basic Multilingual Plane (`U+0000`–`U+FFFF`) | Latin letters, accented text, most common symbols |
| `\Uxxxxxxxx` | Exactly **8** hex digits | Full Unicode (`U+00000000`–`U+0010FFFF`) | Emojis, rare scripts, any character outside the BMP |

Write hex digits as `0`–`9` or `a`–`f` (case-insensitive). For `\U`, pad with leading zeros so the value is always eight digits wide.

> **Note:** These escapes work only in **string** literals. They are **not** processed in [bytes literals](../../string-prefixes/index.md) or [raw strings](../../string-prefixes/index.md) (`r"..."`).

## Examples

### `\u` — four-digit escapes (BMP)

The `\u` form is handy for characters whose code point fits in sixteen bits—letters, punctuation, and symbols you will see in everyday text:

```python
>>> '\u0041'          # U+0041 — LATIN CAPITAL LETTER A
'A'
>>> '\u00e9'          # U+00E9 — é
'é'
>>> '\u1234'          # U+1234 — Ethiopic syllable
'ሴ'
>>> '\u263a'          # U+263A — white smiling face
'☺'
```

You can chain several `\u` escapes in one literal to spell out a word or phrase:

```python
>>> '\u03b1\u03b2\u03b3'   # Greek alpha, beta, gamma
'αβγ'
>>> f"Smile: \u263a"
'Smile: ☺'
```

### `\U` — eight-digit escapes (full Unicode)

Characters above `U+FFFF`—including most emojis—live outside the Basic Multilingual Plane. Use `\U` with **eight** hex digits (leading zeros included):

```python
>>> '\U0001f40d'      # U+1F40D — snake emoji
'🐍'
>>> '\U0001f600'      # U+1F600 — grinning face
'😀'
```

The same BMP character can be written with either form; `\U` just pads the code point to eight digits:

```python
>>> '\u0041' == '\U00000041'
True
>>> '\n' == '\U0000000A'
True
```

### Same character, different escape styles

For a given code point, `\u`, `\U`, and [`\N{name}`](../named-unicode-character/index.md) all produce the same result when valid:

```python
>>> '\U0001f40d' == '\N{SNAKE}'
True
>>> hex(ord('🐍'))
'0x1f40d'
```

At runtime you can also build characters with `chr()`:

```python
>>> chr(0x1F40D)
'🐍'
>>> chr(0x1F40D) == '\U0001f40d'
True
```

### Exactly the right number of digits

Python reads a **fixed width** of hex digits after `\u` or `\U`. Too few digits is a syntax error; extra characters after a complete escape are treated as literal text:

```python
>>> '\u0041'          # valid — four digits
'A'
>>> '\u041'           # SyntaxError — only three digits after \u
>>> '\U0001f40d'      # valid — eight digits
'🐍'
>>> '\U1234'          # SyntaxError — only four digits after \U

>>> '\u12345'         # four digits consumed, then literal '5'
'ሴ5'
```

Think of `\u12345` as `\u1234` followed by the character `'5'`, not as a five-digit code point.

### Not processed in raw or bytes literals

In a raw string, backslash-u is kept literally—useful when you want the text `\u0041` in your data, not the letter `A`:

```python
>>> r'\u0041'
'\\u0041'
```

In a bytes literal, `\u` and `\U` are not recognized escapes; the backslash is preserved:

```python
>>> b'\u0041'
b'\\u0041'
>>> list(b'\u0041')
[92, 117, 48, 48, 52, 49]
```

For raw byte values in the `0`–`255` range, use [`\xhh`](../hexadecimal-character/index.md) or [`\ooo`](../octal-character/index.md) instead.

### Choosing `\u` vs `\U` vs `\N`

| You know… | Use |
|-----------|-----|
| A 4-digit hex code in the BMP | `\uxxxx` |
| A full code point (especially above `U+FFFF`) | `\Uxxxxxxxx` |
| The official Unicode name | `\N{NAME}` |

When in doubt, look up the code point (for example with `ord('🐍')` or the [Unicode charts](https://www.unicode.org/charts/)) and pick the shortest escape that fits.
