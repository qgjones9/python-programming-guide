# [Wave_write Objects](https://docs.python.org/3/library/wave.html#wave-write-objects)

[`wave.open(..., 'wb')`](https://docs.python.org/3/library/wave.html#wave.open) returns a **`Wave_write`** instance for building PCM WAV files. Configure channels, sample width, and frame rate **before** writing audio. On **seekable** streams the module updates the **`nframes`** header field at `close()`; on **unseekable** streams you must declare the frame count up front. Parent overview: [wave — Read and write WAV files](../index.md).

---

## Parameter setters and getters

| Setter | Getter | Meaning |
|--------|--------|---------|
| `setnchannels(n)` | `getnchannels()` | Channel count |
| `setsampwidth(n)` | `getsampwidth()` | Bytes per sample |
| `setframerate(n)` | `getframerate()` | Sample rate (non-int rounded since 3.2) |
| `setnframes(n)` | `getnframes()` | Frames to write (may be corrected on close) |
| `setcomptype(type, name)` | `getcomptype()`, `getcompname()` | Only `'NONE'` / `'not compressed'` supported |
| `setparams(tuple)` | `getparams()` | Bulk set/get matching `getparams()` on read side |

Tuple form: `(nchannels, sampwidth, framerate, nframes, comptype, compname)`.

```python
# Goal: setparams then writeframes
import io
import wave

pcm = b"\x00\x00" * 10  # 10 frames, 16-bit mono
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setparams((1, 2, 22050, 0, "NONE", "not compressed"))
    wf.writeframes(pcm)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    assert rf.getnframes() == 10
    assert rf.readframes(10) == pcm
```

---

## Writing frame data

| Method | Updates `nframes` in header | When to use |
|--------|----------------------------|-------------|
| `writeframes(data)` | Yes (counts bytes / frame size) | Normal path; one or many calls on seekable files |
| `writeframesraw(data)` | No | Unseekable streams after explicit `setnframes` |

Both accept any **bytes-like** object (since 3.4). **Invalid:** call any `set*()` after `writeframes()` or `writeframesraw()` — raises [`wave.Error`](https://docs.python.org/3/library/wave.html#wave.Error).

```python
# Goal: writeframesraw with preset nframes on seekable buffer
import io
import wave

frames = 8
frame_bytes = b"\x00\x00"
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.setnframes(frames)
    wf.writeframesraw(frame_bytes * frames)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    assert rf.getnframes() == frames
```

```python
# Goal: multiple writeframes calls on seekable stream
import io
import wave

buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(1)
    wf.setframerate(8000)
    wf.writeframes(b"\x80" * 5)
    wf.writeframes(b"\x7f" * 5)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    assert rf.getnframes() == 10
    assert len(rf.readframes(10)) == 10
```

---

## Seekable vs unseekable output

| Stream type | Header `nframes` | Recommended API |
|-------------|------------------|-----------------|
| Seekable (`BytesIO`, regular file) | Patched at `close()` from bytes written | `writeframes()` freely |
| Unseekable (pipe, socket) | Must match bytes written or `close()` errors | `setnframes` + `writeframesraw`, or single `writeframes` |

```python
# Goal: unseekable stream — accurate nframes before raw writes
import io
import wave

class UnseekableBuffer(io.BufferedIOBase):
    def __init__(self):
        self._chunks = []

    def writable(self):
        return True

    def seekable(self):
        return False

    def write(self, b):
        self._chunks.append(bytes(b))
        return len(b)

    def getvalue(self):
        return b"".join(self._chunks)

sink = UnseekableBuffer()
n = 4
with wave.open(sink, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.setnframes(n)
    wf.writeframesraw(b"\x00\x00" * n)

# Parse the WAV bytes produced on the unseekable sink
out = io.BytesIO(sink.getvalue())
with wave.open(out, "rb") as rf:
    assert rf.getnframes() == n
```

---

## `tell()` and `close()`

`tell()` returns a position in the output stream (same caveats as on read objects). `close()` finalizes the header and closes the file **only if `wave` opened it by path**. For file-like objects, the caller closes the underlying stream.

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Wrong `nframes` on pipes | Precompute frame count; use `writeframesraw` |
| Calling `setframerate` after first frame | Set all parameters first |
| Expecting compression | Only `'NONE'` PCM — use external encoders for compression |
| Forgetting mono frame size | Total bytes per frame = `nchannels * sampwidth` |
| 24-bit (`sampwidth=3`) interop | Less common; verify consumer support |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`with wave.open(...)`** | Ensures header finalize and `close()` |
| Match **`sampwidth`** to sample encoding | 2 bytes ↔ 16-bit linear PCM |
| Prefer **`writeframes`** on disk files | Header auto-fixes partial writes |
| Validate output with **`Wave_read`** | Quick round-trip test in tests or REPL |
