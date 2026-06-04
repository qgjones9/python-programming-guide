# [shlex — Simple lexical analysis](https://docs.python.org/3/library/shlex.html)

The [`shlex`](https://docs.python.org/3/library/shlex.html) module provides **POSIX-like shell tokenization**: split command strings while honoring quotes, escapes, and comments. Unlike `str.split`, it understands `'single'`, `"double"`, and `\` escapes—essential for safely parsing user shell commands. It is **portable** (available on all platforms). Full API remains on [docs.python.org](https://docs.python.org/3/library/shlex.html).

Related: [`subprocess`](../../concurrent-execution/subprocess-subprocess-management/index.md) with `shell=False` and a list argv; [`tokenize`](../../python-language-services/tokenize-tokenizer-for-python-source/index.md) for Python source, not shell syntax.

---

## Core API — [shlex Objects](https://docs.python.org/3/library/shlex.html#shlex-objects)

| Function / class | Role |
|------------------|------|
| `shlex.split(s, comments=False, posix=True)` | Return list of words from string |
| `shlex.quote(s)` | Return shell-safe quoted string (3.3+) |
| `shlex.join(splitlist)` | Inverse of split for argv lists (3.8+) |
| `shlex.shlex(instream, posix=True, ...)` | Incremental lexer object |

```python
# Goal: split a command line respecting quotes
import shlex

cmd = shlex.split("grep -i 'hello world' *.txt")
assert cmd == ["grep", "-i", "hello world", "*.txt"]
```

```python
# Goal: quote untrusted arguments for shell=True (avoid if possible)
import shlex

user = "file; rm -rf /"
safe = shlex.quote(user)
assert safe.startswith("'") or "\\" in safe
joined = shlex.join(["echo", user])
assert "rm" in joined  # safely quoted as one argument
```

---

## `shlex` lexer object

| Attribute / method | Role |
|--------------------|------|
| `get_token()` | Next token or empty string at EOF |
| `sourcehook` | Resolve `file < path` includes |
| `commenters` | Characters starting comments (default `#`) |
| `whitespace_split` | Split on whitespace only, ignore quotes |

```python
# Goal: incremental tokenization
import io
import shlex

lexer = shlex.shlex(io.StringIO("one two # comment"), posix=True)
lexer.commenters = "#"
tokens = []
while True:
    tok = lexer.get_token()
    if not tok:
        break
    tokens.append(tok)
assert tokens == ["one", "two"]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`subprocess` list argv** over shell strings | Eliminates injection even with `shlex` |
| Use **`posix=True`** (default) for Unix shell rules | Windows cmd.exe uses different rules |
| **`shlex.join`** when building display/debug strings | Safer than manual quoting |

---

## See also

- [`subprocess`](../../concurrent-execution/subprocess-subprocess-management/index.md) — process spawning
- [`argparse`](../../command-line-interface-libraries/argparse-parser-for-command-line-options-arguments-and-subcommands/index.md) — structured CLI parsing
