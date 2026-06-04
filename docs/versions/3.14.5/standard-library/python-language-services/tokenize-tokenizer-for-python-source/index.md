# [tokenize — Tokenizer for Python source](https://docs.python.org/3/library/tokenize.html)

The [`tokenize`](https://docs.python.org/3/library/tokenize.html) module implements Python's **source tokenizer**: it reads `.py` text and yields `(type, string, start, end, line)` tuples (and optionally async variants). It powers tools that need lexical detail beyond `ast.parse`—formatters, importers of non-Python syntax extensions, and debuggers. Full API and constants remain on [docs.python.org](https://docs.python.org/3/library/tokenize.html).

Related: [`token`](../token-constants-used-with-python-parse-trees/index.md) for type constants; [`tabnanny`](../tabnanny-detection-of-ambiguous-indentation/index.md) for indentation checks.

---

## Core functions — [Tokenizing Input](https://docs.python.org/3/library/tokenize.html#tokenizing-input)

| Function | Role |
|----------|------|
| `tokenize.generate_tokens(readline)` | Sync iterator over token 5-tuples |
| `tokenize.tokenize(readline)` | Bytes-oriented tokenizer (detects encoding cookie) |
| `tokenize.detect_encoding(readline)` | Return `(encoding, list_of_lines_read)` |
| `tokenize.open(filename)` | Open a file with PEP 263 encoding detection |
| `tokenize.untokenize(iterable)` | Reconstruct source from token tuples |
| `tokenize.NL` / `NEWLINE` / `COMMENT` / `ENCODING` | Extra token types beyond `token` module |

```python
# Goal: tokenize a string and collect NAME tokens
import io
import tokenize

source = "import os\nx = 42\n"
tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
names = [tok.string for tok in tokens if tok.type == tokenize.NAME]
assert names == ["import", "os", "x"]
```

```python
# Goal: round-trip with untokenize
import io
import tokenize

source = "a + b  # comment\n"
tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
rebuilt = tokenize.untokenize(tokens)
assert "a + b" in rebuilt
```

---

## Token tuple fields

| Index / attr | Meaning |
|--------------|---------|
| `type` | Integer code (`token.NAME`, `tokenize.COMMENT`, …) |
| `string` | Exact source slice for the token |
| `start` / `end` | `(line, column)` positions (0-based columns) |
| `line` | Full logical line text (for error context) |

```python
# Goal: locate the column of an operator
import io
import token
import tokenize

source = "result = a + b\n"
for tok in tokenize.generate_tokens(io.StringIO(source).readline):
    if tok.string == "+":
        assert tok.start == (1, 11)
        assert tok.type == token.OP
        break
else:
    raise AssertionError("plus token not found")
```

---

## Encoding and bytes input

Use **`tokenize.tokenize`** on binary streams so the **PEP 263** cookie (`# -*- coding: ... -*-`) is honored. `detect_encoding` reads only as many lines as needed to find the cookie.

```python
# Goal: detect UTF-8 cookie from bytes
import io
import tokenize

data = b"# coding: utf-8\nprint('ok')\n"
encoding, lines = tokenize.detect_encoding(io.BytesIO(data).readline)
assert encoding == "utf-8"
assert lines[0].startswith(b"# coding")
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`generate_tokens`** for in-memory `str` | Simpler than bytes + encoding dance |
| Handle **`tokenize.TokenError`** for truncated input | Unclosed strings or brackets |
| Use **`untokenize`** for lossy round trips only | Comments and spacing may shift |
| Filter **`COMMENT` / `NL`** when building syntax-only tools | Reduce noise in downstream logic |

---

## See also

- [`token`](../token-constants-used-with-python-parse-trees/index.md) — token constant definitions
- [`ast`](../ast-abstract-syntax-trees/index.md) — parser built on token stream
