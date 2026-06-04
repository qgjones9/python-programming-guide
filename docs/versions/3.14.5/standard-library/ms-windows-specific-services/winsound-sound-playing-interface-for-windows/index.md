# [winsound — Sound-playing interface for Windows](https://docs.python.org/3/library/winsound.html)

The [`winsound`](https://docs.python.org/3/library/winsound.html) module plays **WAV files** and **system alert sounds** on Windows via the `PlaySound` API. It is a thin wrapper—no MP3, no volume mixer control. Windows-only. Full flags remain on [docs.python.org](https://docs.python.org/3/library/winsound.html).

Related: [`msvcrt`](../msvcrt-useful-routines-from-the-ms-vc-runtime/index.md); media playback libraries for cross-platform audio.

---

## Core API — [Sound-playing](https://docs.python.org/3/library/winsound.html#sound-playing)

| Name | Role |
|------|------|
| `winsound.PlaySound(sound, flags)` | Play WAV path, bytes, or alias |
| `winsound.Beep(frequency, duration)` | PC speaker tone (may be emulated) |
| `winsound.MessageBeep(type=...)` | Standard notification sound |
| `winsound.SND_FILENAME` | `sound` is a path |
| `winsound.SND_ALIAS` | `sound` is a system alias (`"SystemAsterisk"`, …) |
| `winsound.SND_ASYNC` | Return immediately; play in background |
| `winsound.SND_NODEFAULT` | Do not fall back if sound missing |

```python
# Goal: platform guard — winsound constants on Windows
import importlib.util
import sys

spec = importlib.util.find_spec("winsound")
if sys.platform == "win32":
    import winsound

    assert spec is not None
    assert winsound.SND_ASYNC != 0
    assert winsound.SND_ALIAS != 0
else:
    assert spec is None
```

---

## Usage patterns (Windows)

```python
# Goal: MessageBeep without blocking (Windows only)
import sys

if sys.platform == "win32":
    import winsound

    winsound.MessageBeep(winsound.MB_ICONASTERISK)
    # Beep frequency Hz, duration ms
    winsound.Beep(440, 100)
```

Play WAV from memory by passing **`bytes`** with `SND_MEMORY` (not shown in minimal guard examples—requires valid RIFF header).

---

## Flag combinations

| Intent | Typical flags |
|--------|---------------|
| Play file asynchronously | `SND_FILENAME \| SND_ASYNC` |
| System alias, no fallback | `SND_ALIAS \| SND_NODEFAULT` |
| Stop current sound | `PlaySound(None, SND_PURGE)` |

---

## Best practices

| Practice | Why |
|----------|-----|
| Combine **`SND_ASYNC`** for UI apps | Default synchronous play blocks |
| Ship **WAV** assets, not MP3 | API is WAV-only |
| Guard all imports on **`win32`** | Module missing on Linux CI |

---

## See also

- [`msvcrt`](../msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) — console feedback alternative (beep-less)
- [`winsound` docs — Platform availability](https://docs.python.org/3/library/winsound.html)
