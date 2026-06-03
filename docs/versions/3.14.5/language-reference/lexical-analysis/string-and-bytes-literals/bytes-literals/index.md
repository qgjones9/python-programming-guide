# [Bytes literals](https://docs.python.org/3/reference/lexical_analysis.html#bytes-literals)

A **bytes literal** is source code that builds a `bytes` object—a fixed-length sequence of integers from 0 to 255—instead of a Unicode `str`. Prefix the opening quote with `b` or `B` (case does not matter):

```python
b'hello'
B"HTTP/1.1"
```

Use bytes literals when you already know the exact byte values you need: protocol constants, file signatures, null-terminated fields, or other binary data that is not human-readable text.

## ASCII-only source text

The characters you type inside a bytes literal must be **ASCII** (code points 0–127). Python evaluates each ASCII character to a byte with the same numeric value.

Any byte with value **128 or greater** cannot appear as a plain character in the source. Write it with an escape sequence instead—most often [`\xhh`](../escape-sequences/hexadecimal-character/index.md) (hexadecimal) or [`\ooo`](../escape-sequences/octal-character/index.md) (octal). See [Escape sequences](../escape-sequences/index.md) for the full list.

The same rule applies to a **zero byte** (value 0): you cannot end a bytes literal with a raw null in the source, so express it as `\0` or `\x00`.

```python
# PNG file signature (magic bytes every PNG starts with)
png_sig = b'\x89PNG\r\n\x1a\n'
list(png_sig)
# [137, 80, 78, 71, 13, 10, 26, 10]

# Null-terminated string (common in C APIs and binary formats)
record = b'user\x00admin\x00'

# Non-ASCII byte via hex escape (0x89 = 137 decimal)
high_byte = b'\x89'
```

Unicode-only escapes—`\N{name}`, `\uxxxx`, and `\Uxxxxxxxx`—belong to **string** literals. They are **not** valid in bytes literals and are treated as unrecognized escapes. Stick to byte-oriented escapes inside `b'…'`.

## Real-world uses

### File and format signatures

Binary formats often begin with a fixed byte pattern. A bytes literal is a concise way to document and compare that pattern:

```python
png_sig = b'\x89PNG\r\n\x1a\n'
pdf_sig = b'%PDF-'
gzip_sig = b'\x1f\x8b'

def is_png(header: bytes) -> bool:
    return header.startswith(png_sig)
```

### Network and text protocols on the wire

HTTP, SMTP, and similar protocols are defined in terms of bytes on the wire. Line endings are `\r\n`, not `\n`:

```python
request = (
    b'GET /index.html HTTP/1.1\r\n'
    b'Host: example.com\r\n'
    b'Connection: close\r\n'
    b'\r\n'
)
assert request.split(b'\r\n', 1)[0] == b'GET /index.html HTTP/1.1'
```

### Binary framing and delimiters

Logs, IPC, and custom file formats often use non-text delimiters:

```python
fields = b'2026-05-29\x1fERROR\x1fDisk full'
date, level, message = fields.split(b'\x1f')
```

### When *not* to use a literal

For large or dynamic binary data, literals are awkward. Prefer:

- **`open(path, 'rb').read()`** — read bytes from a file
- **`bytes.fromhex('89504e47')`** — build from a hex string (tests, configs)
- **`str.encode('utf-8')`** — turn **text** into bytes with an explicit encoding

```python
# Text → bytes: encoding is explicit and documented
greeting = 'café'.encode('utf-8')

# Same ASCII letters as b'hello', but the intent differs:
# b'hello'  → "these exact byte values"
# 'hello'.encode() → "this text in some encoding"
```

## Raw bytes literals (`br` / `rb`)

Combine `b` with `r` for a **raw bytes literal**: backslashes are mostly literal, which helps with Windows paths and regex patterns. See [Raw string literals](../raw-string-literals/index.md).

```python
pattern = br'\\Users\\Public\\'
# b'\\\\Users\\\\Public\\\\'
```

## Best practices

| Practice | Why |
|----------|-----|
| Use `b'…'` for small, fixed binary constants | Clear intent; no encoding guesswork |
| Use `.encode('utf-8')` (or another codec) for human text | Text and bytes are different types in Python 3 |
| Prefer `\xhh` for non-ASCII bytes | Two hex digits are required; easy to read in dumps |
| Use `\x00` or `\0` for null bytes | A raw null cannot appear in source |
| Avoid `\N`, `\u`, and `\U` inside bytes literals | They are for Unicode strings, not byte values |
| Reach for `bytes.fromhex()` or file I/O for large blobs | Keeps source readable and maintainable |
| Compare with `bytes` on both sides | `b'GET' == 'GET'` is always `False` |

## Related sections

| Section | Description |
|---------|-------------|
| [Escape sequences](../escape-sequences/index.md) | Backslash sequences inside string and bytes literals |
| [Hexadecimal character](../escape-sequences/hexadecimal-character/index.md) | `\xhh` byte escapes |
| [Octal character](../escape-sequences/octal-character/index.md) | `\ooo` byte escapes |
| [String prefixes](../string-prefixes/index.md) | How `b`, `r`, and other prefix letters combine |
| [Raw string literals](../raw-string-literals/index.md) | Raw (`r`) and raw-bytes (`br`) behavior |
