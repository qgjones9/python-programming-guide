# [Base classes](https://docs.python.org/3/library/exceptions.html#base-classes)

The built-in exceptions in this section are **mostly base classes**: they group related failure modes or anchor the global hierarchy. Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#base-classes); the pages below distill when to catch each type, how it relates to siblings, and runnable patterns you can copy into handlers or custom exception types.

---

## Role in the built-in hierarchy

Every built-in exception ultimately inherits from [`BaseException`](baseexception/index.md). Normal application errors (including all types in this folder except `BaseException` itself) also inherit from [`Exception`](exception/index.md). Intermediate bases such as [`ArithmeticError`](arithmeticerror/index.md), [`BufferError`](buffererror/index.md), and [`LookupError`](lookuperror/index.md) let you write one `except` clause for a **family** of concrete errors.

| Type | Typical use |
|------|-------------|
| `BaseException` | Root type; attributes (`args`, notes, traceback, chaining); **not** the recommended base for user exceptions |
| `Exception` | Recommended base for user-defined and most catch-all handlers |
| `ArithmeticError` | Shared handler for division, overflow, and float arithmetic failures |
| `BufferError` | Buffer protocol / memoryview failures |
| `LookupError` | Invalid key or index on mappings and sequences (and some codec lookups) |

An `except` clause that names a class also catches **any subclass** of that class. Unrelated exception types are never equivalent, even if they share a name in different modules.

For chaining (`__context__`, `__cause__`, `raise ... from`), see [Exception context](../exception-context/index.md). For subclassing built-ins safely, see [Inheriting from built-in exceptions](../inheriting-from-built-in-exceptions/index.md).

---

## When to catch a base vs a concrete type

| Situation | Prefer |
|-----------|--------|
| You know the failure mode (`KeyError` vs `IndexError`) | The **concrete** exception |
| Several related failures should share recovery logic | The **intermediate** base (`LookupError`, `ArithmeticError`) |
| Broad “any programming error” in application code | [`Exception`](exception/index.md) — not `BaseException` |
| Shutdown, Ctrl+C, generator close | Specific types (`SystemExit`, `KeyboardInterrupt`, `GeneratorExit`) under `BaseException`, often **not** caught |

Catching `BaseException` or `Exception` too broadly can hide bugs or prevent clean shutdown; order handlers from **most specific** to **most general**.

```python
# Goal: confirm intermediate bases sit between Exception and concrete types
assert issubclass(LookupError, Exception)
assert issubclass(KeyError, LookupError)
assert issubclass(ArithmeticError, Exception)
assert issubclass(ZeroDivisionError, ArithmeticError)
assert issubclass(BufferError, Exception)
```

---

## Best practices

- Derive **user-defined** exceptions from [`Exception`](exception/index.md) (or a more specific built-in), not from [`BaseException`](baseexception/index.md).
- Subclass **one** built-in exception at a time when extending the hierarchy (see inheriting notes for C layout caveats).
- Use intermediate bases only when you genuinely want one recovery path for every subclass.
- Re-raise or chain with `raise ... from` when translating errors so tracebacks stay debuggable.

---

## Common pitfalls

- **`except Exception`** does not catch `KeyboardInterrupt`, `SystemExit`, or `GeneratorExit` — by design those inherit only from `BaseException`.
- **`except LookupError`** also catches `UnicodeError` subclasses in some codec paths; prefer `KeyError` / `IndexError` when the container type is known.
- **`FloatingPointError`** is listed under `ArithmeticError` but is **rarely raised** in CPython today; do not assume float bugs surface as that type.
- Treating **`BufferError`** like a generic `OSError` — it signals the [buffer protocol](https://docs.python.org/3/c-api/buffer.html#bufferobjects), not filesystem errno values.

---

## Sections in this repo

| Exception | Page |
|-----------|------|
| [BaseException](baseexception/index.md) | Root class, `args`, traceback, notes, chaining attributes |
| [Exception](exception/index.md) | Default base for application and library errors |
| [ArithmeticError](arithmeticerror/index.md) | `ZeroDivisionError`, `OverflowError`, `FloatingPointError` |
| [BufferError](buffererror/index.md) | Buffer-related operation failures |
| [LookupError](lookuperror/index.md) | `KeyError`, `IndexError`, and `codecs.lookup()` |

Concrete types that inherit from these bases are documented under [Concrete exceptions](../concrete-exceptions/index.md).
