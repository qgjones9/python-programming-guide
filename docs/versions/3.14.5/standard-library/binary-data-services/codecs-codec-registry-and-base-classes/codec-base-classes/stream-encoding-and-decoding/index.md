# [Stream Encoding and Decoding](https://docs.python.org/3/library/codecs.html#stream-encoding-and-decoding)

**Stream codecs** wrap binary (or text) **file-like objects** so application code reads/writes **logical** text or transformed bytes while the codec handles encoding/decoding and buffering. `StreamWriter` and `StreamReader` subclass `Codec`; higher-level wrappers combine directions. Reference: [docs.python.org](https://docs.python.org/3/library/codecs.html#stream-encoding-and-decoding).

---

## Class roles

| Class | Direction | Underlying stream |
|-------|-----------|-------------------|
| `StreamWriter` | Encoded bytes → stream | Open for writing |
| `StreamReader` | Stream → decoded text/bytes | Open for reading |
| `StreamReaderWriter` | Both on one stream | Read/write file-like |
| `StreamRecoder` | Transcode between two encodings | Bytes in “file encoding”, app sees “data encoding” |

Factory functions come from `CodecInfo.streamwriter` / `streamreader` or `codecs.getwriter()` / `getreader()`.

```python
# Goal: wrap BytesIO with UTF-8 StreamWriter
import codecs
import io

buf = io.BytesIO()
writer = codecs.getwriter("utf-8")(buf)
writer.write("line\n")
assert buf.getvalue() == b"line\n"
```

---

## Modern alternative

Since Python 3, prefer **`open(path, 'w', encoding='utf-8')`** or **`TextIOWrapper`** around binary streams. `codecs.open()` wraps `StreamReaderWriter` but is **deprecated in 3.14**.

```python
# Goal: TextIOWrapper equivalent to StreamReader
import io

raw = io.BytesIO("café\n".encode("utf-8"))
text_stream = io.TextIOWrapper(raw, encoding="utf-8")
assert text_stream.readline() == "café\n"
text_stream.detach()
```

---

## StreamReader highlights

| Method | Purpose |
|--------|---------|
| `read(size=-1, chars=-1, firstline=False)` | Greedy decode up to byte/char limits |
| `readline(size=None, keepends=True)` | One line with codec-aware newline handling |
| `readlines(sizehint=None, keepends=True)` | All lines |
| `reset()` | Clear codec buffers after errors (no seek) |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`open(encoding=...)`** for files | Newline translation + idiomatic API |
| Call **`reset()`** after decode error recovery | Resync internal buffers |
| Pass **binary** streams to text wrappers | Mixed text/binary modes confuse encoding |
| Close **wrapper** to flush incremental encoders | Underlying buffer may need flush |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [StreamWriter Objects](streamwriter-objects/index.md) | `write`, `writelines`, `reset` |
| [StreamReader Objects](streamreader-objects/index.md) | `read`, `readline`, `readlines` |
| [StreamReaderWriter Objects](streamreaderwriter-objects/index.md) | Combined read/write wrapper |
| [StreamRecoder Objects](streamrecoder-objects/index.md) | Transcoding pipeline |
