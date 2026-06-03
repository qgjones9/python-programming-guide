# [Unrecognized escape sequences](https://docs.python.org/3/reference/lexical_analysis.html#unrecognized-escape-sequences)

When Python reads a string or bytes literal, it looks at each backslash (`\`) and tries to interpret what follows as an [escape sequence](../index.md). Recognized sequences—such as `\n`, `\t`, `\x41`, or `\u0041`—become special characters. **Unrecognized** sequences are treated differently from Standard C: Python does **not** reject them; it keeps the backslash in the result as a literal `\` character.

That lenient behavior helps when you embed paths, regex patterns, or other text that happens to contain a backslash followed by an ordinary letter. It also means typos like `\q` silently become two characters instead of failing at compile time—so Python now warns you when it sees them.

> **Note:** [Raw strings](../../string-prefixes/index.md) (`r"..."`) skip escape processing entirely. The rules on this page apply to ordinary (non-raw) string and bytes literals.

## Examples

### Backslash kept in the result

If `\` is not followed by a valid escape, both the backslash and the next character appear literally in the string:

```python
>>> print('\q')
\q
>>> repr('\q')
'\\q'
>>> list('\q')
['\\', 'q']
```

Compare with a **recognized** escape—the backslash is consumed and replaced:

```python
>>> repr('\n')       # newline — one character
'\n'
>>> repr('\q')       # unrecognized — two characters
'\\q'
```

### Common pitfall: regex and Windows paths

Patterns that look like C or regex escapes are often **not** valid Python escapes. Without a raw prefix, Python warns and leaves the backslash in place:

```python
>>> repr('\d')       # SyntaxWarning: not \d as in regex
'\\d'
>>> repr('\w+')      # SyntaxWarning
'\\w+'
>>> repr('C:\temp\data.txt')   # SyntaxWarning: \t → tab, \d kept literally
'C:\temp\\data.txt'
```

For regex and file paths, prefer a **raw string** so backslashes stay literal:

```python
>>> repr(r'\d+')
'\\d+'
>>> repr(r'C:\new\file.txt')
'C:\\new\\file.txt'
```

Or double the backslash in an ordinary string: `'\\\\d+'`.

### String-only escapes in bytes literals

Escapes that work only in **str** literals—[`\N{name}`](../named-unicode-character/index.md), `\uxxxx`, and `\Uxxxxxxxx`—are **not** recognized inside **bytes** literals. They fall into the same “unrecognized” category: the backslash is preserved.

```python
>>> b'\x41'           # recognized bytes escape
b'A'
>>> b'\n'             # recognized
b'\n'

>>> b'\N{SNAKE}'      # string-only — backslash kept
b'\\N{SNAKE}'
>>> b'\u0041'         # string-only — backslash kept
b'\\u0041'
>>> b'\U0001f40d'     # string-only — backslash kept
b'\\U0001f40d'
>>> list(b'\u0041')
[92, 117, 48, 48, 52, 49]
```

Use [`\xhh`](../hexadecimal-character/index.md) or [`\ooo`](../octal-character/index.md) in bytes literals when you need non-ASCII byte values.

### Warnings and future errors

Python has tightened behavior over recent versions:

| Version | Behavior |
|---------|----------|
| Before 3.6 | Unrecognized escapes silently kept the backslash |
| 3.6 | [DeprecationWarning](../../../../../standard-library/built-in-exceptions/warnings/index.md) |
| 3.12 | `SyntaxWarning` (subclass of `DeprecationWarning`) |
| Future | Planned [SyntaxError](../../../../../standard-library/built-in-exceptions/concrete-exceptions/index.md) |

In Python 3.12+, loading a module with `'\q'` emits a warning at **compile** time:

```text
SyntaxWarning: invalid escape sequence '\q'
```

You can treat warnings as errors during development to catch mistakes early:

```bash
python -W error::SyntaxWarning your_script.py
```

With that flag, an invalid escape like `'\q'` raises `SyntaxError` immediately—matching the direction the language is heading.

### Fixing unrecognized escapes

| Situation | Fix |
|-----------|-----|
| Regex, paths, or literal `\` before a letter | Use `r"..."` or double each `\` (`"\\\\"`) |
| Typo for a real escape (`\t`, `\n`, `\x41`) | Spell the correct escape sequence |
| Unicode in a bytes literal | Use `\x` or `\ooo`, not `\u` / `\U` / `\N` |
| Warning on legacy code | Add an `r` prefix or fix the escape |

When in doubt, run `repr(your_string)` in the REPL—the doubled backslash `\\` in the output tells you a backslash was stored literally.
