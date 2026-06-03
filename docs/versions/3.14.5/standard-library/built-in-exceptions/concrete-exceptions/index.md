# [Concrete exceptions](https://docs.python.org/3/library/exceptions.html#concrete-exceptions)

These are the built-in exceptions you encounter most often in application code—distinct from hierarchy **base classes** such as [`Exception`](../base-classes/exception/index.md) or [`LookupError`](../base-classes/lookuperror/index.md). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#concrete-exceptions); each child page below adds teaching notes, runnable examples, and links to related types.

---

## How to read this section

| Pattern | Guidance |
|---------|----------|
| Catch the **specific** type when you know what can fail | `except KeyError` for missing dict keys, not bare `except Exception` |
| Catch a **base** when several failures need the same recovery | `except LookupError` for both `KeyError` and `IndexError` |
| Distinguish **type** vs **value** mistakes | `TypeError` for wrong types; `ValueError` for wrong values |
| OS and I/O failures | Prefer `OSError` subclasses (`FileNotFoundError`, `PermissionError`) over the legacy aliases |
| Control flow vs errors | `StopIteration` / `StopAsyncIteration` signal exhausted iterators; `GeneratorExit` and `SystemExit` inherit from `BaseException`, not `Exception` |

---

## Hierarchy snapshot

Many concrete types sit under intermediate bases documented elsewhere:

| Base | Concrete types in this folder |
|------|-------------------------------|
| [`ArithmeticError`](../base-classes/arithmeticerror/index.md) | `FloatingPointError`, `OverflowError`, `ZeroDivisionError` |
| [`LookupError`](../base-classes/lookuperror/index.md) | `IndexError`, `KeyError` |
| [`SyntaxError`](syntaxerror/index.md) | `IndentationError`, `TabError` |
| [`UnicodeError`](unicodeerror/index.md) | `UnicodeEncodeError`, `UnicodeDecodeError`, `UnicodeTranslateError` |
| [`ImportError`](importerror/index.md) | `ModuleNotFoundError` |
| [`NameError`](nameerror/index.md) | `UnboundLocalError` |
| [`RuntimeError`](runtimeerror/index.md) | `NotImplementedError`, `RecursionError`, `PythonFinalizationError` |
| [`OSError`](oserror/index.md) | `EnvironmentError`, `IOError`, `WindowsError` (compatibility aliases) |

---

## Quick example — matching by inheritance

```python
# Goal: except LookupError catches both KeyError and IndexError
def lookup(container, key):
    try:
        return container[key]
    except LookupError as exc:
        return type(exc).__name__

assert lookup({}, 'x') == 'KeyError'
assert lookup([1], 5) == 'IndexError'
assert lookup({'a': 1}, 'a') == 1
```

---

## Sections in this repo

- [AssertionError](assertionerror/index.md)
- [AttributeError](attributeerror/index.md)
- [EOFError](eoferror/index.md)
- [FloatingPointError](floatingpointerror/index.md)
- [GeneratorExit](generatorexit/index.md)
- [ImportError](importerror/index.md)
- [ModuleNotFoundError](modulenotfounderror/index.md)
- [IndexError](indexerror/index.md)
- [KeyError](keyerror/index.md)
- [KeyboardInterrupt](keyboardinterrupt/index.md)
- [MemoryError](memoryerror/index.md)
- [NameError](nameerror/index.md)
- [NotImplementedError](notimplementederror/index.md)
- [OSError](oserror/index.md)
- [OverflowError](overflowerror/index.md)
- [PythonFinalizationError](pythonfinalizationerror/index.md)
- [RecursionError](recursionerror/index.md)
- [ReferenceError](referenceerror/index.md)
- [RuntimeError](runtimeerror/index.md)
- [StopIteration](stopiteration/index.md)
- [StopAsyncIteration](stopasynciteration/index.md)
- [SyntaxError](syntaxerror/index.md)
- [IndentationError](indentationerror/index.md)
- [TabError](taberror/index.md)
- [SystemError](systemerror/index.md)
- [SystemExit](systemexit/index.md)
- [TypeError](typeerror/index.md)
- [UnboundLocalError](unboundlocalerror/index.md)
- [UnicodeError](unicodeerror/index.md)
- [UnicodeEncodeError](unicodeencodeerror/index.md)
- [UnicodeDecodeError](unicodedecodeerror/index.md)
- [UnicodeTranslateError](unicodetranslateerror/index.md)
- [ValueError](valueerror/index.md)
- [ZeroDivisionError](zerodivisionerror/index.md)
- [EnvironmentError](environmenterror/index.md)
- [IOError](ioerror/index.md)
- [WindowsError](windowserror/index.md)
