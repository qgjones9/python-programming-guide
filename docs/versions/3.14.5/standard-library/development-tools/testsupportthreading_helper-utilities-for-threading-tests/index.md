# [test.support.threading_helper — Utilities for threading tests](https://docs.python.org/3/library/test.html#module-test.support.threading_helper)

`test.support.threading_helper` collects **thread lifecycle helpers** for the stdlib test suite: joining with timeouts, starting daemon threads safely, and avoiding hangs in regrtest. Canonical reference: [test.html#module-test.support.threading_helper](https://docs.python.org/3/library/test.html#module-test.support.threading_helper).

---

## Purpose

Threading tests flake when joins block forever. These helpers standardize **bounded waits** and cleanup patterns across `test_threading`, `test_queue`, and asyncio/thread interaction tests.

---

## Key helpers

| Name | Role |
|------|------|
| `join_thread(thread, timeout=...)` | Join or fail with clear timeout |
| `start_threads` | Context manager starting multiple threads |
| `reap_threads` | Ensure no stray threads remain |

---

## Example — join with timeout succeeds

```python
import threading
import test.support.threading_helper as th

def worker():
    pass

t = threading.Thread(target=worker)
t.start()
th.join_thread(t, timeout=5.0)
assert not t.is_alive()
```

---

## Example — start_threads context manager

```python
import threading
import test.support.threading_helper as th

results = []

def task(n):
    results.append(n)

threads = [threading.Thread(target=task, args=(i,)) for i in range(3)]
with th.start_threads(threads):
    pass
assert sorted(results) == [0, 1, 2]
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Always join or daemonize test threads | Prevents regrtest shutdown warnings |
| Use explicit timeouts in CI | Hung threads fail fast |
| Prefer `threading.Event` for coordination | Clearer than sleep polling |

---

## See also

- [`threading`](https://docs.python.org/3/library/threading.html)
- [`test.support`](testsupport-utilities-for-the-python-test-suite/index.md)
