# [Raw string literals](https://docs.python.org/3/reference/lexical_analysis.html#raw-string-literals)

A **raw string literal** (or **raw bytes literal**) is source code prefixed with `r` or `R`. The prefix tells Python to treat **backslashes as ordinary characters** instead of starting [escape sequences](../escape-sequences/index.md). That makes raw literals ideal whenever your text contains many backslashes—regular expressions, Windows paths, and other patterns that would otherwise require doubling every `\`.

Both `str` and `bytes` literals support the raw prefix:

```python
r'hello\nworld'    # str: backslash and n, not a newline
rb'\x00\xff'       # bytes: same raw backslash rules (also written br'…')
```

The `r` prefix can be combined with other prefixes such as `b` (bytes) and `f` (f-strings). Order does not matter: `rf'…'`, `fr'…'`, `br'…'`, and `rb'…'` are all valid.

## How raw literals differ from normal strings

In a normal string, `\` starts an escape sequence. Python interprets `\n` as a newline, `\\` as one backslash, and so on. In a raw string, **almost every backslash is copied into the value unchanged**.

```python
import re

# Normal string: \d is not a valid escape; Python leaves \ and d (with a warning in some contexts)
# You usually double backslashes for regex:
pattern = '\\d{4}-\\d{2}-\\d{2}'

# Raw string: what you type is what re receives
pattern = r'\d{4}-\d{2}-\d{2}'

assert pattern == '\\d{4}-\\d{2}-\\d{2}'
re.fullmatch(pattern, '2026-05-29')  # matches
```

Use a **normal** string when you want escape processing (`'\n'`, `'\t'`, `'\\'`). Use a **raw** string when backslashes should survive literally into the final text.

## Quote escaping (the one special case)

Even in a raw literal, a backslash can **escape the closing quote** so you can embed that quote inside the literal. The backslash **still appears in the result**—it is not removed.

```python
r"\""   # two characters: backslash, then double quote
r'\''   # two characters: backslash, then single quote
```

Because of this rule, a raw string **cannot end with an odd number of backslashes**. The final `\` would escape the closing quote and leave the literal unterminated:

```python
# SyntaxError: unterminated string literal
# r"C:\Users\Public\"

# Valid alternatives:
path = r"C:\Users\Public" + "\\"
path = "C:\\Users\\Public\\"
```

## Newlines are not line continuations

In a normal string, `\` immediately followed by a newline is an [ignored end of line](../escape-sequences/ignored-end-of-line/index.md)—the physical line break disappears from the value. In a raw string, `\` plus newline are **two literal characters** (backslash and linefeed), not a continuation:

```python
# Normal string: one logical line, no embedded newline
s = 'hello\
world'
len(s)   # 10

# Raw string: backslash and newline are both kept
r = r'hello\
world'
len(r)   # 12 — "hello" + \ + newline + "world"
```

For multi-line text, prefer [triple-quoted strings](../triple-quoted-strings/index.md) or explicit `\n` in a normal string rather than relying on raw `\` + newline.

## Real-world uses

### Regular expressions

This is the most common reason to reach for `r'…'`. The `re` module expects regex syntax with backslashes (`\d`, `\s`, `\b`, …). Raw strings keep patterns readable:

```python
import re

DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')

text = 'Contact: alice@example.com by 2026-05-29'
EMAIL.search(text).group()
DATE.search(text).group()
```

Without `r`, every regex metacharacter backslash must be doubled in source code, which is easy to get wrong during maintenance.

### Windows and UNC paths

File paths on Windows use backslashes. A raw string avoids writing `\\` everywhere:

```python
log_dir = r'C:\Logs\app'
unc = r'\\server\share\data.csv'
```

For production code, [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) is usually clearer than string paths, but raw strings remain handy for quick scripts, tests, and constants.

### Embedded formats (JSON, LaTeX, SQL)

When a snippet contains backslash-heavy syntax, raw literals reduce noise:

```python
# JSON string value as it would appear inside a .json file
json_fragment = r'{"path": "C:\\Users\\Public"}'

# LaTeX command in documentation or test fixtures
latex = r'\frac{a}{b}'
```

Remember: raw strings do **not** remove the need to escape quotes that match your delimiter, and they do not change how the **consumer** of the string (JSON parser, regex engine, etc.) interprets backslashes.

### Raw bytes for binary regex or protocols

Combine `r` with `b` when a bytes pattern needs literal backslashes—common in binary log parsers or mixed ASCII/binary protocols:

```python
import re

# Match a Windows-style path segment in bytes
WIN_SEGMENT = re.compile(br'[A-Za-z]:\\(?:[^\\]+\\)*')
```

See [Bytes literals](../bytes-literals/index.md) for when to use `b'…'` instead of `str`.

## Best practices

| Practice | Why |
|----------|-----|
| Use `r'…'` for `re` patterns and similar backslash-heavy text | One backslash in source → one backslash in the value |
| Keep using normal strings for `\n`, `\t`, `\uXXXX`, etc. | Raw literals do not process those escapes |
| Do not end a raw path with a single `\` | Use concatenation, a normal string, or `pathlib` |
| Prefer `pathlib.Path` over manual path strings | Avoids platform-specific escaping mistakes |
| Use `rf'…'` when you need both raw backslashes and `{expression}` interpolation | f-string expressions still evaluate; only `\` handling is “raw” |
| Match `bytes` vs `str` to your API | `re.compile(r'…')` vs `re.compile(br'…')` must align with input type |
| Do not assume raw means “no escaping at all” | Quote characters can still be escaped with `\`, and that `\` is kept |

## When *not* to use a raw string

- **Human-readable multiline text** with intentional newlines and tabs — use normal or triple-quoted strings.
- **Unicode escapes** — `\u`, `\U`, and `\N{…}` are not interpreted in raw strings; use normal strings or actual Unicode characters.
- **Paths that must end in `\`** — raw literals cannot end on a lone backslash; append `'\\'` or use `Path`.
- **Replacing proper APIs** — URL encoding, JSON serialization, and HTML escaping belong in `urllib.parse`, `json`, or templating libraries, not ad hoc raw string manipulation.

## Related sections

| Section | Description |
|---------|-------------|
| [Escape sequences](../escape-sequences/index.md) | Backslash processing in normal (non-raw) literals |
| [String prefixes](../string-prefixes/index.md) | How `r` combines with `b`, `f`, and other prefixes |
| [Bytes literals](../bytes-literals/index.md) | `b`-prefixed literals and raw bytes (`br` / `rb`) |
| [Triple-quoted strings](../triple-quoted-strings/index.md) | Multi-line string literals |
| [f-strings](../f-strings/index.md) | Formatted literals; combine with `r` as `rf` or `fr` |
