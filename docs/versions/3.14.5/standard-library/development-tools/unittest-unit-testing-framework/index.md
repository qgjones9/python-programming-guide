# [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)

`unittest` is Python's **xUnit-style** testing framework: group tests in classes, share fixtures, assert outcomes, and discover tests by naming convention. It ships with the standard library and integrates with CI runners via `python -m unittest`. Canonical reference: [unittest.html](https://docs.python.org/3/library/unittest.html).

---

## Purpose

Use `unittest` when you want **structured tests** with setup/teardown, rich assertions, and subtests. Subclass `unittest.TestCase`, name methods `test_*`, and run with `unittest.main()` or discovery. For mocking dependencies see [`unittest.mock`](unittestmock-mock-object-library/index.md).

---

## Core concepts

| Concept | Role |
|---------|------|
| `TestCase` | Container for test methods and assertions |
| `setUp` / `tearDown` | Per-test fixture hooks |
| `setUpClass` / `tearDownClass` | Once-per-class hooks (`@classmethod`) |
| `assert*` methods | `assertEqual`, `assertRaises`, `assertAlmostEqual`, … |
| `subTest` | Parameterized cases within one test method |
| `TestLoader` / `TestSuite` | Collect and organize tests |
| `TextTestRunner` | Execute suite and report failures |

---

## Example — basic TestCase

```python
import unittest

class MathTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 2, 4)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

suite = unittest.TestSuite()
suite.addTest(MathTests("test_addition"))
suite.addTest(MathTests("test_division_by_zero"))
result = unittest.TextTestRunner(stream=open("/dev/null", "w")).run(suite)
assert result.wasSuccessful()
```

---

## Example — subTest for parameterized cases

```python
import unittest

class ParseTests(unittest.TestCase):
    def test_integers(self):
        cases = [("0", 0), ("42", 42), ("-3", -3)]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(int(text), expected)

t = ParseTests()
t.test_integers()
```

---

## Discovery conventions

| Pattern | Meaning |
|---------|---------|
| Files `test_*.py` | Discovered by default |
| Classes `Test*` | Loaded as test cases |
| Methods `test_*` | Individual tests |
| `python -m unittest discover -s tests` | Run package under `tests/` |

---

## Best practices

| Practice | Why |
|----------|-----|
| One logical behavior per test method | Failures pinpoint regressions |
| Use `assertRaises` as context manager | Ensures exception type and optional message |
| Prefer `setUp` over duplicating preamble | Keeps tests readable |
| Avoid inter-test shared mutable state | Order-independent runs |
| Combine with [`doctest`](doctest-test-interactive-python-examples/index.md) via `load_tests` | Docstring examples in larger suites |

---

## See also

- [`unittest.mock`](unittestmock-mock-object-library/index.md)
- [`unittest.mock — getting started`](unittestmock-getting-started/index.md)
