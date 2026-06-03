# [ResourceWarning](https://docs.python.org/3/library/exceptions.html#ResourceWarning)

`ResourceWarning` (added in Python 3.2) reports **resource usage problems**—typically unclosed files, sockets, or generators holding OS handles. Canonical docs: [exceptions.html#ResourceWarning](https://docs.python.org/3/library/exceptions.html#ResourceWarning).

---

## Purpose

Make leaks visible in long-running processes and tests. CPython’s garbage collector emits `ResourceWarning` when tracked objects are finalized without being closed.

---

## Default filter behavior

| Aspect | Behavior |
|--------|----------|
| Default filter | **Ignored** (`ignore::ResourceWarning`) |
| Development mode | Shown (see [devmode](https://docs.python.org/3/library/devmode.html)) |
| `"error"` in tests | Common pattern: `filterwarnings("error", category=ResourceWarning)` |
| `source` argument | [`warnings.warn(..., source=obj)`](https://docs.python.org/3/library/warnings.html#warnings.warn) ties the message to the leaking object |

---

## When to emit

- Standard library when a file object or socket is collected without `.close()`.
- Application code detecting handles held past expected lifetime.
- Prefer `try`/`finally` or context managers (`with open(...)`) so warnings are a backstop, not the primary fix.

---

## Best practices

- Always close resources with `with` statements; warnings indicate a bug in cleanup logic.
- In tests, treat `ResourceWarning` as failure to catch regressions early.
- Pass `source=` when re-emitting from a destructor wrapper so diagnostics identify the object.

---

## Example — unclosed file detected via warn

```python
import warnings

class LeakyReader:
    def __init__(self, path):
        self._file = open(path, "w", encoding="utf-8")

    def __del__(self):
        if self._file and not self._file.closed:
            warnings.warn(
                "LeakyReader closed implicitly in __del__",
                ResourceWarning,
                source=self,
                stacklevel=2,
            )
            self._file.close()

import os
import tempfile

path = os.path.join(tempfile.gettempdir(), "resource_warning_demo.txt")
with warnings.catch_warnings(record=True) as log:
    warnings.simplefilter("always")
    reader = LeakyReader(path)
    del reader
    assert any(issubclass(item.category, ResourceWarning) for item in log)
os.remove(path)
```

---

## See also

- [`warnings.warn()` — `source` parameter](https://docs.python.org/3/library/warnings.html#warnings.warn)
- [Development mode](https://docs.python.org/3/library/devmode.html)
