# [StreamRecoder Objects](https://docs.python.org/3/library/codecs.html#streamrecoder-objects)

`codecs.StreamRecoder` implements **transparent transcoding**: application code reads/writes in a **data encoding** while the underlying stream stores **file encoding** bytes. `codecs.EncodedFile()` is a convenience constructor. Specification on [docs.python.org](https://docs.python.org/3/library/codecs.html#streamrecoder-objects).

---

## Constructor

```text
StreamRecoder(stream, encode, decode, Reader, Writer, errors='strict')
```

| Layer | Role |
|-------|------|
| Frontend `encode` / `decode` | `Codec`-interface functions for app-visible data |
| `Reader` / `Writer` | Stream codecs for backend bytes |
| `stream` | Storage/interchange file-like object |

Typical pattern: Latin-1 file bytes ↔ UTF-8 application text.

```python
# Goal: StreamRecoder stack — decode UTF-8 bytes from a binary buffer
import codecs
import io

backend = io.BytesIO("café".encode("utf-8"))
reader = codecs.getreader("utf-8")(backend)
assert reader.read() == "café"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Document **both** encodings in file format specs | Mislabelled layers corrupt data silently |
| Use for **legacy file migration** | Read old charset, write UTF-8 to new store |
| Close recoder to close backing stream | Ownership transfers on close |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Confusing **data** vs **file** encoding order | Data = what `read()` returns; file = raw bytes |
| Seeking backend without resetting codec state | May desync incremental buffers |
| Transcoding lossy charsets | Characters not in target charset need error policy |
