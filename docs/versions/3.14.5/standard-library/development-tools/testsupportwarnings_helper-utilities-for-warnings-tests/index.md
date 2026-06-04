# [test.support.warnings_helper — Utilities for warnings tests](https://docs.python.org/3/library/test.html#module-test.support.warnings_helper)

`test.support.warnings_helper` standardizes **warning capture and assertion** in CPython tests: expect exact messages, ignore categories temporarily, and verify syntax warnings. Canonical reference: [test.html#module-test.support.warnings_helper](https://docs.python.org/3/library/test.html#module-test.support.warnings_helper).

---

## Purpose

Warning behavior depends on filters and [Development Mode](../python-development-mode/index.md). Test helpers record warnings reliably without mutating global filters permanently.

---

## Key helpers

| Name | Role |
|------|------|
| `check_warnings` | Context manager expecting specific warnings |
| `ignore_warnings` | Suppress categories for a block |
| `check_no_warnings` | Fail if any warning fires |
| `WarningsRecorder` | List-like recorded warnings |
| `check_syntax_warning` | Assert `SyntaxWarning` on compile |

---

## Example — check_warnings expects a DeprecationWarning

```python
import warnings
import test.support.warnings_helper as wh

def emit():
    warnings.warn("old API", DeprecationWarning, stacklevel=1)

with wh.check_warnings(("", DeprecationWarning)):
    emit()
```

---

## Example — check_no_warnings guard

```python
import unittest
import test.support.warnings_helper as wh

class SilentTest(unittest.TestCase):
    def test_no_warnings(self):
        with wh.check_no_warnings(self):
            self.assertEqual(42, 42)

unittest.main(argv=["demo"], exit=False, verbosity=0)
```

---

## Example — WarningsRecorder

```python
import warnings
import test.support.warnings_helper as wh

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    rec = wh.WarningsRecorder(log)
    warnings.warn("note", UserWarning)
    assert len(rec.warnings) == 1
    assert issubclass(rec.warnings[0].category, UserWarning)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Match **message regex** loosely | Format strings change between versions |
| Restore filters via context managers | Avoid breaking subsequent tests |
| Test warning **category** and **stacklevel** | Ensures users see actionable locations |

---

## See also

- [`warnings`](https://docs.python.org/3/library/warnings.html)
- [`test.support`](testsupport-utilities-for-the-python-test-suite/index.md)
