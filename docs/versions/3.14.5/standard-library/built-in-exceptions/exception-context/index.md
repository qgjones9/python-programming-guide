# [Exception context](https://docs.python.org/3/library/exceptions.html#exception-context)

When one exception occurs while another is already being handled, Python records that relationship on the exception object. The default traceback printer uses these links to show **chained tracebacks** (PEP 3134). Full specification remains on [docs.python.org](https://docs.python.org/3/library/exceptions.html#exception-context); this page explains the three chaining attributes and how display rules work.

---

## Context attributes — [Exception context](https://docs.python.org/3/library/exceptions.html#exception-context)

Three attributes on every `BaseException` instance describe how the current error relates to earlier ones:

| Attribute | Role |
|-----------|------|
| `BaseException.__context__` | The exception being handled when this one was raised (implicit chain). |
| `BaseException.__cause__` | The explicit cause set by `raise new_exc from original_exc`. |
| `BaseException.__suppress_context__` | When `True`, traceback display hides the implicit `__context__` chain. |

An exception is **being handled** inside an `except` or `finally` clause, or while unwinding a `with` statement's context manager.

---

## Implicit context (`__context__`)

When you `raise` (or let Python raise) a new exception while another is active in an `except`, `finally`, or `with` handler, the interpreter sets the new exception's `__context__` to the handled exception automatically. No `from` clause is required.

```python
def demo_implicit_context():
    try:
        1 / 0
    except ZeroDivisionError:
        try:
            {}["missing"]
        except KeyError as e:
            assert e.__context__ is not None
            assert isinstance(e.__context__, ZeroDivisionError)

demo_implicit_context()
```

---

## Explicit causes (`raise ... from`)

Use `raise new_exc from original_exc` to attach an **explicit cause**. The expression after `from` must be an exception instance or `None`. Python sets it on `__cause__` and sets `__suppress_context__` to `True`, so traceback output prefers the explicit chain.

```python
def demo_explicit_cause():
    try:
        int("not a number")
    except ValueError as original:
        try:
            raise TypeError("bad conversion") from original
        except TypeError as e:
            assert e.__cause__ is original
            assert e.__suppress_context__ is True

demo_explicit_cause()
```

### Replacing the displayed chain — `raise ... from None`

`raise new_exc from None` sets `__cause__` to `None` and suppresses `__context__` in tracebacks—useful when translating errors (for example turning `KeyError` into `AttributeError`) without showing the original to users. The old exception remains on `__context__` for debugging.

```python
def demo_from_none():
    try:
        {}["x"]
    except KeyError as orig:
        try:
            raise AttributeError("missing attr") from None
        except AttributeError as e:
            assert e.__cause__ is None
            assert e.__suppress_context__ is True
            assert e.__context__ is orig

demo_from_none()
```

---

## Traceback display

The default traceback printer shows chained exceptions **before** the primary exception. The raised exception always appears last so the final line names the error that actually propagated.

| Condition | What traceback shows |
|-----------|----------------------|
| `__cause__` is set | The explicit cause chain (always shown). |
| `__cause__` is `None` and `__suppress_context__` is false | The implicit `__context__` chain (if any). |
| `__suppress_context__` is `True` | Implicit context hidden; explicit `__cause__` still shown when set. |

For older code paths that predate PEP 3134, `BaseException.with_traceback(tb)` can attach a traceback without setting cause or context; see [`BaseException.with_traceback()`](../base-classes/baseexception/index.md).
