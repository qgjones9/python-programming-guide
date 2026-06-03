# [Inheriting from built-in exceptions](https://docs.python.org/3/library/exceptions.html#inheriting-from-built-in-exceptions)

You can define application-specific errors by **subclassing built-in exception types**. That lets callers use familiar `except` patterns and keeps your types inside the standard hierarchy. Upstream rules and CPython implementation notes are on [docs.python.org](https://docs.python.org/3/library/exceptions.html#inheriting-from-built-in-exceptions); this page focuses on safe subclassing and good class design.

---

## Single inheritance rule

Subclass **one** built-in exception type at a time. Multiple inheritance among built-ins (for example `class E(ValueError, TypeError)`) is unsupported in practice:

| Risk | Detail |
|------|--------|
| **`args` handling** | Each base may initialize or interpret `args` differently; MRO can leave ambiguous state. |
| **CPython memory layout** | Many built-ins are C types with fixed struct layouts; mixing bases can fail at class creation or behave differently across versions. |

> **CPython implementation detail:** Most built-in exceptions are implemented in C ([`Objects/exceptions.c`](https://github.com/python/cpython/blob/main/Objects/exceptions.c)). Types with custom layouts cannot always combine with another exception base. Layout is **not** part of the language spec and may change between releases—stick to **one** exception base.

```python
# Goal: single inheritance is the supported pattern
class AppValidationError(ValueError):
    pass

assert issubclass(AppValidationError, ValueError)
assert issubclass(AppValidationError, Exception)

# Multiple built-in exception bases are discouraged: args handling and C layout
# may conflict even when class creation succeeds—use one base plus attributes.
```

If you need several “tags” on an error, use **one** exception base plus **attributes** or an **`Enum`** field—not multiple exception bases.

---

## Derive from `Exception`, not `BaseException`

[`BaseException`](../base-classes/baseexception/index.md) is reserved for system-exiting and control-flow types (`SystemExit`, `KeyboardInterrupt`, `GeneratorExit`). User-defined errors should inherit [`Exception`](../base-classes/exception/index.md) or a **more specific** built-in (`ValueError`, `OSError`, …).

```python
class ConfigError(Exception):
    """Misconfiguration in application settings."""

class InvalidPortError(ValueError):
    """Port number out of allowed range."""

assert issubclass(ConfigError, Exception)
assert ConfigError.__bases__ == (Exception,)
assert issubclass(InvalidPortError, ValueError)
```

Catching `except Exception:` then includes your types without swallowing `KeyboardInterrupt`.

---

## Patterns for good custom exception classes

### Minimal message-only type

```python
class PaymentDeclinedError(Exception):
    """Raised when a payment provider rejects a charge."""

def charge(amount):
    if amount <= 0:
        raise PaymentDeclinedError("amount must be positive")
    return "ok"

try:
    charge(0)
except PaymentDeclinedError as e:
    assert "positive" in str(e)
assert charge(10) == "ok"
```

### Structured fields beyond `args`

Store domain data on the instance; keep `args` for the human message when possible.

```python
class HTTPError(Exception):
    def __init__(self, status, message):
        self.status = status
        super().__init__(f"{status}: {message}")

err = HTTPError(404, "not found")
assert err.status == 404
assert "404" in str(err)
```

### Narrow base for a family of errors

Subclass an intermediate built-in when handlers should group failures.

```python
class CodecNotFoundError(LookupError):
    """No codec registered for the requested name."""

def get_codec(name):
    if name not in ("utf-8", "ascii"):
        raise CodecNotFoundError(name)
    return name

try:
    get_codec("unknown")
except LookupError:
    handled = True
else:
    handled = False
assert handled is True
```

### Exception groups for parallel failures (3.11+)

When aggregating errors, prefer [`ExceptionGroup`](../exception-groups/exceptiongroup/index.md) over a custom “multi-error” exception.

```python
errors = [ValueError("a"), TypeError("b")]
group = ExceptionGroup("batch failed", errors)
assert len(group.exceptions) == 2
assert isinstance(group, Exception)
```

---

## Anti-patterns to avoid

| Anti-pattern | Prefer instead |
|--------------|----------------|
| `class MyError(BaseException)` | `class MyError(Exception)` |
| Multiple built-in bases | One base + attributes |
| Empty `except:` to catch your own type | `except MyError:` or `except Exception:` with logging and re-raise |
| Raising `Exception("msg")` everywhere | Named subclasses for stable `except` targets |
| Subclassing `Warning` for fatal errors | Subclass `Exception`; reserve `Warning` for [`warnings`](../warnings/index.md) |

---

## Testing handlers

Built-in and custom subclasses behave the same in `try` / `except`:

```python
class DemoError(RuntimeError):
    pass

def run(handler):
    try:
        raise DemoError("fail")
    except RuntimeError:
        return handler

assert run("caught") == "caught"
```

For translating errors while preserving context, use `raise NewError(...) from old`—see [Exception context](../exception-context/index.md).

---

## Related pages

| Topic | Link |
|-------|------|
| Tutorial: user-defined exceptions | [Errors and Exceptions — User-defined Exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions) |
| Hierarchy and catch breadth | [Exception hierarchy](../exception-hierarchy/index.md) |
| `BaseException` attributes (`add_note`, `with_traceback`) | [BaseException](../base-classes/baseexception/index.md) |
