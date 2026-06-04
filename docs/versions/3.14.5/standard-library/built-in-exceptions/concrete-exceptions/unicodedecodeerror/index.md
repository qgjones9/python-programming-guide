# [UnicodeDecodeError](https://docs.python.org/3/library/exceptions.html#UnicodeDecodeError)

Subclass of [`UnicodeError`](../unicodeerror/index.md) raised during **Unicode decoding** (bytes → str). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#UnicodeDecodeError).

---

## When it is raised

| Cause | Example |
|-------|----------|
| Invalid byte sequence for codec | Lone UTF-8 continuation byte |
| Truncated multibyte sequence | File cut mid-character |

---

## Demonstrating raise and catch

```python
# Goal: invalid UTF-8 raises UnicodeDecodeError with byte slice info
bad = b'\xc3\x28'
caught = None
try:
    bad.decode('utf-8')
except UnicodeDecodeError as exc:
    caught = (exc.encoding, bad[exc.start:exc.end])
assert caught[0] == 'utf-8'
assert caught[1] == b'\xc3'
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `decode('utf-8', errors='replace')` | Display or log corrupted bytes without crashing |
| `except UnicodeDecodeError` | Reject upload with “invalid UTF-8” message |
| Catch [`UnicodeError`](../unicodeerror/index.md) | Either encode or decode direction is unknown |

Related: [`UnicodeEncodeError`](../unicodeencodeerror/index.md), [`ValueError`](../valueerror/index.md).

---

## Best practices

- Open text files with explicit `encoding='utf-8'` (3.10+ defaults help but be explicit in libraries).
- Log `exc.object[exc.start:exc.end]` when debugging corrupted input.
- Parent: [`UnicodeError`](../unicodeerror/index.md).
