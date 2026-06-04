# [IndentationError](https://docs.python.org/3/library/exceptions.html#IndentationError)

Subclass of [`SyntaxError`](../syntaxerror/index.md) for syntax errors caused by **incorrect indentation**. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#IndentationError).

---

## When it is raised

| Cause | Example |
|-------|----------|
| Missing indent after block header | `def f()` then unindented body |
| Unexpected indent | Stray leading spaces |
| Inconsistent dedent | Block ends at wrong level |

---

## Demonstrating raise and catch

```python
# Goal: bad indent raises IndentationError (subclass of SyntaxError)
caught = None
try:
    compile('def f():\npass\n', '<demo>', 'exec')
except IndentationError as exc:
    caught = type(exc).__name__
assert caught == 'IndentationError'
assert issubclass(IndentationError, SyntaxError)
```

---

## Sections in this repo

- [TabError](../taberror/index.md)

---

## Best practices

- Configure editors for **spaces-only** (PEP 8) to avoid [`TabError`](../taberror/index.md).
- Parent: [`SyntaxError`](../syntaxerror/index.md).
