# [PythonFinalizationError](https://docs.python.org/3/library/exceptions.html#PythonFinalizationError)

Subclass of [`RuntimeError`](runtimeerror/index.md) raised when an operation is **blocked during interpreter shutdown** (finalization). Added in Python 3.13 ([docs.python.org](https://docs.python.org/3/library/exceptions.html#PythonFinalizationError)).

---

## When it is raised

| Blocked operation | Notes |
|-------------------|-------|
| Creating a new thread | During shutdown |
| `threading.Thread.join()` on daemon | Changed in 3.14 |

See also [`sys.is_finalizing()`](https://docs.python.org/3/library/sys.html#sys.is_finalizing).

---

## Demonstrating the type

```python
# Goal: confirm hierarchy on 3.13+; handler pattern via RuntimeError base
import builtins

exc_cls = getattr(builtins, 'PythonFinalizationError', None)
assert issubclass(RuntimeError, Exception)
if exc_cls is not None:
    assert issubclass(exc_cls, RuntimeError)
    caught = None
    try:
        raise exc_cls('interpreter is finalizing')
    except RuntimeError as exc:
        caught = type(exc).__name__
    assert caught == 'PythonFinalizationError'
```

---

## Best practices

- Avoid starting threads or heavy cleanup in `atexit` handlers that may run during finalization.
- Parent: [`RuntimeError`](runtimeerror/index.md).
