# [SyntaxError](https://docs.python.org/3/library/exceptions.html#SyntaxError)

Raised when the parser encounters **invalid syntax** during import, [`compile()`](https://docs.python.org/3/library/functions.html#compile), [`exec()`](https://docs.python.org/3/library/functions.html#exec), [`eval()`](https://docs.python.org/3/library/functions.html#eval), or startup. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#SyntaxError).

---

## When it is raised

| Source | Example |
|--------|----------|
| Invalid statement | `if True` without body |
| Bad expression in f-string | Reported with `f-string:` prefix |
| Import of broken module | SyntaxError at import time |

---

## Detail attributes

| Attribute | Meaning |
|-----------|----------|
| `filename` | File being compiled |
| `lineno` | 1-based start line |
| `offset` | 1-based start column |
| `text` | Source line(s) involved |
| `end_lineno`, `end_offset` | End position (3.10+) |

`str(exc)` returns **only the message**; use attributes for location.

---

## Demonstrating raise and catch

```python
# Goal: compile() raises SyntaxError with lineno
caught = None
try:
    compile('if True\n', '<demo>', 'exec')
except SyntaxError as exc:
    caught = (exc.lineno, 'if' in (exc.text or ''))
assert caught == (1, True)
assert issubclass(IndentationError, SyntaxError)
```

---

## Sections in this repo

- [IndentationError](../indentationerror/index.md)
- [TabError](../taberror/index.md)

---

## Best practices

- Catch at tooling boundaries (REPL, plugin loaders) and show `lineno` / `offset` to users.
- Indentation issues often appear as [`IndentationError`](../indentationerror/index.md) or [`TabError`](../taberror/index.md).
