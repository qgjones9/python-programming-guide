# [test.support.os_helper — Utilities for os tests](https://docs.python.org/3/library/test.html#module-test.support.os_helper)

`test.support.os_helper` provides **filesystem and environment helpers** for CPython OS tests: canonical temp filenames (`TESTFN`), working-directory changes, symlink capability probes, and `EnvironmentVarGuard`. Canonical reference: [test.html#module-test.support.os_helper](https://docs.python.org/3/library/test.html#module-test.support.os_helper).

---

## Purpose

OS-facing tests create and destroy files repeatedly. Shared conventions (`TESTFN`, `change_cwd`, `unlink`) reduce collisions and platform-specific failures across the regression suite.

---

## Key symbols

| Name | Role |
|------|------|
| `TESTFN`, `TESTFN_NONASCII`, … | Basenames for temp files |
| `EnvironmentVarGuard` | Save/restore environment variables |
| `change_cwd(path)` | Context manager switching cwd |
| `can_symlink()`, `can_chmod()` | Feature probes for `@unittest.skipUnless` |
| `FakePath` | Path-like object for mock paths |
| `unlink(path)` | Remove file with retry on Windows |

---

## Example — EnvironmentVarGuard

```python
import os
import test.support.os_helper as oh

key = "PYTEST_OS_HELPER_DEMO"
with oh.EnvironmentVarGuard() as env:
    env.set(key, "1")
    assert os.environ[key] == "1"
assert key not in os.environ or os.environ.get(key) != "1"
```

---

## Example — temp file with TESTFN

```python
import os
import tempfile
import test.support.os_helper as oh

with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, oh.TESTFN)
    with open(path, "w", encoding="utf-8") as f:
        f.write("data")
    assert os.path.isfile(path)
    oh.unlink(path)
    assert not os.path.exists(path)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Create `TESTFN` under a **TemporaryDirectory** | Avoids littering cwd |
| Use `EnvironmentVarGuard` instead of manual del/set | Restores even on exceptions |
| Check `can_symlink()` before symlink tests | Skips on platforms without symlinks |

---

## See also

- [`os`](https://docs.python.org/3/library/os.html)
- [`test.support`](../testsupport-utilities-for-the-python-test-suite/index.md)
