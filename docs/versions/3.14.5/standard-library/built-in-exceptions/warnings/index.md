# [Warnings](https://docs.python.org/3/library/exceptions.html#warnings)

Built-in warning categories are exception subclasses of [`Warning`](warning/index.md). They label recoverable conditions that usually should not stop the program. The [`warnings`](https://docs.python.org/3/library/warnings.html) module routes messages through a **filter** (ignore, print once, always print, or turn into an error) and a **show** hook (typically `sys.stderr`). Full reference wording lives on [docs.python.org](https://docs.python.org/3/library/exceptions.html#warnings); these notes explain categories, default filters, and how to emit warnings from your code.

---

## Warnings vs exceptions

| Aspect | Warnings | Exceptions |
|--------|----------|------------|
| Typical outcome | Message printed (or ignored) unless filtered to `"error"` | Propagate until caught or terminate the thread |
| Base type | [`Warning`](warning/index.md) → [`Exception`](../base-classes/exception/index.md) | [`Exception`](../base-classes/exception/index.md) and subclasses |
| Primary API | [`warnings.warn()`](https://docs.python.org/3/library/warnings.html#warnings.warn) | `raise` |
| Audience tuning | Category choice (`DeprecationWarning` vs `FutureWarning`) | Exception type |

Because `Warning` inherits from `Exception`, a filter action of `"error"` raises `category(message)` like any other exception.

---

## How filtering works

Each warning is matched against an ordered list of filter specs `(action, message, category, module, lineno)`. The first match wins. Actions include `"default"` (first occurrence per location), `"ignore"`, `"always"`, `"module"`, `"once"`, and `"error"`. Configure filters with [`filterwarnings()`](https://docs.python.org/3/library/warnings.html#warnings.filterwarnings), [`simplefilter()`](https://docs.python.org/3/library/warnings.html#warnings.simplefilter), `-W` / `PYTHONWARNINGS`, or [`catch_warnings`](https://docs.python.org/3/library/warnings.html#warnings.catch_warnings) in tests.

### Default filters (release builds)

In ordinary release builds Python installs these filters (later entries do not override earlier ones for the same match—order matters):

```
default::DeprecationWarning:__main__
ignore::DeprecationWarning
ignore::PendingDeprecationWarning
ignore::ImportWarning
ignore::ResourceWarning
```

| Category | Default disposition | Notes |
|----------|---------------------|-------|
| [`DeprecationWarning`](deprecationwarning/index.md) | Ignored except in `__main__` | PEP 565; shown in dev mode |
| [`PendingDeprecationWarning`](pendingdeprecationwarning/index.md) | Ignored | Shown in [development mode](https://docs.python.org/3/library/devmode.html) |
| [`ImportWarning`](importwarning/index.md) | Ignored | Shown in development mode |
| [`ResourceWarning`](resourcewarning/index.md) | Ignored | Shown in development mode |
| [`UserWarning`](userwarning/index.md), [`RuntimeWarning`](runtimewarning/index.md), [`FutureWarning`](futurewarning/index.md), [`SyntaxWarning`](syntaxwarning/index.md), [`UnicodeWarning`](unicodewarning/index.md) | `"default"` | First hit per module line unless overridden |
| [`BytesWarning`](byteswarning/index.md) | Enabled with `-bb` / `-b` twice | Not in the default list since 3.7 |
| [`EncodingWarning`](encodingwarning/index.md) | Opt-in | `-X warn_default_encoding` or `PYTHONWARNDEFAULTENCODING` |

Run tests with `-Wd` (`PYTHONWARNINGS=default`) to surface normally ignored developer warnings. Application authors sometimes call `warnings.simplefilter("ignore")` when `sys.warnoptions` is empty so end users do not see library deprecations by default.

---

## Emitting warnings from code

Use [`warnings.warn(message, category=..., stacklevel=...)`](https://docs.python.org/3/library/warnings.html#warnings.warn). The default category is `UserWarning`. Wrapper functions should pass `stacklevel=2` (or higher) so tracebacks point at the caller, not the helper. Pick the category that matches the intended audience: [`DeprecationWarning`](deprecationwarning/index.md) for other Python developers, [`FutureWarning`](futurewarning/index.md) for application end users (see PEP 565 / 3.7 filter changes).

```python
import warnings

def deprecated_helper(msg):
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

captured = []
with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    deprecated_helper("old API")
    captured.append((log[-1].category, str(log[-1].message)))

assert captured[0][0] is DeprecationWarning
assert "old API" in captured[0][1]
```

For testing, use [`catch_warnings(record=True)`](https://docs.python.org/3/library/warnings.html#warnings.catch_warnings) with `simplefilter("always")` or `"error"`. Python 3.13+ also provides [`@warnings.deprecated`](https://docs.python.org/3/library/warnings.html#warnings.deprecated) for functions and classes.

---

## Hierarchy

All built-in warning categories inherit from [`Warning`](warning/index.md):

```
Exception
 └── Warning
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

User-defined categories must subclass `Warning` (usually `UserWarning` or a more specific built-in).

---

## Sections in this repo

| Warning | Description |
|---------|-------------|
| [Warning](warning/index.md) | Root category; default base for custom warning classes. |
| [UserWarning](userwarning/index.md) | Default category for `warnings.warn()`; general user-facing notices. |
| [DeprecationWarning](deprecationwarning/index.md) | Deprecated APIs for **Python developers** (libraries, frameworks). |
| [PendingDeprecationWarning](pendingdeprecationwarning/index.md) | Features slated for future deprecation but not deprecated yet. |
| [SyntaxWarning](syntaxwarning/index.md) | Dubious syntax, usually at compile time. |
| [RuntimeWarning](runtimewarning/index.md) | Dubious but legal runtime behavior. |
| [FutureWarning](futurewarning/index.md) | Deprecated behavior for **end users** of applications. |
| [ImportWarning](importwarning/index.md) | Probable mistakes in import machinery. |
| [UnicodeWarning](unicodewarning/index.md) | Unicode-related issues. |
| [EncodingWarning](encodingwarning/index.md) | Default locale encoding used where UTF-8 is expected (3.10+). |
| [BytesWarning](byteswarning/index.md) | Bytes/bytearray misuse (e.g. comparing `str` to `bytes`). |
| [ResourceWarning](resourcewarning/index.md) | Unclosed files, sockets, and similar resource leaks. |

See also the [`warnings` module](https://docs.python.org/3/library/warnings.html) for filter syntax, `warn_explicit()`, and logging integration via [`logging.captureWarnings()`](https://docs.python.org/3/library/logging.html#logging.captureWarnings).
