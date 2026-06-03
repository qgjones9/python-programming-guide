# [TabError](https://docs.python.org/3/library/exceptions.html#TabError)

Subclass of [`IndentationError`](indentationerror/index.md) raised when indentation **mixes tabs and spaces** inconsistently. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#TabError).

---

## When it is raised

| Cause | Prevention |
|-------|------------|
| Tab after spaces in same block | Editor "insert spaces" setting |
| Copy-paste from mixed sources | Run `python -tt` or linter |

---

## Demonstrating raise and catch

```python
# Goal: TabError is an IndentationError subclass (raise directly for demo)
caught = None
try:
    raise TabError('inconsistent use of tabs and spaces in demo')
except TabError as exc:
    caught = type(exc).__name__
assert caught == 'TabError'
assert issubclass(TabError, IndentationError)
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| Editor “convert tabs to spaces” | Fix file before commit |
| `python -m tabnanny` | CI check for ambiguous indentation |
| `except TabError` | Tooling that loads user scripts—show line number |

Related: [`IndentationError`](indentationerror/index.md), [`SyntaxError`](syntaxerror/index.md).

---

## Best practices

- Use spaces only (4 per indent level per PEP 8).
- Parent chain: [`IndentationError`](indentationerror/index.md) → [`SyntaxError`](syntaxerror/index.md).
