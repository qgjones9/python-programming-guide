# [wave — Read and write WAV files](https://docs.python.org/3/library/wave.html)

The [`wave`](https://docs.python.org/3/library/wave.html) module reads and writes **WAV** (Waveform Audio) files containing **uncompressed PCM** samples. It is a thin wrapper around the RIFF WAVE container — not a general audio codec library. Compressed WAV variants and non-PCM formats raise [`wave.Error`](https://docs.python.org/3/library/wave.html#wave.Error). Since 3.12, **`WAVE_FORMAT_EXTENSIBLE`** headers work when the extended subtype is PCM.

Modes are **`'rb'`** (read → [`Wave_read`](wave-read-objects/index.md)) and **`'wb'`** (write → [`Wave_write`](wave-write-objects/index.md)). There is no read/write mode. Full method lists remain on [docs.python.org](https://docs.python.org/3/library/wave.html).

---

## `wave.open()` — [Module functions](https://docs.python.org/3/library/wave.html#wave.open)

| Argument | Role |
|----------|------|
| `file` | Path string or file-like object |
| `mode` | `'rb'` or `'wb'`; defaults to `file.mode` for file-like objects |

| Mode | Returns | Notes |
|------|---------|-------|
| `'rb'` | `Wave_read` | Parses header; `readframes(n)` returns `bytes` |
| `'wb'` | `Wave_write` | Set channel/rate/width before writing frames |

`open()` supports **`with`** statements — `close()` runs on block exit. If you pass a file-like object, **`wave` does not close it**; the caller owns the stream.

```python
# Goal: round-trip PCM mono WAV through BytesIO
import io
import wave

payload = b"\x00\x00" * 25  # 25 frames, 16-bit mono (2 bytes per frame)
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.writeframes(payload)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    assert rf.getnchannels() == 1
    assert rf.getsampwidth() == 2
    assert rf.getframerate() == 8000
    assert rf.getcomptype() == "NONE"
    assert rf.readframes(25) == payload
```

```python
# Goal: open by filesystem path (write then read)
import os
import tempfile
import wave

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "tone.wav")
    with wave.open(path, "wb") as wf:
        wf.setparams((1, 2, 44100, 0, "NONE", "not compressed"))
        wf.writeframes(b"\x00\x00" * 100)
    with wave.open(path, "rb") as rf:
        params = rf.getparams()
        assert params.nchannels == 1 and params.framerate == 44100
        assert params.nframes == 100
```

---

## `wave.Error`

Raised when the file violates the WAV spec or the implementation cannot proceed — wrong compression type, invalid parameter changes after writing, or bad markers API usage.

```python
# Goal: changing parameters after writeframes raises wave.Error
import io
import wave

buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.writeframes(b"\x00\x00")
    try:
        wf.setframerate(16000)
    except wave.Error:
        pass
    else:
        raise AssertionError("expected wave.Error")
```

---

## Read vs write workflows

| Step | Read (`'rb'`) | Write (`'wb'`) |
|------|---------------|----------------|
| Open | `wave.open(path, "rb")` | `wave.open(path, "wb")` |
| Metadata | `get*()` / `getparams()` | `set*()` / `setparams()` before frames |
| Audio data | `readframes(n)` | `writeframes(data)` or `writeframesraw(data)` |
| Seek | `setpos`, `tell`, `rewind` | `tell` only (position semantics differ) |
| Close | Updates nothing on disk | Patches `nframes` in header when seekable |

On **unseekable** output streams, set an accurate **`nframes`** before the first frame write (via `setnframes` or `setparams`), then prefer **`writeframesraw()`**, or pass all audio in one **`writeframes()`** call so the module can count frames.

---

## Limitations

| Limitation | Detail |
|------------|--------|
| PCM only | No ADPCM, MP3-in-WAV, or float32 extended formats unless PCM extensible |
| No simultaneous RW | Open once per direction |
| Deprecated markers | `getmarkers` / `getmark` (aifc compatibility) deprecated since 3.13, removal in 3.15 |
| Sample inspection | Returns raw **bytes** — interpret with `array`, `struct`, or numpy |

```python
# Goal: decode 16-bit little-endian samples from readframes output
import array
import io
import wave

raw = (array.array("h", [0, 1000, -1000, 32767])).tobytes()
buf = io.BytesIO()
with wave.open(buf, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(8000)
    wf.writeframes(raw)

buf.seek(0)
with wave.open(buf, "rb") as rf:
    data = rf.readframes(4)
samples = array.array("h")
samples.frombytes(data)
assert list(samples) == [0, 1000, -1000, 32767]
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Wave_read Objects](wave-read-objects/index.md) | Reading frames, `getparams`, seek/rewind |
| [Wave_write Objects](wave-write-objects/index.md) | Header setup, `writeframes`, unseekable streams |
