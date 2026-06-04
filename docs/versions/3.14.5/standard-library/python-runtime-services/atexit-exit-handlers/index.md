# [atexit — Exit handlers](https://docs.python.org/3/library/atexit.html)

[`atexit`](https://docs.python.org/3/library/atexit.html) registers functions called **automatically at normal interpreter shutdown**, after main finishes or `sys.exit()` runs. Handlers execute in **LIFO** order (last registered, first called). Reference: [docs.python.org](https://docs.python.org/3/library/atexit.html).

---

## API

| Function | Role |
|----------|------|
| `register(func, *args, **kwargs)` | Schedule callable at shutdown; returns `func` |
| `unregister(func)` | Remove a previously registered function |
| `@atexit.register` | Decorator form of `register` |

```python
# Goal: LIFO order of atexit handlers
import atexit

log = []

@atexit.register
def second():
    log.append("second")

@atexit.register
def first():
    log.append("first")

# Simulate shutdown without exiting interpreter
atexit._run_exitfuncs()
assert log == ["first", "second"]
```

The example calls the private `_run_exitfuncs()` for demonstration; production code relies on normal process exit.

---

## Limitations

| Scenario | Handlers run? |
|----------|---------------|
| Normal return from script | Yes |
| `sys.exit()` | Yes |
| `os._exit()` | **No** |
| SIGKILL / power loss | **No** |
| Fatal interpreter error | **No** |

Do not rely on atexit for critical durability — flush best-effort logs only.

---

## Best practices

| Practice | Why |
|----------|-----|
| Keep handlers **idempotent and fast** | Multiple imports may re-register |
| Prefer **`contextlib` / `try/finally`** for scoped cleanup | Runs even on exceptional paths within process |
| Use **`unregister`** in tests | Prevent cross-test pollution |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Registering bound methods to dying objects | Weak refs may not save you | Close resources explicitly in `finally` |
| Expecting handlers after `os._exit(0)` | Skipped entirely | Use filesystem sync in critical paths |

---

## See also

- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — `sys.exit` triggers atexit
- [`weakref.finalize`](https://docs.python.org/3/library/weakref.html#weakref.finalize) — per-object finalizers
