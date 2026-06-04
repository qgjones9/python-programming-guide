# [MS Windows Specific Services](https://docs.python.org/3/library/windows.html)

The **MS Windows Specific Services** section wraps platform APIs available when CPython is built for **Windows**: CRT helpers (`msvcrt`), the registry (`winreg`), and simple sound playback (`winsound`). These modules are **not importable** on Linux or macOS builds. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/windows.html).

For cross-platform code, guard imports with `sys.platform == "win32"` or `importlib.util.find_spec()`.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`msvcrt`](msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) | Console I/O, locking, heap, low-level CRT on Windows |
| [`winreg`](winreg-windows-registry-access/index.md) | Read/write Windows registry keys and values |
| [`winsound`](winsound-sound-playing-interface-for-windows/index.md) | Play WAV files or system sounds |

---

## Platform availability

| Platform | Behavior |
|----------|----------|
| Windows (`win32`) | All three modules available |
| Linux / macOS | Import raises `ModuleNotFoundError` |

```python
# Goal: detect Windows-only modules at runtime
import importlib.util
import sys

for name in ("msvcrt", "winreg", "winsound"):
    spec = importlib.util.find_spec(name)
    if sys.platform == "win32":
        assert spec is not None, name
    else:
        assert spec is None, name
```

---

## Choosing the right tool

| Task | Module |
|------|--------|
| Read installer config from `HKLM` / `HKCU` | [`winreg`](winreg-windows-registry-access/index.md) |
| Non-blocking console keypress in a CLI | [`msvcrt`](msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) |
| Alert sound in a desktop script | [`winsound`](winsound-sound-playing-interface-for-windows/index.md) |
| Cross-platform terminal UI | Prefer [`curses`-style libraries](../development-tools/index.md) or GUI toolkits—not these modules |

---

## Best practices

| Practice | Why |
|----------|-----|
| Always **guard imports** in shared libraries | Avoid import-time failure on CI Linux runners |
| Close **registry keys** with `CloseKey` or context managers | Prevents handle leaks in long-running services |
| Use **`winsound.SND_ASYNC`** for non-blocking alerts | Default play can block the UI thread |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [msvcrt — Useful routines from the MS VC++ runtime](msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) | Console and CRT helpers |
| [winreg — Windows registry access](winreg-windows-registry-access/index.md) | Registry keys, values, and types |
| [winsound — Sound-playing interface for Windows](winsound-sound-playing-interface-for-windows/index.md) | WAV and system sound playback |
