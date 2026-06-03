# [StreamWriter Objects](https://docs.python.org/3/library/codecs.html#streamwriter-objects)

`codecs.StreamWriter` subclasses `Codec` and writes **encoded output** to a wrapped stream. Construct with `codecs.getwriter(encoding)(stream, errors='strict')`. The writer **delegates** unknown attributes to the underlying file object. Details on [docs.python.org](https://docs.python.org/3/library/codecs.html#streamwriter-objects).

---

## Constructor

| Parameter | Role |
|-----------|------|
| `stream` | File-like object open for writing (binary for text encodings) |
| `errors` | Error handler name; stored as `.errors` |

---

## Methods

| Method | Role |
|--------|------|
| `write(object)` | Encode and write object to stream |
| `writelines(list)` | Encode and write each string (concatenated via `write`) |
| `reset()` | Clear codec buffers for a clean append state |

Bytes-to-bytes codecs may not support `writelines`.

```python
# Goal: StreamWriter on BytesIO
import codecs
import io

buf = io.BytesIO()
w = codecs.getwriter("utf-8")(buf)
w.write("α")
w.write("β")
assert buf.getvalue() == "αβ".encode("utf-8")
```

```python
# Goal: switch error handler via attribute
import codecs
import io

buf = io.BytesIO()
w = codecs.getwriter("ascii")(buf, errors="replace")
w.errors = "backslashreplace"
w.write("\u2665")
assert b"\\u2665" in buf.getvalue()
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Flush/close underlying stream when done | Encoders may buffer |
| Use **`errors`** appropriate for logs vs protocols | `'replace'` hides data issues |
| Prefer **`TextIOWrapper.write`** for new code | Same role, better integration |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Opening stream in text mode | Pass binary `wb` stream to UTF-8 writer |
| Huge **`writelines`** iterables | Not supported for infinite iterators |
| Expecting **`reset()`** to truncate file | Only clears codec state, not stream position |
