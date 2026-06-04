# [UnicodeTranslateError](https://docs.python.org/3/library/exceptions.html#UnicodeTranslateError)

Subclass of [`UnicodeError`](../unicodeerror/index.md) raised during **Unicode translation** between codecs (not plain encode/decode). See [docs.python.org](https://docs.python.org/3/library/exceptions.html#UnicodeTranslateError).

---

## When it is raised

| Context | Notes |
|---------|-------|
| `bytes.decode('codec_a').encode('codec_b')` pipeline | Failures may surface as encode/decode errors instead |
| Custom codec `translate` step | Direct **`UnicodeTranslateError`** |

Less common in everyday application code than encode/decode errors.

---

## Demonstrating raise and catch

```python
# Goal: UnicodeTranslateError shares UnicodeError attributes
exc = UnicodeTranslateError('abc', 1, 2, 'invalid code point')
caught = None
try:
    raise exc
except UnicodeTranslateError as err:
    caught = (err.object[err.start:err.end], err.reason)
assert caught == ('b', 'invalid code point')
assert issubclass(UnicodeTranslateError, UnicodeError)
```

---

## Handling patterns

| Pattern | Use when |
|---------|----------|
| `except UnicodeError` | Generic codec pipeline failure |
| `except UnicodeTranslateError` | Custom codec or `codecs` translation step |
| Split encode/decode | Simpler errors from two-step conversion |

Related: [`UnicodeEncodeError`](../unicodeencodeerror/index.md), [`UnicodeDecodeError`](../unicodedecodeerror/index.md).

---

## Best practices

- Prefer catching [`UnicodeError`](../unicodeerror/index.md) unless you know translation is the failing phase.
- Parent: [`UnicodeError`](../unicodeerror/index.md).
