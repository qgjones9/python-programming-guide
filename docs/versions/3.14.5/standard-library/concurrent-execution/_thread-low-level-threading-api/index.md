# [_thread — Low-level threading API](https://docs.python.org/3/library/_thread.html)

The [`_thread`](https://docs.python.org/3/library/_thread.html) module exposes **CPython’s low-level threading primitives**: start OS threads, allocate mutex locks, and exit threads. Application code should normally use [`threading`](../threading-thread-based-parallelism/index.md), which wraps `_thread` with higher-level `Thread`, `RLock`, and exception hooks. Always available since 3.7. Reference: [docs.python.org](https://docs.python.org/3/library/_thread.html).

---

## Functions and constants

| API | Purpose |
|-----|---------|
| `start_new_thread(function, args, kwargs={})` | Begin thread; `args` must be a **tuple** |
| `allocate_lock()` | New unlocked lock (`LockType`) |
| `get_ident()` | Current thread id (cookie for thread-local dicts) |
| `get_native_id()` | OS thread id (3.8+, platform-dependent) |
| `exit()` | Raise `SystemExit` in current thread |
| `interrupt_main(signum=SIGINT)` | Schedule signal handler in main thread |
| `stack_size([size])` | Optional stack size for new threads (platform limits) |
| `TIMEOUT_MAX` | Upper bound for lock `acquire(timeout=...)` |
| `error` | Alias of `RuntimeError` (3.3+) |

---

## Lock objects

| Method | Behavior |
|--------|----------|
| `acquire(blocking=True, timeout=-1)` | Returns `True` if acquired; `timeout` in seconds when blocking |
| `release()` | Must be held; not required to be same thread that acquired (document carefully) |
| `locked()` | Whether any thread holds the lock |
| Context manager | `with lock:` supported |

```python
# Goal: start_new_thread requires a tuple for args
import _thread

seen = []

def record(value):
    seen.append(value)

_thread.start_new_thread(record, (42,))
import time
time.sleep(0.02)
assert 42 in seen
```

```python
# Goal: non-blocking acquire when lock is held
import _thread

lock = _thread.allocate_lock()
lock.acquire()
assert lock.locked()
assert lock.acquire(blocking=False) is False
lock.release()
assert not lock.locked()
```

---

## Caveats (from upstream)

| Topic | Detail |
|-------|--------|
| `KeyboardInterrupt` | Signals go to the **main** thread |
| `sys.exit()` / `SystemExit` | Same as `_thread.exit()` |
| Main thread exit | Other threads may be killed without `finally` (platform-defined) |
| Prefer `threading` | `excepthook`, daemon flag, `join()` |

---

## See also

- [threading](../threading-thread-based-parallelism/index.md) — recommended application API
- [Concurrent Execution hub](../index.md)
