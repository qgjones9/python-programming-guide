# [Exception](https://docs.python.org/3/library/exceptions.html#Exception)

`Exception` is the base class for **all built-in exceptions that represent recoverable program errors**, and the type you should subclass for **user-defined** exceptions. System-exiting types (`SystemExit`, `KeyboardInterrupt`) and `GeneratorExit` inherit only from [`BaseException`](../baseexception/index.md), not from `Exception`. Full specification: [docs.python.org](https://docs.python.org/3/library/exceptions.html#Exception).

---

## Why `Exception` exists

Python splits the hierarchy so everyday `try` / `except` code can catch “something went wrong in my logic or I/O” without accidentally swallowing interpreter shutdown or generator cleanup. Anything you expect callers to handle in normal libraries should live under `Exception`.

| Inherits from `Exception` | Does **not** inherit from `Exception` |
|---------------------------|----------------------------------------|
| `ValueError`, `TypeError`, `OSError`, … | `SystemExit`, `KeyboardInterrupt` |
| `ArithmeticError`, `LookupError`, … | `GeneratorExit` |
| Typical `class MyError(Exception)` | (use `BaseException` only for special cases) |

```python
# Goal: built-in programming errors and user types share Exception
assert issubclass(RuntimeError, Exception)
assert issubclass(ArithmeticError, Exception)

class ConfigError(Exception):
    """Misconfigured deployment."""

assert issubclass(ConfigError, Exception)
assert issubclass(ConfigError, BaseException)
```

Tutorial background: [User-defined Exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions). Subclassing caveats: [Inheriting from built-in exceptions](../../inheriting-from-built-in-exceptions/index.md).

---

## Catching `Exception` in application code

A handler for `Exception` matches any subclass except the `BaseException`-only types above. Use it at API boundaries when you must log and translate unknown failures—but prefer **specific** types when you know what can fail.

```python
def run_user_code(callback):
    try:
        return ("ok", callback())
    except Exception as exc:
        return ("error", type(exc).__name__)

assert run_user_code(lambda: 1 / 0) == ("error", "ZeroDivisionError")
assert run_user_code(lambda: 42) == ("ok", 42)
```

Order handlers from **narrow** to **broad**: an `except ValueError` block must appear **before** `except Exception` for the same `try`.

```python
def classify(exc):
    try:
        raise exc
    except ValueError:
        return "value"
    except Exception:
        return "other"

assert classify(ValueError()) == "value"
assert classify(TypeError()) == "other"
```

---

## Shared instance API (inherited from `BaseException`)

`Exception` instances use the same machinery documented on [`BaseException`](../baseexception/index.md):

| Member | Summary |
|--------|---------|
| `args` | Tuple passed to the constructor |
| `__traceback__` | Traceback when raised |
| `with_traceback(tb)` | Return self with traceback replaced |
| `add_note()` / `__notes__` | Extra lines in traceback (3.11+) |
| `__context__`, `__cause__`, `__suppress_context__` | Chaining — see [Exception context](../../exception-context/index.md) |

```python
def demo_exception_message():
    exc = FileNotFoundError(2, "No such file", "missing.txt")
    assert exc.args[0] == 2
    assert "missing.txt" in str(exc)

demo_exception_message()
```

---

## Defining your own exception types

```python
class ValidationError(Exception):
    """Raised when user input fails business rules."""

class PaymentError(ValidationError):
    """More specific failure under the same family."""

def validate_age(age):
    if age < 0:
        raise ValidationError("age must be non-negative")

try:
    validate_age(-1)
except ValidationError as exc:
    assert "non-negative" in str(exc)
```

| Practice | Reason |
|----------|--------|
| Subclass `Exception` (or a built-in sibling) | Callers can `except YourError` predictably |
| Add attributes in `__init__` when needed | Keep `args` meaningful for `str(exc)` |
| Avoid multiple built-in bases | C layout / `args` handling conflicts — see inheriting notes |

---

## Intermediate bases under `Exception`

Several built-in **grouping** classes inherit from `Exception` and are documented in this folder:

| Base | Concrete examples |
|------|-------------------|
| [ArithmeticError](../arithmeticerror/index.md) | `ZeroDivisionError`, `OverflowError` |
| [LookupError](../lookuperror/index.md) | `KeyError`, `IndexError` |
| [BufferError](../buffererror/index.md) | (raised directly for buffer failures) |

Catch the intermediate type when recovery is the same for every subclass; otherwise catch the concrete type.

---

## When to use `Exception`

| Use `Exception` | Use something more specific |
|-----------------|----------------------------|
| Base class for custom app errors | `ValueError` for bad values, `OSError` for errno |
| Top-level handler that logs and returns an error code | Inner loops where you can fix one failure mode |
| Tests that assert “any expected error” | Public APIs documenting raised types |

---

## Best practices

- Never subclass [`BaseException`](../baseexception/index.md) for ordinary errors.
- Document raised types in docstrings; raise the **narrowest** built-in that fits.
- Re-raise with `raise` alone or `raise ... from` to preserve context when translating.
- In `except Exception as exc`, bind `exc` only for logging—avoid bare `except:`.

---

## Common pitfalls

- **`except Exception` still lets `KeyboardInterrupt` through** — good for servers; bad if you thought you caught “everything.”
- **Catching `Exception` around `finally` cleanup** can mask programming mistakes—handle expected types explicitly first.
- **Empty `except Exception: pass`** hides bugs; at minimum log `exc`.
- **`GeneratorExit`** is not an `Exception` subclass—do not catch it in generic error handlers inside generators.

---

## Related pages

| Topic | Link |
|-------|------|
| Root type and notes API | [BaseException](../baseexception/index.md) |
| Numeric error family | [ArithmeticError](../arithmeticerror/index.md) |
| Key/index error family | [LookupError](../lookuperror/index.md) |
| Parent index | [Base classes](../index.md) |
