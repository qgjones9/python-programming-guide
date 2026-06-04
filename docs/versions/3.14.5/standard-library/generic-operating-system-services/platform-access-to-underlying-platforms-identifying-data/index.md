# [platform — Access to underlying platform’s identifying data](https://docs.python.org/3/library/platform.html)

The [`platform`](https://docs.python.org/3/library/platform.html) module reports **OS and Python build metadata**: system name, release, machine hardware, interpreter version, and (on Linux) `/etc/os-release` fields. Use it for installers, bug reports, and feature gates — not for security decisions. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/platform.html).

Related: [`sys`](../../python-runtime-services/sys-system-specific-parameters-and-functions/index.md) (`sys.platform`, `sys.version`); [`os`](../os-miscellaneous-operating-system-interfaces/index.md) `uname()` for kernel-level names.

---

## Cross-platform APIs — overview

| Function | Returns | Notes |
|----------|---------|-------|
| `platform.system()` | OS name (`Linux`, `Windows`, `Darwin`, …) | User-facing on mobile |
| `platform.release()` | OS release string | May be empty |
| `platform.version()` | Build/version detail | Human-oriented |
| `platform.machine()` | Hardware type (`x86_64`, `aarch64`, …) | |
| `platform.node()` | Network name | May be unqualified |
| `platform.platform()` | Single summary string | `aliased`, `terse` kwargs |
| `platform.uname()` | `namedtuple` of six fields | Differs from `os.uname()` field names |
| `platform.python_version()` | `"major.minor.patch"` | Always includes patch |
| `platform.python_implementation()` | `CPython`, `PyPy`, … | |

---

## Python build info — [Cross platform](https://docs.python.org/3/library/platform.html#cross-platform)

| Function | Role |
|----------|------|
| `python_version_tuple()` | `('3', '14', '5')` strings |
| `python_build()` | `(buildno, builddate)` |
| `python_compiler()` | Compiler used to build CPython |

```python
# Goal: read Python version tuple and implementation
import platform

major, minor, patch = platform.python_version_tuple()
assert major.isdigit() and minor.isdigit()
assert platform.python_implementation() in {"CPython", "PyPy", "Jython", "IronPython", "GraalVM"}
```

```python
# Goal: human-readable platform string
import platform

summary = platform.platform()
assert isinstance(summary, str) and len(summary) > 0
```

```python
# Goal: detect 64-bit interpreter via sys.maxsize idiom
import sys

is_64bit = sys.maxsize > 2**32
assert isinstance(is_64bit, bool)
```

---

## Linux distro detection — [Linux platforms](https://docs.python.org/3/library/platform.html#linux-platforms)

| Function | Role |
|----------|------|
| `freedesktop_os_release()` | Parse `/etc/os-release` → `dict` (3.10+) |
| Keys | `ID`, `VERSION_ID`, `PRETTY_NAME`, optional `ID_LIKE` |

Use **`ID`** / **`ID_LIKE`** for programmatic checks; **`PRETTY_NAME`** for display.

```python
# Goal: read os-release when available (Linux)
import platform

try:
    info = platform.freedesktop_os_release()
    assert "ID" in info
except OSError:
    pass  # Expected off Linux or in minimal containers
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`sys.platform`** for quick checks | Stable prefixes (`linux`, `win32`, `darwin`) |
| Use **`ID_LIKE`** for distro families | Covers derivatives (e.g. RHEL-like) |
| Call **`invalidate_caches()`** (3.14+) after hostname changes | Refreshes cached `uname` data |
| Do not **parse `platform.platform()`** | Not machine-stable; use specific APIs |
| Log **`python_version()` + `machine()`** in support bundles | Enough for most triage |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`platform.system()` vs `os.uname().sysname`** | Different strings on some OSes | Pick one API per check |
| **`architecture()` needs `file` command** | Empty linkage on minimal containers | Fall back to `sys.maxsize` |
| **`freedesktop_os_release` on Android** | Often raises `OSError` | Catch and use `android_ver()` (3.13+) |
| **`processor` may equal `machine`** | Empty or duplicate on many Unixes | Do not rely on CPU marketing names |
| **`java_ver` deprecated (3.13+)** | Removed in 3.15 | Avoid for new code |
