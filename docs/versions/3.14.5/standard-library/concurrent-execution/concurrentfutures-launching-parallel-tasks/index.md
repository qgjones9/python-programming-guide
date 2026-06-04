# [concurrent.futures — Launching parallel tasks](https://docs.python.org/3/library/concurrent.futures.html)

The [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html) module provides a **high-level executor interface** for running callables asynchronously via **threads**, **processes**, or **interpreters** (3.14+). All concrete executors share `submit()`, `map()`, and `shutdown()`. Do not confuse `concurrent.futures.Future` with `asyncio.Future`. Added in 3.2. Reference: [docs.python.org](https://docs.python.org/3/library/concurrent.futures.html).

---

## Executor types

| Class | Backend | Best for |
|-------|---------|----------|
| `ThreadPoolExecutor` | OS threads | I/O-bound, shared memory |
| `ProcessPoolExecutor` | Child processes | CPU-bound Python (picklable targets) |
| `InterpreterPoolExecutor` | Subinterpreters (3.14+) | CPU parallelism in one process |

Use as a **context manager** so `shutdown(wait=True)` runs automatically.

```python
# Goal: ThreadPoolExecutor.submit and Future.result
from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=2) as ex:
    fut = ex.submit(square, 9)
    assert fut.result() == 81
```

```python
# Goal: map applies fn to iterables in parallel
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as ex:
    out = list(ex.map(lambda x: x + 1, range(5)))
assert out == [1, 2, 3, 4, 5]
```

---

## `Future` objects

| Method | Behavior |
|--------|----------|
| `result(timeout=None)` | Return value; re-raises worker exception |
| `exception(timeout=None)` | Exception object or `None` |
| `done()` / `running()` / `cancelled()` | State queries |
| `add_done_callback(fn)` | `fn(future)` when complete |
| `cancel()` | May fail if already running |

```python
# Goal: exception surfaces at result()
from concurrent.futures import ThreadPoolExecutor

def boom():
    raise ValueError("fail")

with ThreadPoolExecutor(max_workers=1) as ex:
    fut = ex.submit(boom)
    err = None
    try:
        fut.result()
    except ValueError as e:
        err = e
assert str(err) == "fail"
```

---

## `shutdown` and pitfalls

| Parameter | Effect |
|-----------|--------|
| `wait=True` | Block until pending futures finish |
| `cancel_futures=True` (3.9+) | Cancel not-yet-started work |

**Deadlock warning:** a worker waiting on another `Future` from the **same** pool with `max_workers` too small can stall forever (classic circular `result()` wait).

`ProcessPoolExecutor.map(..., chunksize=n)` batches iterables for efficiency on large inputs.

---

## Module helpers

| Function | Role |
|----------|------|
| `wait(fs, timeout=None, return_when=ALL_COMPLETED)` | Block on a set of futures |
| `as_completed(fs, timeout=None)` | Iterator yielding futures as they finish |

```python
# Goal: as_completed yields in finish order
from concurrent import futures

def slow(n):
    import time
    time.sleep(0.01 * (3 - n))
    return n

with futures.ThreadPoolExecutor(max_workers=3) as ex:
    futs = [ex.submit(slow, i) for i in range(3)]
    order = [f.result() for f in futures.as_completed(futs)]
assert len(order) == 3 and set(order) == {0, 1, 2}
```

---

## See also

- [threading](../threading-thread-based-parallelism/index.md) — underlying threads
- [multiprocessing](../multiprocessing-process-based-parallelism/index.md) — underlying processes
- [concurrent.interpreters](../concurrentinterpreters-multiple-interpreters-in-the-same-process/index.md) — `InterpreterPoolExecutor`
- [The concurrent package](../the-concurrent-package/index.md)
