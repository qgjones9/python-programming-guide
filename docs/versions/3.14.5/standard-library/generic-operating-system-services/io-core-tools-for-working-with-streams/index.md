# [io — Core tools for working with streams](https://docs.python.org/3/library/io.html)

The [`io`](https://docs.python.org/3/library/io.html) module defines Python’s **stream stack**: raw byte I/O, buffered binary I/O, and text I/O with encoding and newline handling. Built-in [`open()`](https://docs.python.org/3/library/functions.html#open) delegates here; in-memory stand-ins are `StringIO` and `BytesIO`. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/io.html).

Related: [`os`](../os-miscellaneous-operating-system-interfaces/index.md) for file descriptors; [`codecs`](../../binary-data-services/codecs-codec-registry-and-base-classes/index.md) for incremental encoders; [`gzip`](../../data-compression-and-archiving/gzip-support-for-gzip-files/index.md) and other wrappers that stack on binary streams.

---

## Stream layers — overview

| Layer | Base class | Data type | Typical source |
|-------|------------|-----------|----------------|
| Text I/O | `TextIOBase` | `str` | `open(..., "rt", encoding="utf-8")` |
| Binary buffered | `BufferedIOBase` | `bytes` | `open(..., "rb")`, `BytesIO` |
| Raw | `RawIOBase` | `bytes` | `open(..., "rb", buffering=0)` |

Concrete file objects implement **read-only**, **write-only**, or **read-write**, and may or may not support **seek**.

---

## Text I/O — [Text I/O](https://docs.python.org/3/library/io.html#text-i-o)

| API | Notes |
|-----|-------|
| `io.StringIO(initial_value='')` | In-memory text stream |
| `io.TextIOWrapper(buffer, encoding=None, …)` | Wraps binary buffer with codec |
| `io.text_encoding(encoding, stacklevel=1)` | PEP 597 helper for library `open` wrappers |

```python
# Goal: round-trip text in memory
import io

buf = io.StringIO()
buf.write("line one\nline two\n")
buf.seek(0)
assert buf.read() == "line one\nline two\n"
```

```python
# Goal: wrap binary buffer as UTF-8 text
import io

raw = io.BytesIO(b"hello\n")
text = io.TextIOWrapper(raw, encoding="utf-8", newline="\n")
assert text.read() == "hello\n"
```

---

## Binary I/O — [Binary I/O](https://docs.python.org/3/library/io.html#binary-i-o)

| API | Notes |
|-----|-------|
| `io.BytesIO(initial_bytes=b'')` | Growable in-memory bytes buffer |
| `BufferedReader` / `BufferedWriter` | Block buffering over raw stream |
| `DEFAULT_BUFFER_SIZE` | Default buffer size (often 8 KiB) |

```python
# Goal: build binary payload incrementally
import io

buf = io.BytesIO()
buf.write(b"\x00\x01")
buf.write(b"\x02")
buf.seek(0)
assert buf.read() == b"\x00\x01\x02"
```

---

## Raw I/O — [Raw I/O](https://docs.python.org/3/library/io.html#raw-i-o)

Raw streams are low-level; application code usually stops at buffered or text layers. Use `buffering=0` only when you need unbuffered access to the OS file descriptor.

---

## Text encoding — [Text Encoding](https://docs.python.org/3/library/io.html#text-encoding)

| Recommendation | Reason |
|----------------|--------|
| Pass **`encoding="utf-8"`** explicitly | Windows default locale is often not UTF-8 |
| Use **`encoding="locale"`** (3.10+) | Opt into current locale deliberately |
| Enable **`-X warn_default_encoding`** | Surfaces implicit locale encoding (PEP 597) |

---

## Best practices

| Practice | Why |
|----------|-----|
| Never **`write(str)`** to binary streams | Raises `TypeError`; encode first |
| Never **`write(bytes)`** to text streams | Same — pick one layer |
| Use **`with open(...)`** context managers | Flushes and closes reliably |
| Prefer **`read()` size limits** or iteration | Avoid loading huge files entirely |
| Reset **`BytesIO`** with **`seek(0)`** before reread | Write position starts at end |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Default encoding on Windows | Mojibake reading UTF-8 JSON/TOML | Always specify `encoding="utf-8"` |
| **`StringIO.getvalue()`** vs **`read()`** | Position affects `read()` | `seek(0)` or use `getvalue()` |
| Detached **`TextIOWrapper`** | Closing wrapper may not close buffer | Use context managers in order |
| Mixing **`\n`** and **`newline=`** | Unexpected universal newline behavior | Match `newline` to file format |
| **`io.open` is builtin `open`** | Alias only — same semantics | Use either interchangeably |
