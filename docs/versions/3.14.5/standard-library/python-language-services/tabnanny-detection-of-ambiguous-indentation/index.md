# [tabnanny — Detection of ambiguous indentation](https://docs.python.org/3/library/tabnanny.html)

The [`tabnanny`](https://docs.python.org/3/library/tabnanny.html) module scans Python source for **ambiguous indentation**: lines where tabs and spaces are mixed in a way that can confuse readers or differ across editors. It is a small policy checker, not a full linter. Full behavior and CLI usage remain on [docs.python.org](https://docs.python.org/3/library/tabnanny.html).

Related: [`tokenize`](../tokenize-tokenizer-for-python-source/index.md) (token stream); [PEP 8](https://peps.python.org/pep-0008/) style guidance.

---

## Core API — [Checker Classes](https://docs.python.org/3/library/tabnanny.html)

| Name | Role |
|------|------|
| `tabnanny.check(file)` | Raise `NannyNag` if the file has inconsistent indentation |
| `tabnanny.process_tokens(tokens)` | Check an iterable of tokenize tuples |
| `tabnanny.NannyNag` | Exception carrying filename and line number |
| `tabnanny.verbose` | Module flag; set to `1` for extra logging |
| `tabnanny.filename_only` | When true, only print offending filenames |

```python
# Goal: clean spaces-only file passes
import io
import tempfile
import tokenize
import tabnanny

source = "def ok():\n    return 1\n"
with tempfile.NamedTemporaryFile("w+", suffix=".py", delete=False) as tmp:
    tmp.write(source)
    tmp.flush()
    tabnanny.check(tmp.name)
```

```python
# Goal: process_tokens on an in-memory stream
import io
import tokenize
import tabnanny

source = "x = 1\n"
tokens = tokenize.generate_tokens(io.StringIO(source).readline)
tabnanny.process_tokens(tokens)  # no exception
```

---

## What triggers `NannyNag`

| Pattern | Risk |
|---------|------|
| Tab used for indent on one line, spaces on the next | Visual alignment depends on tab width |
| Mixed leading whitespace on continuation lines | Hard to see in diffs and editors |

The module **tokenizes** the file (respecting encoding) and inspects **INDENT** / **DEDENT** context—it does not validate PEP 8 line length or naming.

```python
# Goal: detect ambiguous tab/space mixing
import io
import tokenize
import tabnanny

bad = "def f():\n\tpass\n \tpass\n"  # tab then space+tab on next line
tokens = tokenize.generate_tokens(io.StringIO(bad).readline)
try:
    tabnanny.process_tokens(tokens)
except tabnanny.NannyNag:
    pass
else:
    raise AssertionError("expected NannyNag for mixed indent")
```

---

## Command-line use

Run as **`python -m tabnanny [-v] [-q] file_or_directory ...`**. Quiet mode (`-q`) prints only files with problems—useful in pre-commit hooks alongside `compileall`.

---

## Best practices

| Practice | Why |
|----------|-----|
| Standardize on **spaces (4)** or **tabs**, never both | Avoids `NannyNag` and team friction |
| Run tabnanny in **CI** on changed `.py` files | Cheap guard before review |
| Do not rely on tabnanny for **syntax** errors | Use `py_compile` or `ast.parse` instead |

---

## See also

- [`tokenize`](../tokenize-tokenizer-for-python-source/index.md) — underlying tokenizer
- [`compileall`](../compileall-byte-compile-python-libraries/index.md) — batch syntax check
