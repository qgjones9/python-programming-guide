# [SyntaxWarning](https://docs.python.org/3/library/exceptions.html#SyntaxWarning)

`SyntaxWarning` flags **dubious syntax** in source code. The compiler often emits it while parsing; runtime `warnings` filters may not affect already-compiled bytecode. Canonical docs: [exceptions.html#SyntaxWarning](https://docs.python.org/3/library/exceptions.html#SyntaxWarning).

---

## Purpose

Alert authors to constructs that are legal today but confusing, error-prone, or slated for stricter rules—without upgrading to [`SyntaxError`](../../concrete-exceptions/syntaxerror/index.md).

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | `"default"` when the warning is emitted and matched |
| Compile time | Raised during `compile()` / import of `.py` source; often **not** re-checked on cached `.pyc` |
| Runtime filters | Apply when the compiler emits the warning; changing filters after import does not recompile |

Treat `SyntaxWarning` as a **source authoring** signal: fix the code or explicitly filter at compile time if you must.

---

## When to emit

Mostly emitted by CPython’s parser (e.g. `assert` with wrong indentation patterns, comparison idioms). Library code seldom calls `warnings.warn(..., SyntaxWarning)` unless mimicking compiler diagnostics in template or macro systems.

---

## Best practices

- Run `-We` (`error::SyntaxWarning`) or treat warnings as errors in CI for packages you ship as source.
- Fix the underlying syntax rather than silencing globally.
- If you emit manually, use `warnings.warn_explicit()` with accurate `filename` and `lineno` when the logical source is not the current stack frame.

---

## Example — compile-time `is` with literal

```python
import warnings

source = "value is 42\n"

with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    compile(source, "<example>", "exec")
    assert any(issubclass(item.category, SyntaxWarning) for item in log)
```

---

## See also

- [SyntaxError](../../concrete-exceptions/syntaxerror/index.md)
- [`warnings.warn_explicit()`](https://docs.python.org/3/library/warnings.html#warnings.warn_explicit)
