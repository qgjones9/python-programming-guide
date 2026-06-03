# [UnicodeEncodeError](https://docs.python.org/3/library/exceptions.html#UnicodeEncodeError)

Subclass of [`UnicodeError`](unicodeerror/index.md) raised during **Unicode encoding** (str → bytes). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#UnicodeEncodeError).

---

## When it is raised

| Cause | Example |
|-------|----------|
| Character not representable in target encoding | Emoji with `ascii` codec |
| Strict error handler | Default `'strict'` raises |

---

## Demonstrating raise and catch

```python
# Goal: non-ASCII char with ascii codec raises UnicodeEncodeError
text = 'café'
caught = None
try:
    text.encode('ascii')
except UnicodeEncodeError as exc:
    caught = (exc.encoding, exc.start, exc.end, text[exc.start:exc.end])
assert caught == ('ascii', 3, 4, 'é')
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `encode('utf-8')` | Modern default for wire/storage |
| `encode('ascii', errors='ignore')` | Lossy fallback (document data loss) |
| `except UnicodeEncodeError` | User-facing “unsupported character” message |

---

## Best practices

- Default to UTF-8 for wire format and file output; restrict to ASCII only when the protocol requires it.
- When using `errors='ignore'`, document that output may be lossy.
- Parent: [`UnicodeError`](unicodeerror/index.md).
