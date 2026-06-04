# [Wave_read Objects](https://docs.python.org/3/library/wave.html#wave-read-objects)

[`wave.open(..., 'rb')`](https://docs.python.org/3/library/wave.html#wave.open) returns a **`Wave_read`** instance for parsing PCM WAV files. The object exposes header getters, frame reads as **`bytes`**, and limited seeking. It does not decode samples into integers — pair with [`array`](../../../data-types/array-efficient-arrays-of-numeric-values/index.md) or [`struct`](../../../binary-data-services/struct-interpret-bytes-as-packed-binary-data/index.md) for typed views. Parent overview: [wave — Read and write WAV files](../index.md).

---

## Header getters

| Method | Returns |
|--------|---------|
| `getnchannels()` | `1` mono, `2` stereo, … |
| `getsampwidth()` | Sample width in **bytes** (1, 2, 3, or 4 typical) |
| `getframerate()` | Samples per second |
| `getnframes()` | Total audio frames in file |
| `getcomptype()` | `'NONE'` for PCM |
| `getcompname()` | Human label (often `'not compressed'`) |
| `getparams()` | `namedtuple(nchannels, sampwidth, framerate, nframes, comptype, compname)` |

```python
# Goal: inspect header without reading all audio
import io
import wave

buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(48000)
    wf.writeframes(b"\x00\x00" * 200)  # 100 stereo frames

buf.seek(0)
with wave.open(buf, "rb") as rf:
    p = rf.getparams()
    assert (p.nchannels, p.sampwidth, p.framerate) == (2, 2, 48000)
    assert p.nframes == 100
    assert p.comptype == "NONE"
```

---

## Reading frames — [`readframes`](https://docs.python.org/3/library/wave.html#wave.Wave_read.readframes)

`readframes(n)` returns at most **`n`** frames as a **`bytes`** object. Frame size in bytes is `nchannels * sampwidth`. Fewer bytes may be returned near EOF.

```python
# Goal: read in chunks
import io
import wave

samples = b"\x01\x00" * 50 + b"\x02\x00" * 50
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.writeframes(samples)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    first = rf.readframes(30)
    rest = rf.readframes(100)
    assert len(first) == 60
    assert first + rest == samples
```

---

## Position and rewind

`setpos(pos)`, `tell()`, and `rewind()` share a **position** measured in frames (compatible with each other; exact file offset is implementation-defined).

| Method | Role |
|--------|------|
| `tell()` | Current frame index |
| `setpos(pos)` | Jump to frame index `pos` |
| `rewind()` | Same as `setpos(0)` |

```python
# Goal: seek back and reread the same frames
import io
import wave

body = b"\xab\xcd" * 40
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.writeframes(body)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    rf.readframes(10)
    mark = rf.tell()
    chunk_a = rf.readframes(5)
    rf.setpos(mark)
    chunk_b = rf.readframes(5)
    assert chunk_a == chunk_b
    rf.rewind()
    assert rf.tell() == 0
```

---

## Lifecycle — [`close`](https://docs.python.org/3/library/wave.html#wave.Wave_read.close)

`close()` releases the reader. Called automatically when using `with wave.open(...)`. After close, methods on the instance are unsafe.

---

## Deprecated marker methods

| Method | Behavior | Status |
|--------|----------|--------|
| `getmarkers()` | Always returns `None` | Deprecated 3.13, removed 3.15 |
| `getmark(id)` | Raises an error | Deprecated 3.13, removed 3.15 |

These existed only for **`aifc`** compatibility (`aifc` removed in 3.13). Do not use in new code.

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Treating `readframes` output as `int` samples | Parse with `array.array('h')` or `struct` using `getsampwidth()` |
| Assuming `readframes(n)` always returns `n * frame_bytes` | Check length or loop until EOF |
| Confusing **frames** with **bytes** in `setpos` | Position is in audio frames, not byte offset |
| Relying on markers API | Use sidecar metadata files instead |
