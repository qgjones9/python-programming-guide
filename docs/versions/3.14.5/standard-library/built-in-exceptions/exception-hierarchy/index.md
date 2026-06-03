# [Exception hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)

Built-in exceptions form a **single inheritance tree** rooted at [`BaseException`](../base-classes/baseexception/index.md). Handlers match by **`issubclass`**, so the tree tells you which `except` types cover which failures. Full canonical listing lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#exception-hierarchy); below is the same tree with grouping notes and handler guidance.

---

## Full tree (annotated)

Legend: **bold** = often caught deliberately; *(control)* = not a typical application error; *(warn)* = warnings machinery.

```
BaseException                          # root; avoid except BaseException in app code
 ├── BaseExceptionGroup                 # wraps any exceptions; except* only (3.11+)
 ├── GeneratorExit                      # (control) closing generators/coroutines
 ├── KeyboardInterrupt                  # (control) user interrupt; inherits BaseException
 ├── SystemExit                         # (control) sys.exit(); inherits BaseException
 └── Exception                          # recommended catch boundary for "errors"
      ├── ArithmeticError               # numeric failures (see subclasses)
      │    ├── FloatingPointError       # rarely raised in CPython today
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError                   # buffer protocol failures
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]  # wraps Exception subclasses only
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError                   # invalid index/key on sequence or mapping
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError                       # errno-based; see OS exceptions section
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError                # weakref proxy after referent gone
      ├── RuntimeError                  # catch-all runtime failure
      │    ├── NotImplementedError
      │    ├── PythonFinalizationError
      │    └── RecursionError
      ├── StopAsyncIteration            # (control) async iterator protocol
      ├── StopIteration                 # (control) iterator protocol
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError                   # interpreter internal bug
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning                       # (warn) base for warning categories
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning
```

Local pages: [Base classes](../base-classes/index.md) · [Concrete exceptions](../concrete-exceptions/index.md) · [OS exceptions](../os-exceptions/index.md) · [Warnings](../warnings/index.md) · [Exception groups](../exception-groups/index.md)

---

## Major groupings

| Branch | Role | Typical handler |
|--------|------|-----------------|
| **Direct `BaseException` children** | Process control, not logic bugs | Usually **do not catch**; `GeneratorExit` and `SystemExit` must propagate; `KeyboardInterrupt` only with care |
| **`Exception` subtree** | Recoverable or reportable failures | `except Exception` at application boundaries; prefer narrower types inside libraries |
| **`ArithmeticError`** | Shared numeric failure base | `except ArithmeticError` when overflow and division-by-zero share one recovery path |
| **`LookupError`** | Missing index or key | `except LookupError` for “not found” on sequences and mappings alike |
| **`OSError` + errno subclasses** | OS and I/O | Catch `FileNotFoundError`, `PermissionError`, etc., instead of bare `OSError` when errno matters |
| **`ConnectionError` family** | Network/socket errno mapping | Catch `ConnectionError` for retry logic; subclass for specific reset/refused cases |
| **`RuntimeError` family** | Generic or specialized runtime | `RecursionError`, `NotImplementedError`, `PythonFinalizationError` under this node |
| **`ValueError` / `UnicodeError`** | Bad value vs bad Unicode transform | Catch `UnicodeDecodeError` when decoding bytes; `ValueError` for general validation |
| **`Warning` subtree** | Non-fatal conditions | Use [`warnings`](https://docs.python.org/3/library/warnings.html), not exception handlers, unless you promote to error |
| **Exception groups** | Multiple failures at once | `except*` (PEP 654); see [Exception groups](../exception-groups/index.md) |

---

## Outside `Exception`: why it matters

These inherit from [`BaseException`](../base-classes/baseexception/index.md) but **not** from [`Exception`](../base-classes/exception/index.md):

| Type | Reason |
|------|--------|
| `BaseExceptionGroup` | Can wrap `KeyboardInterrupt`, `SystemExit`, etc. |
| `GeneratorExit` | Normal generator shutdown—not an error |
| `KeyboardInterrupt` | Must not be hidden by broad `except Exception` |
| `SystemExit` | Clean interpreter exit via `sys.exit()` |

```python
# Goal: except Exception does not catch SystemExit
def exits_through(exc_type):
    try:
        raise exc_type()
    except Exception:
        return "caught"
    except BaseException:
        return "base"

assert exits_through(ValueError) == "caught"
assert exits_through(SystemExit) == "base"
```

Application code that uses `except Exception:` therefore still allows the interpreter to exit and Ctrl+C to propagate unless you catch `BaseException` explicitly (which is almost always wrong).

---

## When to catch broad vs narrow

| Situation | Prefer |
|-----------|--------|
| Fixing a known failure (bad user input, missing key) | **Narrow** type: `ValueError`, `KeyError`, `FileNotFoundError` |
| Logging and re-raising at a framework boundary | **`Exception`** (still excludes `SystemExit` / `KeyboardInterrupt`) |
| Retry loop on transient network/filesystem faults | **`OSError`** or **`ConnectionError`** if several errno subclasses share recovery |
| “Any lookup failed” without distinguishing list vs dict | **`LookupError`** |
| Numeric code where all arithmetic failures mean the same fallback | **`ArithmeticError`** |
| Defensive catch-all that hides bugs | **Avoid** bare `except:` or overly broad handlers without re-raise |

```python
# Goal: specific handler runs before broad LookupError
def classify(exc):
    try:
        raise exc
    except KeyError:
        return "mapping"
    except LookupError:
        return "lookup"
    except Exception:
        return "other"

assert classify(KeyError("x")) == "mapping"
assert classify(IndexError()) == "lookup"
```

**Rule of thumb:** catch the type you can **meaningfully handle**. If handlers would differ, split them; if recovery is identical, use the nearest common base (`LookupError`, `OSError`, `ArithmeticError`).

---

## Related pages

| Topic | Link |
|-------|------|
| Chaining and `raise ... from` | [Exception context](../exception-context/index.md) |
| Subclassing built-ins | [Inheriting from built-in exceptions](../inheriting-from-built-in-exceptions/index.md) |
| Parent overview and best practices | [Built-in Exceptions](../index.md) |
