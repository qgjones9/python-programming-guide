# [Generic Operating System Services](https://docs.python.org/3/library/allos.html)

The **Generic Operating System Services** chapter groups modules that expose portable (mostly POSIX/C-shaped) interfaces to the host OS: process environment, file descriptors, clocks, stream I/O, structured logging, platform introspection, errno constants, and C-library FFI via [`ctypes`](ctypes-a-foreign-function-library-for-python/index.md). Use [`os`](os-miscellaneous-operating-system-interfaces/index.md) and [`io`](io-core-tools-for-working-with-streams/index.md) for files and streams; [`time`](time-time-access-and-conversions/index.md) for clocks; the [`logging`](logging-logging-facility-for-python/index.md) family for application diagnostics; [`platform`](platform-access-to-underlying-platforms-identifying-data/index.md) and [`errno`](errno-standard-errno-system-symbols/index.md) for identity and error codes. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/allos.html).

Related material: [`pathlib`](../file-and-directory-access/pathlib-object-oriented-filesystem-paths/index.md) and [`shutil`](../file-and-directory-access/shutil-high-level-file-operations/index.md) for higher-level file work; [`subprocess`](../concurrent-execution/subprocess-subprocess-management/index.md) for spawning processes; [`sys`](../python-runtime-services/sys-system-specific-parameters-and-functions/index.md) for interpreter parameters.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`os`](os-miscellaneous-operating-system-interfaces/index.md) | Process environment, files, directories, low-level OS calls |
| [`io`](io-core-tools-for-working-with-streams/index.md) | Text/binary/raw stream base classes and in-memory buffers |
| [`time`](time-time-access-and-conversions/index.md) | Wall clock, monotonic timers, sleep, struct_time |
| [`logging`](logging-logging-facility-for-python/index.md) | Hierarchical loggers, levels, handlers, formatters |
| [`logging.config`](loggingconfig-logging-configuration/index.md) | dictConfig/fileConfig for wiring loggers at startup |
| [`logging.handlers`](logginghandlers-logging-handlers/index.md) | Rotating files, syslog, SMTP, HTTP, queue handlers |
| [`platform`](platform-access-to-underlying-platforms-identifying-data/index.md) | OS name, Python build info, Linux os-release |
| [`errno`](errno-standard-errno-system-symbols/index.md) | Integer errno constants and `errorcode` reverse map |
| [`ctypes`](ctypes-a-foreign-function-library-for-python/index.md) | Call C shared libraries without writing an extension |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Read/write paths, env vars, mkdir, stat | [`os`](os-miscellaneous-operating-system-interfaces/index.md) or [`pathlib`](../file-and-directory-access/pathlib-object-oriented-filesystem-paths/index.md) |
| Explicit text vs binary stream layering | [`io`](io-core-tools-for-working-with-streams/index.md) |
| Measure elapsed time or sleep | [`time.perf_counter`](time-time-access-and-conversions/index.md) / `monotonic` |
| Application or library diagnostics | [`logging.getLogger(__name__)`](logging-logging-facility-for-python/index.md) |
| Load logging from JSON/YAML/INI at startup | [`logging.config.dictConfig`](loggingconfig-logging-configuration/index.md) |
| Log rotation or remote log shipping | [`logging.handlers`](logginghandlers-logging-handlers/index.md) |
| Feature-detect OS or distro in installers | [`platform`](platform-access-to-underlying-platforms-identifying-data/index.md) |
| Compare `OSError.errno` to known codes | [`errno`](errno-standard-errno-system-symbols/index.md) |
| Call a C API from a `.so`/`.dll` | [`ctypes`](ctypes-a-foreign-function-library-for-python/index.md) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **`pathlib.Path`** for path composition | Clearer than string joins; still uses `os` under the hood |
| Pass **`encoding="utf-8"`** on text files | Avoids locale surprises on Windows and in CI |
| Use **`logging.getLogger(__name__)`** per module | Hierarchical names mirror package layout |
| Configure logging **once** at app entry | `basicConfig` or `dictConfig` before other imports log |
| Catch **`OSError`** (not bare `Exception`) for OS calls | Includes `FileNotFoundError`, `PermissionError`, etc. |
| Use **`time.monotonic()`** for intervals | Not affected by NTP or daylight-saving jumps |
| Treat **`ctypes`** as unsafe FFI | No type checking; wrong signatures corrupt memory |

```python
# Goal: portable env lookup and path existence check
import os
from pathlib import Path

home = os.environ.get("HOME") or os.environ.get("USERPROFILE", "")
assert isinstance(home, str)
assert Path(os.getcwd()).is_dir()
```

```python
# Goal: module-level logger with temporary handler
import io
import logging

log = logging.getLogger("demo.os_services")
buf = io.StringIO()
handler = logging.StreamHandler(buf)
handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
log.addHandler(handler)
log.setLevel(logging.INFO)
log.info("ready")
assert "INFO:demo.os_services:ready" in buf.getvalue()
log.removeHandler(handler)
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Mutating **`os.environ`** vs **`putenv`** | External env out of sync | Change `os.environ` mapping, not `putenv` alone |
| **`logging.basicConfig`** after handlers exist | No effect on root logger | Configure before any logging calls |
| Mixing **text and binary** stream writes | `TypeError` on write | Match mode (`"rb"`/`"rt"`) to data type |
| Using **`time.time()`** for benchmarks | Skews when clock adjusts | Prefer `perf_counter()` or `monotonic()` |
| Assuming all **`errno`** symbols exist | `AttributeError` on import | Guard with `getattr(errno, "EXDEV", None)` |
| **`ctypes`** without `restype`/`argtypes` | Wrong return values or crashes | Set prototypes explicitly |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [os — Miscellaneous operating system interfaces](os-miscellaneous-operating-system-interfaces/index.md) | Environment, files, directories, process IDs, scandir |
| [io — Core tools for working with streams](io-core-tools-for-working-with-streams/index.md) | TextIO, BufferedIO, RawIO, StringIO/BytesIO |
| [time — Time access and conversions](time-time-access-and-conversions/index.md) | epoch seconds, struct_time, sleep, clocks |
| [logging — Logging facility for Python](logging-logging-facility-for-python/index.md) | Loggers, levels, handlers, formatters, filters |
| [logging.config — Logging configuration](loggingconfig-logging-configuration/index.md) | dictConfig, fileConfig, listen/reconfigure |
| [logging.handlers — Logging handlers](logginghandlers-logging-handlers/index.md) | RotatingFileHandler, TimedRotatingFileHandler, QueueHandler |
| [platform — Access to underlying platform’s identifying data](platform-access-to-underlying-platforms-identifying-data/index.md) | system(), python_version(), freedesktop_os_release() |
| [errno — Standard errno system symbols](errno-standard-errno-system-symbols/index.md) | EPERM, ENOENT, EEXIST, errorcode map |
| [ctypes — A foreign function library for Python](ctypes-a-foreign-function-library-for-python/index.md) | CDLL, Structure, CFUNCTYPE, pointers |
