# [threading — Thread-based parallelism](https://docs.python.org/3/library/threading.html)

The [`threading`](https://docs.python.org/3/library/threading.html) module builds a **high-level threading API** on [`_thread`](../_thread-low-level-threading-api/index.md): `Thread` objects, locks, events, conditions, semaphores, and `Thread-local` storage. Use it when work is **I/O-bound** or when you need background tasks in **one process** with shared memory. Not available on WASI. Full reference: [docs.python.org](https://docs.python.org/3/library/threading.html).

---

## GIL and when threads help

CPython’s [GIL](../../../glossary/global-interpreter-lock/index.md) lets only one thread execute Python bytecode at a time, so **CPU-bound pure Python** rarely speeds up with threads. Threads still help when code **blocks on I/O** or calls C extensions that release the GIL. For multi-core CPU work, prefer [`multiprocessing`](../multiprocessing-process-based-parallelism/index.md) or [`concurrent.futures.ProcessPoolExecutor`](../concurrentfutures-launching-parallel-tasks/index.md). Free-threaded builds (3.13+) can disable the GIL — see [Thread safety guarantees](../../thread-safety-guarantees/index.md).

---

## `Thread` basics — [Introduction](https://docs.python.org/3/library/threading.html#introduction)

| Parameter | Role |
|-----------|------|
| `target` | Callable to run |
| `args` | Tuple of positional arguments |
| `kwargs` | Dict of keyword arguments |
| `daemon` | Process exits without waiting for daemon threads |
| `name` | Debug label |

```python
# Goal: run work in a background thread and join
import threading

results = []

def worker(x):
    results.append(x * 2)

t = threading.Thread(target=worker, args=(21,))
t.start()
t.join()
assert results == [42]
```

```python
# Goal: Event coordinates producer and consumer
import threading

ready = threading.Event()
data = {}

def producer():
    data["value"] = 7
    ready.set()

def consumer():
    ready.wait()
    return data["value"]

t = threading.Thread(target=producer)
t.start()
assert consumer() == 7
t.join()
```

---

## Synchronization primitives

| Type | Use case |
|------|----------|
| `Lock` / `RLock` | Mutual exclusion; `RLock` for re-entrant code |
| `Event` | One-shot or persistent flag |
| `Condition` | Wait for a predicate with associated lock |
| `Semaphore` / `BoundedSemaphore` | Limit concurrent access (pool slots) |
| `Barrier` | Fixed party count rendezvous |

```python
# Goal: Lock makes counter updates atomic
import threading

total = 0
lock = threading.Lock()

def add(n):
    global total
    for _ in range(n):
        with lock:
            total += 1

threads = [threading.Thread(target=add, args=(100,)) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
assert total == 500
```

---

## Module-level helpers

| Function | Returns |
|----------|---------|
| `active_count()` | Number of alive threads |
| `current_thread()` | `Thread` for caller |
| `enumerate()` | List of alive `Thread` objects |
| `main_thread()` | Main thread object |
| `excepthook` | Hook for uncaught exceptions in `Thread.run` (3.8+) |

`threading.local()` stores **per-thread** attributes; for asyncio-aware code prefer [`contextvars`](../contextvars-context-variables/index.md).

---

## `ThreadPoolExecutor` shortcut

For fire-and-forget or pooled I/O, [`concurrent.futures`](../concurrentfutures-launching-parallel-tasks/index.md) wraps threads with `Future` results. Pair with [`queue`](../queue-a-synchronized-queue-class/index.md) for explicit work queues.

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Data races on shared mutable objects | Lock around multi-step invariants; see [thread safety](../../thread-safety-guarantees/index.md) |
| Daemon thread still running at exit | `join()` or graceful shutdown flag |
| Deadlock with nested locks | Fixed lock order or `RLock` |
| `time.sleep` in CPU-bound threads | Does not parallelize Python compute |

---

## See also

- [_thread](../_thread-low-level-threading-api/index.md) — low-level API
- [queue](../queue-a-synchronized-queue-class/index.md) — thread-safe queues
- [concurrent.futures](../concurrentfutures-launching-parallel-tasks/index.md) — pool executor
