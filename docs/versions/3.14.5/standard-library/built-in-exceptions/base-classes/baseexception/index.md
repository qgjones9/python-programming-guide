# [BaseException](https://docs.python.org/3/library/exceptions.html#BaseException)

`BaseException` is the **root** of Python’s built-in exception hierarchy. Every built-in and user-defined exception class inherits from it. It is **not** meant as the base for ordinary application exceptions—use [`Exception`](../exception/index.md) instead. Full API detail remains on [docs.python.org](https://docs.python.org/3/library/exceptions.html#BaseException); this page covers instance attributes, notes, tracebacks, and which built-ins sit directly under this type.

---

## Placement in the hierarchy

| Category | Examples | Inherit from |
|----------|----------|-------------|
| Normal errors | `ValueError`, `TypeError`, `OSError` | `Exception` → `BaseException` |
| System exit / interrupt | `SystemExit`, `KeyboardInterrupt` | `BaseException` only |
| Generator shutdown | `GeneratorExit` | `BaseException` only (not `Exception`) |

```python
# Goal: system-exiting types are BaseException but not Exception
assert issubclass(KeyboardInterrupt, BaseException)
assert not issubclass(KeyboardInterrupt, Exception)
assert issubclass(SystemExit, BaseException)
assert issubclass(GeneratorExit, BaseException)
assert not issubclass(GeneratorExit, Exception)
assert issubclass(ValueError, BaseException)
```

See the overview tree in [Built-in Exceptions](../../index.md) and [Exception](../exception/index.md) for the recommended catch boundaries.

---

## Constructor and `args`

The optional arguments passed to the constructor are stored in **`args`**. Calling `str()` on the instance returns the string representation of those arguments, or **`""`** when `args` is empty. Some built-ins (for example `OSError`) assign special meaning to each element of `args`; others are usually constructed with a single message string.

```python
def demo_args_and_str():
    with_message = ValueError("disk full")
    assert with_message.args == ("disk full",)
    assert str(with_message) == "disk full"
    empty = ValueError()
    assert empty.args == ()
    assert str(empty) == ""

demo_args_and_str()
```

---

## Traceback: `__traceback__` and `with_traceback()`

**`__traceback__`** holds the traceback object for this exception (set when the exception is raised). **`with_traceback(tb)`** replaces that traceback and **returns the same exception instance**—handy when re-wrapping an error before PEP 3134-style `raise ... from`, or when converting one exception type into another while preserving stack information.

```python
import sys

def demo_with_traceback():
    try:
        1 / 0
    except ZeroDivisionError:
        tb = sys.exception().__traceback__
        wrapped = RuntimeError("conversion failed").with_traceback(tb)
        assert wrapped.__traceback__ is tb
        assert type(wrapped).__name__ == "RuntimeError"

demo_with_traceback()
```

For implicit and explicit chaining, see [Exception context](../../exception-context/index.md).

---

## Exception notes (3.11+)

**`add_note(note)`** appends a string that appears in the default traceback after the exception message. **`__notes__`** lists all notes added so far; the list is created when the first note is added. Passing a non-string to `add_note()` raises **`TypeError`**.

```python
def demo_notes():
    exc = ConnectionError("reset by peer")
    exc.add_note("Retry after checking VPN status.")
    assert exc.__notes__ == ["Retry after checking VPN status."]
    assert "reset by peer" in str(exc)

demo_notes()
```

---

## Chaining attributes

These live on every `BaseException` instance and drive traceback display (PEP 3134):

| Attribute | Role |
|-----------|------|
| `__context__` | Exception being handled when this one was raised (implicit chain) |
| `__cause__` | Explicit cause from `raise new from old` |
| `__suppress_context__` | When true, hide implicit context in tracebacks |

Full behavior and examples: [Exception context](../../exception-context/index.md).

---

## When to use or catch `BaseException`

| Do | Don't |
|----|-------|
| Inspect hierarchy with `issubclass` / `isinstance` | Subclass `BaseException` for routine app errors |
| Catch `KeyboardInterrupt` / `SystemExit` only with deliberate shutdown logic | Use bare `except BaseException` in general libraries |
| Access `args`, notes, and traceback for logging | Assume `except Exception` catches Ctrl+C or `sys.exit()` |

---

## Best practices

- Define application exception types under [`Exception`](../exception/index.md).
- Use `add_note()` for operator-facing hints that should not replace the primary message.
- Prefer `raise ... from` over manual `with_traceback()` for new code unless you are porting legacy patterns.
- Log `exc.args` and `exc.__notes__` in structured error reports.

---

## Common pitfalls

- **`except Exception` misses `GeneratorExit`** — closing generators uses a `BaseException` subclass by design.
- **`str(exc)` with no args** is empty even though the type name appears in tracebacks.
- **`add_note()` requires `str`** — format numbers yourself before calling.
- Confusing **`BaseException`** (root) with **`BaseExceptionGroup`** ([exception groups](../../exception-groups/index.md)) — different feature (3.11+).

---

## Related pages

| Topic | Link |
|-------|------|
| Recommended application base | [Exception](../exception/index.md) |
| Chaining and `raise ... from` | [Exception context](../../exception-context/index.md) |
| All base-class grouping types | [Base classes](../index.md) |
