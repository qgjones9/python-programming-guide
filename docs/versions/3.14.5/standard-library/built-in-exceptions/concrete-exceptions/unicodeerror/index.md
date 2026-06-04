# [UnicodeError](https://docs.python.org/3/library/exceptions.html#UnicodeError)

Subclass of [`ValueError`](../valueerror/index.md) for **Unicode encoding, decoding, or translation** failures. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#UnicodeError).

---

## When it is raised

| Phase | Subclass |
|-------|----------|
| str → bytes | [`UnicodeEncodeError`](../unicodeencodeerror/index.md) |
| bytes → str | [`UnicodeDecodeError`](../unicodedecodeerror/index.md) |
| Codec translation | [`UnicodeTranslateError`](../unicodetranslateerror/index.md) |

Any of these inherit the shared attributes below.

---

## Shared attributes

| Attribute | Meaning |
|-----------|----------|
| `encoding` | Codec name |
| `reason` | Short description |
| `object` | Object being processed |
| `start`, `end` | Slice of invalid data: `object[start:end]` |

---

## Subclass roles

| Type | Phase |
|------|-------|
| [`UnicodeEncodeError`](../unicodeencodeerror/index.md) | Encoding str → bytes |
| [`UnicodeDecodeError`](../unicodedecodeerror/index.md) | Decoding bytes → str |
| [`UnicodeTranslateError`](../unicodetranslateerror/index.md) | Codec-to-codec translation |

---

## Demonstrating raise and catch

```python
# Goal: bad UTF-8 bytes raise UnicodeDecodeError (UnicodeError subclass)
caught = None
try:
    b'\xff\xfe'.decode('utf-8')
except UnicodeError as exc:
    caught = (type(exc).__name__, exc.encoding)
assert caught == ('UnicodeDecodeError', 'utf-8')
assert issubclass(UnicodeError, ValueError)
```

---

## Sections in this repo

- [UnicodeEncodeError](../unicodeencodeerror/index.md)
- [UnicodeDecodeError](../unicodedecodeerror/index.md)
- [UnicodeTranslateError](../unicodetranslateerror/index.md)

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except UnicodeError` | Direction unknown; log `encoding` and `reason` |
| Catch specific subclass | Known encode vs decode path |
| `errors='replace'` / `'surrogateescape'` | Controlled data loss or binary round-trip |

Related: [`ValueError`](../valueerror/index.md) (non-Unicode bad values).

---

## Best practices

- Use `errors='replace'` or `'ignore'` only when data loss is acceptable—document the choice.
- Catch specific subclasses when you know the direction (encode vs decode).
