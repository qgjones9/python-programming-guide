# [StreamReaderWriter Objects](https://docs.python.org/3/library/codecs.html#streamreaderwriter-objects)

`codecs.StreamReaderWriter` combines **`StreamReader`** and **`StreamWriter`** on a **single bidirectional stream**. `codecs.open()` returns this type (deprecated 3.14 in favor of `open(encoding=...)`). Built from `codecs.lookup()` reader/writer factories. Reference: [docs.python.org](https://docs.python.org/3/library/codecs.html#streamreaderwriter-objects).

---

## Constructor

```text
StreamReaderWriter(stream, Reader, Writer, errors='strict')
```

| Argument | Role |
|----------|------|
| `stream` | Underlying file-like object (binary mode for text encodings) |
| `Reader` / `Writer` | Factory callables from `CodecInfo` |
| `errors` | Shared error handler for both directions |

The instance exposes **both** reader and writer methods and forwards other attributes to `stream`.

```python
# Goal: build StreamReaderWriter manually (same idea as codecs.open)
import codecs
import io

info = codecs.lookup("utf-8")
buf = io.BytesIO()
rw = codecs.StreamReaderWriter(buf, info.streamreader, info.streamwriter, errors="strict")
rw.write("ping")
buf.seek(0)
assert rw.read() == "ping"
```

---

## Behavior notes

| Topic | Detail |
|-------|--------|
| Newline handling | **No** automatic `\n` ↔ `\r\n` translation (unlike text mode `open`) |
| Mode | Underlying file opened **binary** when `encoding` is set |
| Deprecation | Prefer `open(path, encoding='utf-8')` for new code |

```python
# Goal: preferred modern replacement
import io

buf = io.BytesIO()
tw = io.TextIOWrapper(buf, encoding="utf-8", newline="\n")
tw.write("hello\n")
tw.flush()
assert buf.getvalue() == b"hello\n"
tw.detach()
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Migrate off **`codecs.open()`** | Deprecated; `open` handles encoding |
| Keep stream at correct offset | Reader/writer share one cursor |
| Specify **`errors`** explicitly | Same defaults as other codec APIs |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Expecting universal-newline mode | Open text wrapper with `newline=` if needed |
| Writing after read without **`seek`** | Mixed RW on BytesIO needs position management |
| Using `'U'` mode | Removed in 3.11 |
