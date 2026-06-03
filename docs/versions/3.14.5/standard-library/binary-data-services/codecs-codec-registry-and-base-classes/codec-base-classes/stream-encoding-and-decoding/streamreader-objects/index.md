# [StreamReader Objects](https://docs.python.org/3/library/codecs.html#streamreader-objects)

`codecs.StreamReader` reads from a binary (or appropriate) stream and returns **decoded** objects—usually `str` for text encodings. Construct with `codecs.getreader(encoding)(stream, errors='strict')`. Unrecognized attributes forward to the wrapped stream. API on [docs.python.org](https://docs.python.org/3/library/codecs.html#streamreader-objects).

---

## Constructor

| Parameter | Role |
|-----------|------|
| `stream` | File-like object open for reading |
| `errors` | Decoding error handler |

---

## Methods

| Method | Role |
|--------|------|
| `read(size=-1, chars=-1, firstline=False)` | Decode up to byte/character limits; greedy read |
| `readline(size=None, keepends=True)` | Single line; optional stream `read` size cap |
| `readlines(sizehint=None, keepends=True)` | List of lines |
| `reset()` | Clear decoder buffers after errors (no repositioning) |

`firstline=True` allows returning after first line even if later lines have decode errors.

```python
# Goal: StreamReader over in-memory bytes
import codecs
import io

raw = io.BytesIO("line1\nline2\n".encode("utf-8"))
r = codecs.getreader("utf-8")(raw)
assert r.readline() == "line1\n"
assert r.readline(keepends=False) == "line2"
```

```python
# Goal: read with character limit
import codecs
import io

raw = io.BytesIO("abcdef".encode("utf-8"))
r = codecs.getreader("utf-8")(raw)
chunk = r.read(chars=3)
assert chunk == "abc"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`TextIOWrapper`** for new file code | Integrates with `open(encoding=...)` |
| Pass **`sizehint`** to `readlines` for large files | Limits underlying `read()` batch |
| Call **`reset()`** only for error recovery | Not a substitute for `seek` |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Mixing `read()` on raw and wrapped stream | Decode only through reader |
| Assuming **`readlines`** loads entire file | Still bounded by stream EOF |
| **`keepends=False`** stripping custom newlines | Newlines defined by codec decode |
