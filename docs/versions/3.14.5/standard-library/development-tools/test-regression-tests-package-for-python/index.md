# [test — Regression tests package for Python](https://docs.python.org/3/library/test.html)

The **`test`** package is CPython's **stdlib regression test suite** (`Lib/test` in source). It is installed with Python so developers can run **`python -m test`** against their build. Application projects normally use [`unittest`](../unittest-unit-testing-framework/index.md) instead. Canonical reference: [test.html](https://docs.python.org/3/library/test.html).

---

## Purpose

The `test` package validates the **interpreter and standard library** across platforms. It provides discovery, regrtest orchestration, and shared helpers under [`test.support`](../testsupport-utilities-for-the-python-test-suite/index.md). Running the full suite takes significant time and may skip tests on unsupported platforms.

---

## Running tests (CLI — not for exec blocks)

| Command | Effect |
|---------|--------|
| `python -m test` | Run the default regression set |
| `python -m test -j 4` | Parallel workers |
| `python -m test test_os` | Run one test module |
| `python -m test -v` | Verbose output |

---

## Package layout (conceptual)

| Area | Contents |
|------|----------|
| `test/test_*.py` | Individual test modules mirroring stdlib areas |
| `test/support/` | Shared utilities imported by many tests |
| `test/regrtest.py` | Main driver (`python -m test`) |

---

## Example — import a support helper from application tests

Third-party projects may reuse **documented** `test.support` utilities (see child pages), but the `test` package itself is not a general application testing framework.

```python
import test.support as support
import test.support.os_helper as os_helper

# verbose is an int flag (0/1) set by regrtest -v
assert support.verbose in (0, 1)
assert isinstance(os_helper.TESTFN, str)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Do not name your app package `test` | Shadows the stdlib driver |
| Use `python -m test` from the built interpreter | Ensures the tested binary matches |
| Expect skips and timeouts on partial platforms | Many tests probe OS-specific behavior |
| Contribute fixes upstream | This tree belongs to CPython development |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [test.support](../testsupport-utilities-for-the-python-test-suite/index.md) | Core helpers: temp files, matchers, timeouts |
| [test.support.socket_helper](../testsupportsocket_helper-utilities-for-socket-tests/index.md) | Socket test fixtures |
| [test.support.script_helper](../testsupportscript_helper-utilities-for-the-python-execution-tests/index.md) | Subprocess interpreter helpers |
| [test.support.bytecode_helper](../testsupportbytecode_helper-support-tools-for-testing-correct-bytecode-generation/index.md) | Bytecode assertion utilities |
| [test.support.threading_helper](../testsupportthreading_helper-utilities-for-threading-tests/index.md) | Thread join helpers |
| [test.support.os_helper](../testsupportos_helper-utilities-for-os-tests/index.md) | Filesystem and environment guards |
| [test.support.import_helper](../testsupportimport_helper-utilities-for-import-tests/index.md) | Fresh import contexts |
| [test.support.warnings_helper](../testsupportwarnings_helper-utilities-for-warnings-tests/index.md) | Warning capture helpers |
