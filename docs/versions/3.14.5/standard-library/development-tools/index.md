# [Development Tools](https://docs.python.org/3/library/development.html)

The **Development Tools** section of the standard library covers **type hints**, **documentation helpers**, **development-mode safety checks**, and the **testing stack** (`doctest`, `unittest`, `unittest.mock`, and the internal `test` package). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/development.html); these notes distill common workflows and link to local chapter pages.

---

## Module overview

| Module / topic | Primary use |
|----------------|-------------|
| [`typing`](typing-support-for-type-hints/index.md) | Static type annotations, generics, protocols, `TypedDict`, and runtime helpers |
| [`pydoc`](pydoc-documentation-generator-and-online-help-system/index.md) | CLI and browser help for modules, classes, and functions |
| [Python Development Mode](python-development-mode/index.md) | Extra runtime checks via `-X dev` or `PYTHONDEVMODE` |
| [`doctest`](doctest-test-interactive-python-examples/index.md) | Executable examples embedded in docstrings and text files |
| [`unittest`](unittest-unit-testing-framework/index.md) | xUnit-style test cases, suites, and discovery |
| [`unittest.mock`](unittestmock-mock-object-library/index.md) | Test doubles, patching, and autospec |
| [`test`](test-regression-tests-package-for-python/index.md) | CPython's own regression test package (includes `test.support` helpers) |

---

## Typical workflows

| Goal | Start here |
|------|------------|
| Annotate a public API for type checkers | [`typing`](typing-support-for-type-hints/index.md) + `from __future__ import annotations` |
| Run examples in docstrings as tests | [`doctest`](doctest-test-interactive-python-examples/index.md) |
| Structure unit tests with setup/teardown | [`unittest`](unittest-unit-testing-framework/index.md) |
| Replace network or filesystem dependencies in tests | [`unittest.mock`](unittestmock-mock-object-library/index.md) |
| Catch resource leaks and deprecation noise locally | [Development Mode](python-development-mode/index.md) |

```python
# Goal: combine typing hints with a doctest-friendly pure function
def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Return value bounded to [low, high].

    >>> clamp(1.5)
    1.0
    >>> clamp(-0.1, high=10)
    0.0
    """
    return max(low, min(value, high))

assert clamp(1.5) == 1.0
assert clamp(-0.1, high=10) == 0.0
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [typing — Support for type hints](typing-support-for-type-hints/index.md) | Generics, unions, protocols, `TypeVar`, `Literal`, and runtime introspection |
| [pydoc — Documentation generator and online help system](pydoc-documentation-generator-and-online-help-system/index.md) | `help()`, `pydoc` CLI, HTML rendering, keyword search |
| [Python Development Mode](python-development-mode/index.md) | `-X dev`, eager warnings, debug hooks, and allocator checks |
| [doctest — Test interactive Python examples](doctest-test-interactive-python-examples/index.md) | Docstring tests, `DocTestSuite`, and comparison flags |
| [unittest — Unit testing framework](unittest-unit-testing-framework/index.md) | `TestCase`, fixtures, assertions, discovery, and runners |
| [unittest.mock — mock object library](unittestmock-mock-object-library/index.md) | `Mock`, `MagicMock`, `patch`, `create_autospec`, and call tracking |
| [unittest.mock — getting started](unittestmock-getting-started/index.md) | Worked examples: patching, autospec, and side effects |
| [test — Regression tests package for Python](test-regression-tests-package-for-python/index.md) | CPython's `Lib/test` tree and how to run stdlib tests |
| [test.support — Utilities for the Python test suite](testsupport-utilities-for-the-python-test-suite/index.md) | Shared helpers: temp dirs, matchers, timeouts, and platform skips |
| [test.support.socket_helper — Utilities for socket tests](testsupportsocket_helper-utilities-for-socket-tests/index.md) | Ephemeral ports, loopback helpers, and socket test fixtures |
| [test.support.script_helper — Utilities for the Python execution tests](testsupportscript_helper-utilities-for-the-python-execution-tests/index.md) | Spawn interpreter subprocesses with controlled flags |
| [test.support.bytecode_helper — Support tools for testing correct bytecode generation](testsupportbytecode_helper-support-tools-for-testing-correct-bytecode-generation/index.md) | Assert expected bytecode sequences in compiler tests |
| [test.support.threading_helper — Utilities for threading tests](testsupportthreading_helper-utilities-for-threading-tests/index.md) | Join timeouts, thread start/join helpers |
| [test.support.os_helper — Utilities for os tests](testsupportos_helper-utilities-for-os-tests/index.md) | `TESTFN` temp files, `EnvironmentVarGuard`, platform capability probes |
| [test.support.import_helper — Utilities for import tests](testsupportimport_helper-utilities-for-import-tests/index.md) | Fresh imports, `CleanImport`, and module cleanup |
| [test.support.warnings_helper — Utilities for warnings tests](testsupportwarnings_helper-utilities-for-warnings-tests/index.md) | `check_warnings`, `ignore_warnings`, syntax-warning helpers |
