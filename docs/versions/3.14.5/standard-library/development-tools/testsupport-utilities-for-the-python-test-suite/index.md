# [test.support — Utilities for the Python test suite](https://docs.python.org/3/library/test.html#module-test.support)

`test.support` is the **shared utility layer** for CPython's regression tests: temporary file names, platform capability flags, verbose logging, matchers for complex comparisons, and helpers to skip unsupported configurations. Canonical reference: [test.html#module-test.support](https://docs.python.org/3/library/test.html#module-test.support).

---

## Purpose

Stdlib test modules import `test.support` to avoid duplicating **portability checks**, **temp path conventions**, and **timing helpers**. Third-party projects occasionally reuse stable helpers (see child pages), but APIs may change without deprecation policy.

---

## Commonly used symbols

| Symbol | Role |
|--------|------|
| `TESTFN`, `TESTFN_UNDECODABLE`, … | Unique temp file basenames (via [`os_helper`](testsupportos_helper-utilities-for-os-tests/index.md)) |
| `verbose` | Mirrors `-v` regrtest flag |
| `Matcher` | Flexible equality for complex objects |
| `ALWAYS_EQ`, `NEVER_EQ` | Sentinel objects for ordering tests |
| `find_unused_fd` | Locate free file descriptor |
| `suppress_msvcrt_asserts` | Windows CRT noise control |
| `requires_*` decorators | Skip when OS/resource missing |

---

## Example — Matcher for partial dict comparison

```python
import test.support as support

m = support.Matcher()
assert m.matches({"status": "ok", "detail": "ignored"}, status="ok")
assert not m.matches({"status": "fail"}, status="ok")
```

---

## Example — temp filename convention

```python
import test.support.os_helper as oh

name = oh.TESTFN
assert isinstance(name, str)
assert len(name) > 0
# Tests combine TESTFN with temp directories; do not use in production paths
```

---

## Child modules

Specialized helpers live in submodules—each has a local page:

| Module | Focus |
|--------|-------|
| [`socket_helper`](testsupportsocket_helper-utilities-for-socket-tests/index.md) | Ephemeral ports, socket timeouts |
| [`script_helper`](testsupportscript_helper-utilities-for-the-python-execution-tests/index.md) | Spawn `python` subprocesses |
| [`bytecode_helper`](testsupportbytecode_helper-support-tools-for-testing-correct-bytecode-generation/index.md) | Expected bytecode sequences |
| [`threading_helper`](testsupportthreading_helper-utilities-for-threading-tests/index.md) | Thread lifecycle in tests |
| [`os_helper`](testsupportos_helper-utilities-for-os-tests/index.md) | Filesystem and env guards |
| [`import_helper`](testsupportimport_helper-utilities-for-import-tests/index.md) | Clean import contexts |
| [`warnings_helper`](testsupportwarnings_helper-utilities-for-warnings-tests/index.md) | Capture and assert warnings |

---

## See also

- [`test` package overview](test-regression-tests-package-for-python/index.md)
