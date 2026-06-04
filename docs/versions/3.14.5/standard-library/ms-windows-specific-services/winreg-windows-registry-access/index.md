# [winreg — Windows registry access](https://docs.python.org/3/library/winreg.html)

The [`winreg`](https://docs.python.org/3/library/winreg.html) module reads and writes the **Windows registry**: keys, subkeys, and typed values (`REG_SZ`, `REG_DWORD`, …). Installers, IT scripts, and desktop tools use it to persist settings. The module is **Windows-only**. Full API and value types remain on [docs.python.org](https://docs.python.org/3/library/winreg.html).

Related: [`msvcrt`](../msvcrt-useful-routines-from-the-ms-vc-runtime/index.md); portable config via files or [`configparser`](../../file-formats/configparser-configuration-file-parser/index.md).

---

## Core functions — [Registry Handles](https://docs.python.org/3/library/winreg.html#registry-handles)

| Function | Role |
|----------|------|
| `winreg.OpenKey(hkey, sub_key, ...)` | Open existing key (returns handle) |
| `winreg.CreateKey(hkey, sub_key)` | Create or open key |
| `winreg.QueryValueEx(key, name)` | Read `(value, type)` |
| `winreg.SetValueEx(key, name, type, value)` | Write typed value |
| `winreg.EnumKey(key, index)` | List subkey name by index |
| `winreg.EnumValue(key, index)` | List value name, data, type |
| `winreg.CloseKey(key)` | Release handle |
| `winreg.HKEY_CURRENT_USER`, `HKEY_LOCAL_MACHINE`, … | Root hive constants |

```python
# Goal: platform guard — winreg hive constants on Windows only
import importlib.util
import sys

spec = importlib.util.find_spec("winreg")
if sys.platform == "win32":
    import winreg

    assert spec is not None
    assert winreg.HKEY_CURRENT_USER == 0x80000001
    assert winreg.REG_SZ == 1
else:
    assert spec is None
```

---

## Typical read pattern (Windows)

```python
# Goal: read Python install path from registry (Windows only)
import sys

if sys.platform == "win32":
    import winreg

    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Python\PythonCore",
    ) as key:
        # Enumerate installed versions; structure varies by installer
        try:
            sub = winreg.EnumKey(key, 0)
            assert isinstance(sub, str)
        except OSError:
            pass  # no subkeys on minimal installs
```

---

## Value types

| Constant | Python type |
|----------|-------------|
| `REG_SZ` / `REG_EXPAND_SZ` | `str` |
| `REG_DWORD` / `REG_QWORD` | `int` |
| `REG_BINARY` | `bytes` |
| `REG_MULTI_SZ` | `list` of `str` |

Always pass the correct **`type`** to `SetValueEx`; wrong types corrupt the value for native readers.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`with winreg.OpenKey(...)`** (3.2+) | Closes handles on exit |
| Prefer **`QueryValueEx`** over legacy `QueryValue` | Preserves type information |
| Avoid writing **`HKEY_LOCAL_MACHINE`** without elevation | Requires admin rights |
| Mirror critical settings to **files** for portability | Registry has no Linux equivalent |

---

## See also

- [`msvcrt`](../msvcrt-useful-routines-from-the-ms-vc-runtime/index.md) — Windows CRT helpers
- [`configparser`](../../file-formats/configparser-configuration-file-parser/index.md) — cross-platform INI files
