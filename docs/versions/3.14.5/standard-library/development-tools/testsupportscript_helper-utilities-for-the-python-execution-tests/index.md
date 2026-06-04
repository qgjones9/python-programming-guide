# [test.support.script_helper — Utilities for the Python execution tests](https://docs.python.org/3/library/test.html#module-test.support.script_helper)

`test.support.script_helper` runs **Python interpreter subprocesses** with controlled arguments, environment, and expected exit codes. CPython's tests for `-c`, `-m`, and script execution use these helpers. Canonical reference: [test.html#module-test.support.script_helper](https://docs.python.org/3/library/test.html#module-test.support.script_helper).

---

## Purpose

When validating **command-line behavior**, in-process calls are insufficient—you need a fresh interpreter. `script_helper` wraps `subprocess` with conventions matching regrtest (suppress noise, normalize paths, assert return codes).

---

## Key functions

| Name | Role |
|------|------|
| `assert_python_ok(*args, **kw)` | Run `sys.executable` expecting exit 0 |
| `assert_python_failure(*args, **kw)` | Expect non-zero exit |
| `kill_python` | Terminate a spawned Popen helper |

---

## Example — run code in subprocess

```python
import test.support.script_helper as sh

rc, out, err = sh.assert_python_ok("-c", "print('hello')")
assert rc == 0
assert b"hello" in out
```

---

## Example — expect failure exit code

```python
import test.support.script_helper as sh

rc, out, err = sh.assert_python_failure("-c", "raise SystemExit(2)")
assert rc == 2
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass **list args** without shell interpolation | Avoids injection and quoting bugs |
| Capture `out` / `err` bytes | Subprocess output is binary |
| Use for CLI tests only | Heavy compared to in-process unit tests |

---

## See also

- [`subprocess`](https://docs.python.org/3/library/subprocess.html)
- [`test.support`](testsupport-utilities-for-the-python-test-suite/index.md)
