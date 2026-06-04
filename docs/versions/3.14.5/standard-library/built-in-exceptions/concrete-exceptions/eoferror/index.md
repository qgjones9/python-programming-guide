# [EOFError](https://docs.python.org/3/library/exceptions.html#EOFError)

Raised when [`input()`](https://docs.python.org/3/library/functions.html#input) hits end-of-file **without reading any data**. Full reference: [docs.python.org](https://docs.python.org/3/library/exceptions.html#EOFError). File reads at EOF normally return `''`, not this exception.

---

## When it is raised vs not raised

| API | At EOF |
|-----|--------|
| `input()` on empty stream | **`EOFError`** |
| `io.TextIOBase.read()` | Returns `''` |
| `io.IOBase.readline()` | Returns `''` |

---

## Demonstrating raise and catch

```python
import io

# Goal: EOFError is catchable; file read returns empty string
caught = False
try:
    raise EOFError('no input available')
except EOFError:
    caught = True
assert caught
assert io.StringIO('').read() == ''
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except EOFError` | REPL or CLI loop when stdin closes |
| Iterate file lines | Prefer `for line in f` over repeated `input()` |
| Check empty read | `read()` returning `''` is normal EOF for files |

Related: [`OSError`](../oserror/index.md) (broken pipes), [`KeyboardInterrupt`](../keyboardinterrupt/index.md).

---

## Best practices

- In REPL-style loops, catch `EOFError` to exit cleanly when stdin closes.
- For file parsing, iterate lines and check for empty results instead of calling `input()`.
- Do not confuse with [`OSError`](../oserror/index.md) from broken pipes.
