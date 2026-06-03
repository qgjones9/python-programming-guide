# [KeyboardInterrupt](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt)

Raised when the user presses the interrupt key (typically Control-C). Inherits from [`BaseException`](../base-classes/baseexception/index.md), not [`Exception`](../base-classes/exception/index.md), so generic `except Exception` handlers do not swallow it. See [docs.python.org](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt).

---

## When it is raised

| Context | Behavior |
|---------|----------|
| Main thread, running Python bytecode | Interrupt check between opcodes |
| Blocking C extension | May defer until the call returns |
| Signal handler | Documented in [Note on Signal Handlers and Exceptions](https://docs.python.org/3/library/signal.html#note-on-signal-handlers-and-exceptions) |

---

## Demonstrating the type hierarchy

```python
# Goal: KeyboardInterrupt is BaseException, not caught by except Exception
assert issubclass(KeyboardInterrupt, BaseException)
assert not issubclass(KeyboardInterrupt, Exception)

def handler(exc):
    try:
        raise exc
    except Exception:
        return 'caught Exception'
    except BaseException:
        return 'caught BaseException'

assert handler(KeyboardInterrupt()) == 'caught BaseException'
assert handler(ValueError()) == 'caught Exception'
```

---

## Best practices

- Allow `KeyboardInterrupt` to propagate unless you are shutting down gracefully (save state, then re-raise).
- Catching it can leave programs in inconsistent state if cleanup is incomplete.
- Related: [`SystemExit`](systemexit/index.md) (also inherits from `BaseException`).
