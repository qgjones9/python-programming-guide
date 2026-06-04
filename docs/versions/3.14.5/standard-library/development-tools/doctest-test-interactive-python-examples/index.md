# [doctest — Test interactive Python examples](https://docs.python.org/3/library/doctest.html)

`doctest` finds **interactive Python examples** in docstrings, text files, and objects, then **executes and compares** them to expected output. It is ideal for small, deterministic examples that double as documentation. Canonical reference: [doctest.html](https://docs.python.org/3/library/doctest.html).

---

## Purpose

Use `doctest` to keep **examples honest**: regression-test pure functions, demonstrate APIs in docstrings, and validate tutorial snippets. For larger suites prefer [`unittest`](unittest-unit-testing-framework/index.md); doctest excels at literate, copy-paste-friendly examples.

---

## Key API

| Name | Role |
|------|------|
| `doctest.testmod()` | Run tests in current module's docstrings |
| `doctest.DocTestSuite` / `DocFileSuite` | Build `unittest` suites from docstrings or `.txt` files |
| `doctest.run_docstring_examples` | Run examples attached to one object |
| `doctest.ELLIPSIS` flag | Match `...` wildcard in expected output |
| `doctest.master` | Global runner registry (advanced) |

---

## Example — docstring tests

```python
def factorial(n: int) -> int:
    """Compute n!.

    >>> factorial(5)
    120
    >>> factorial(0)
    1
    """
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

import doctest
failures, _ = doctest.testmod(verbose=False)
assert failures == 0
assert factorial(5) == 120
```

---

## Example — `ELLIPSIS` for variable output

```python
import doctest

def show_dict():
    """Show a mapping.

    >>> show_dict()  # doctest: +ELLIPSIS
    {'a': ...}
    """
    return {"a": id(object())}

globs = {"show_dict": show_dict}
result = doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS, globs=globs)
assert result.failed == 0
assert "a" in show_dict()
```

---

## Comparison flags and pitfalls

| Flag / topic | Notes |
|--------------|-------|
| `NORMALIZE_WHITESPACE` | Collapses whitespace differences |
| `DONT_ACCEPT_TRUE_FOR_1` | Rejects `True` where `1` expected |
| `# doctest: +SKIP` | Skip a single example |
| Trailing whitespace | Significant unless normalized |
| `print` vs expression | REPL shows repr; last expression is not auto-printed in doctest |

---

## See also

- [`unittest`](unittest-unit-testing-framework/index.md) — full test framework
- [How to write docstrings](https://docs.python.org/3/tutorial/documentation.html)
