# [Multimedia Services](https://docs.python.org/3/library/mm.html)

Python’s **Multimedia Services** chapter groups small, optional standard-library modules aimed at audio and color workflows. They ship with CPython when the build includes them, but unlike core I/O modules they are not always needed for everyday scripting. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/mm.html); this hub orients you to each module and when to reach for it.

For production audio pipelines (MP3, AAC, resampling, device I/O), third-party packages such as **soundfile**, **pydub**, or **PyAudio** usually replace or wrap these primitives. For image/video, look elsewhere in the library ([`mimetypes`](../internet-data-handling/mimetypes-map-filenames-to-mime-types/index.md), [`base64`](../internet-data-handling/base64-base16-base32-base64-base85-data-encodings/index.md)) or external libraries.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`wave`](wave-read-and-write-wav-files/index.md) | Read and write uncompressed PCM **WAV** files |
| [`colorsys`](colorsys-conversions-between-color-systems/index.md) | Convert RGB values to/from HSV, HLS, and YIQ |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Inspect or slice a `.wav` file without extra dependencies | [`wave.open()`](wave-read-and-write-wav-files/index.md) in `'rb'` mode |
| Generate a simple tone or export raw PCM as WAV | [`wave`](wave-read-and-write-wav-files/index.md) in `'wb'` mode on a seekable stream |
| Convert UI color picker values between RGB and HSV/HLS | [`colorsys`](colorsys-conversions-between-color-systems/index.md) (float coordinates 0–1) |
| Compress audio (MP3, FLAC, Ogg) | External library — `wave` supports **uncompressed PCM only** |
| Read/write AIFF, Sun `.au`, or other containers | Not in this section — use specialized libraries |

---

## Cross-cutting notes

| Topic | Detail |
|-------|--------|
| **Availability** | Modules are optional at install time; import normally succeeds on standard CPython builds |
| **WAV scope** | PCM only; `WAVE_FORMAT_EXTENSIBLE` supported since 3.12 when the extended format is PCM |
| **Color coordinates** | `colorsys` uses **floats**; divide 8-bit channel bytes by 255 before calling |
| **Seekable streams** | `wave` can patch header `nframes` on seekable outputs; unseekable streams need accurate frame counts up front |

```python
# Goal: confirm both multimedia modules import on this interpreter
import colorsys
import wave

assert hasattr(wave, "open")
assert hasattr(colorsys, "rgb_to_hsv")
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [wave — Read and write WAV files](wave-read-and-write-wav-files/index.md) | `wave.open`, PCM WAV read/write, `Wave_read` / `Wave_write` |
| [colorsys — Conversions between color systems](colorsys-conversions-between-color-systems/index.md) | RGB ↔ HSV, HLS, YIQ conversion helpers |
