# [7.3. The assert statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)

Notes on **7.3. The assert statement** within [*7. Simple statements*](https://docs.python.org/3/reference/simple_stmts.html). Normative grammar and footnotes live on [docs.python.org](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement).

- `assert expr` is equivalent to `if __debug__: if not expr: raise AssertionError`.
- The two-expression form `assert expr1, expr2` supplies `AssertionError(expr2)` when the check fails.
- With `python -O`, assert statements are not emitted — do not rely on them for production invariants.

```python
# Passing checks do nothing; failures raise AssertionError (when __debug__ is True).
flag = True
assert flag
assert 1 + 1 == 2, "expected two"

errors = []
try:
    assert False, "boom"
except AssertionError as exc:
    errors.append(str(exc))
assert errors == ["boom"]
```

Parent: [7. Simple statements](../index.md)
