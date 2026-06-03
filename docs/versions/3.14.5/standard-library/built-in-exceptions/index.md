# [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)

Every error path in Python flows through **exception objects**: classes derived from [`BaseException`](base-classes/baseexception/index.md). Built-in exceptions are the vocabulary the interpreter and standard library use to signal failure—division by zero, missing files, bad types, exhausted iterators, and dozens of other conditions. Full reference prose lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html); this page orients you through the hierarchy, local notes, and practical handler patterns.

---

## How exception matching works

In a [`try`](https://docs.python.org/3/reference/compound_stmts.html#try) statement, an [`except`](https://docs.python.org/3/reference/compound_stmts.html#except) clause that names a class also catches **any subclass** of that class. Matching walks the inheritance tree; unrelated types are never equivalent, even if they share a name.

```python
# Goal: except Exception catches ValueError but not the reverse relationship
def caught_by(exc_type, handler_type):
    try:
        raise exc_type("demo")
    except handler_type:
        return True
    except Exception:
        return False

assert caught_by(ValueError, Exception) is True
assert caught_by(Exception, ValueError) is False
assert caught_by(KeyError, LookupError) is True
```

User code may raise built-in exceptions to mimic interpreter behavior (for tests or API contracts), but nothing prevents raising an inappropriate type—choose types deliberately.

---

## Associated values (`args`)

Except where noted upstream, built-in exceptions carry an **associated value** in `args`: usually a message string, sometimes a tuple (for example `OSError` errno pairs). The constructor arguments become `exc.args`; `str(exc)` typically formats them for display.

```python
exc = ValueError("bad literal")
assert exc.args == ("bad literal",)
assert str(exc) == "bad literal"
```

Some types assign extra attributes (`OSError.errno`, `KeyError` key display, `SyntaxError.lineno`, and others). See the per-exception pages linked below.

---

## Exception handling best practices

| Practice | Why |
|----------|-----|
| Catch the **narrowest** type that you can handle | Avoid swallowing bugs you did not anticipate (`except Exception` around large blocks hides `KeyboardInterrupt` only if you catch `Exception`, not `BaseException`—but it still hides many logic errors). |
| Order **`except`** clauses from **specific to general** | The first matching handler wins; put `ZeroDivisionError` before `ArithmeticError`. |
| Prefer **`raise ... from`** when translating errors | Preserves cause chains for debugging; use `from None` only when hiding the original traceback is intentional. See [Exception context](exception-context/index.md). |
| Derive custom types from [`Exception`](base-classes/exception/index.md) | Keeps `except Exception` useful and avoids catching [`SystemExit`](concrete-exceptions/systemexit/index.md) or [`KeyboardInterrupt`](concrete-exceptions/keyboardinterrupt/index.md) by mistake. |
| Subclass **one** built-in exception at a time | Avoids `args` and C memory-layout conflicts. See [Inheriting from built-in exceptions](inheriting-from-built-in-exceptions/index.md). |
| Use **`OSError`** subclasses for filesystem and network I/O | `FileNotFoundError`, `PermissionError`, and related types map to errno values portably. See [OS exceptions](os-exceptions/index.md). |
| Treat **warnings** separately from fatal errors | Warning categories inherit from [`Warning`](warnings/warning/index.md); control them with the [`warnings`](https://docs.python.org/3/library/warnings.html) module, not bare `except`. |
| Re-raise or log, then **`raise`** | `except SomeError: log(...); raise` preserves the traceback; bare `raise` inside `except` re-raises the active exception. |
| Use **`except*`** for **exception groups** (3.11+) | Matches subgroups by contained exception types. See [Exception groups](exception-groups/index.md). |

```python
# Goal: narrow handler leaves other errors visible
def parse_positive(text):
    try:
        value = int(text)
    except ValueError:
        return None
    if value <= 0:
        raise ValueError("must be positive")
    return value

assert parse_positive("abc") is None
assert parse_positive("3") == 3
try:
    parse_positive("0")
except ValueError as e:
    assert "positive" in str(e)
```

For user-defined hierarchies, see the tutorial section [User-defined Exceptions](https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions).

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Exception context](exception-context/index.md) | Implicit `__context__`, explicit `__cause__`, and `__suppress_context__`; chaining with `raise ... from` and traceback display rules (PEP 3134). |
| [Inheriting from built-in exceptions](inheriting-from-built-in-exceptions/index.md) | Subclass one built-in at a time; derive from `Exception`; CPython memory-layout notes; patterns for application-specific error types. |
| [Base classes](base-classes/index.md) | Root and intermediate types—`BaseException`, `Exception`, `ArithmeticError`, `BufferError`, `LookupError`—used mainly as catch-all bases or for shared behavior. |
| [Concrete exceptions](concrete-exceptions/index.md) | Day-to-day errors: `TypeError`, `ValueError`, `ImportError`, `SyntaxError`, iterator protocol types, compatibility aliases, and more. |
| [OS exceptions](os-exceptions/index.md) | `OSError` subclasses tied to errno (`FileNotFoundError`, `PermissionError`, `ConnectionError` family, and others). |
| [Warnings](warnings/index.md) | Recoverable conditions as exception types (`DeprecationWarning`, `UserWarning`, …) for the warnings machinery. |
| [Exception groups](exception-groups/index.md) | `ExceptionGroup` / `BaseExceptionGroup` for multiple unrelated failures; `except*` matching (Python 3.11+). |
| [Exception hierarchy](exception-hierarchy/index.md) | Full annotated inheritance tree with grouping notes and guidance on broad vs narrow handlers. |

---

## Subsection highlights

### [Exception context](exception-context/index.md)

When a new exception is raised while another is already being handled (inside `except`, `finally`, or `with`), Python links them for traceback display. Explicit `raise new from old` sets `__cause__`; `raise new from None` hides the implicit chain from users while keeping `__context__` for introspection.

### [Inheriting from built-in exceptions](inheriting-from-built-in-exceptions/index.md)

Programmers should extend [`Exception`](base-classes/exception/index.md) or a specific subclass—not [`BaseException`](base-classes/baseexception/index.md). Multiple inheritance among built-in exception types is discouraged because C implementations may use incompatible struct layouts.

### [Base classes](base-classes/index.md)

[`BaseException`](base-classes/baseexception/index.md) roots the tree; [`Exception`](base-classes/exception/index.md) is the recommended base for catchable application errors. Intermediate bases such as [`ArithmeticError`](base-classes/arithmeticerror/index.md) and [`LookupError`](base-classes/lookuperror/index.md) let you handle families of failures with one `except` clause.

### [Concrete exceptions](concrete-exceptions/index.md)

The types you encounter most often in tracebacks. Includes control-flow exceptions (`StopIteration`, `GeneratorExit`), import and syntax failures, Unicode errors under `ValueError`, and legacy aliases (`IOError`, `EnvironmentError` → `OSError`).

### [OS exceptions](os-exceptions/index.md)

Fine-grained `OSError` subclasses chosen from the platform errno. Prefer catching `FileNotFoundError` over parsing `OSError.errno` when the distinction matters.

### [Warnings](warnings/index.md)

Not fatal by default; filters in [`warnings`](https://docs.python.org/3/library/warnings.html) decide visibility. `DeprecationWarning` vs `FutureWarning` targets developers vs end users respectively.

### [Exception groups](exception-groups/index.md)

Wrap a sequence of exceptions so concurrent or aggregated failures propagate together. `ExceptionGroup` is caught by `except Exception`; `BaseExceptionGroup` is not.

### [Exception hierarchy](exception-hierarchy/index.md)

Single reference tree from `BaseException` through warnings and OS errors, with notes on which branches sit outside `Exception`.
