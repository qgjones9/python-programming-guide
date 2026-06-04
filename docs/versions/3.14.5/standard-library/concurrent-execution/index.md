# [Concurrent Execution](https://docs.python.org/3/library/concurrency.html)

The [Concurrent Execution](https://docs.python.org/3/library/concurrency.html) chapter groups modules for **running work in parallel or in the background** within one process (threads, interpreters, schedulers) or across processes (multiprocessing, subprocesses). Picking the right tool depends on whether work is **CPU-bound** or **I/O-bound**, whether you need **shared memory** or **isolation**, and whether you prefer **callbacks/events** or **preemptive threads/processes**. Full API reference and platform notes remain on [docs.python.org](https://docs.python.org/3/library/concurrency.html).

---

## Choosing a concurrency model

| Workload | Typical tool | Why |
|----------|--------------|-----|
| Many blocking I/O calls (HTTP, files, sockets) | [`threading`](threading-thread-based-parallelism/index.md), [asyncio](https://docs.python.org/3/library/asyncio.html) | Threads release the GIL while waiting; asyncio avoids thread overhead |
| CPU-heavy Python code on multiple cores | [`multiprocessing`](multiprocessing-process-based-parallelism/index.md), [`concurrent.futures.ProcessPoolExecutor`](concurrentfutures-launching-parallel-tasks/index.md) | Separate interpreters bypass the GIL per process |
| Isolated Python runtimes in one process (3.14+) | [`concurrent.interpreters`](concurrentinterpreters-multiple-interpreters-in-the-same-process/index.md) | Subinterpreters + threads can use all cores without multiple processes |
| Run another program or shell pipeline | [`subprocess`](subprocess-subprocess-management/index.md) | OS-level process with its own memory |
| Producer/consumer between threads | [`queue`](queue-a-synchronized-queue-class/index.md) | Built-in locking for `put`/`get` |
| Request-scoped state (async, tasks) | [`contextvars`](contextvars-context-variables/index.md) | Safer than `threading.local()` in concurrent frameworks |
| Delayed or periodic callbacks (single-threaded) | [`sched`](sched-event-scheduler/index.md) | Priority queue of timed events |

```python
# Goal: classify a task — I/O wait vs CPU work
import time

def io_bound_simulated():
    time.sleep(0.01)  # stands in for blocking I/O
    return "done"

def cpu_bound(n):
    return sum(i * i for i in range(n))

assert io_bound_simulated() == "done"
assert cpu_bound(1000) == 332833500
```

---

## Layered APIs (low → high)

| Layer | Module | Role |
|-------|--------|------|
| OS threads | [`_thread`](_thread-low-level-threading-api/index.md) | `start_new_thread`, raw locks |
| Threading | [`threading`](threading-thread-based-parallelism/index.md) | `Thread`, `Lock`, `Event`, `local` |
| Process pools | [`multiprocessing`](multiprocessing-process-based-parallelism/index.md) | `Process`, `Pool`, IPC queues |
| High-level pools | [`concurrent.futures`](concurrentfutures-launching-parallel-tasks/index.md) | `ThreadPoolExecutor`, `ProcessPoolExecutor` |
| Subinterpreters | [`concurrent.interpreters`](concurrentinterpreters-multiple-interpreters-in-the-same-process/index.md) | Isolated interpreters in one process (3.14+) |
| Package hub | [`concurrent`](the-concurrent-package/index.md) | Namespace for futures and interpreters |

Shared **POSIX-style** segments for numeric/array data: [`multiprocessing.shared_memory`](multiprocessingshared_memory-shared-memory-for-direct-access-across-processes/index.md).

---

## GIL, free threading, and safety

With the default GIL build, **only one thread runs Python bytecode at a time**; threads still help for I/O and for calling into C extensions that release the GIL. For **true parallel CPU work** in one interpreter, use processes or (on 3.13+) a [free-threaded build](../../glossary/free-threaded-build/index.md). Container sharing rules: [Thread safety guarantees](../thread-safety-guarantees/index.md).

```python
# Goal: protect a multi-step update with threading.Lock
import threading

counter = 0
lock = threading.Lock()

def add_many(times):
    global counter
    for _ in range(times):
        with lock:
            counter += 1

threads = [threading.Thread(target=add_many, args=(100,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
assert counter == 400
```

---

## Common pitfalls

| Pitfall | Symptom | Mitigation |
|---------|---------|------------|
| Threads for CPU-bound pure Python | No speedup | `ProcessPoolExecutor` or multiprocessing |
| `multiprocessing` on Windows without `if __name__ == "__main__"` | Spawn recursion | Guard `Process`/`Pool` creation |
| `queue.empty()` then `get()` race | `Empty` anyway | Block on `get()` or use `join()` + `task_done()` |
| Mixing `concurrent.futures.Future` with `asyncio.Future` | Wrong await API | Use the Future type matching your runtime |
| `SharedMemory` without `unlink()` | Leaked segments | `close()` per handle; one `unlink()` when done |

---

## Sections in this repo

| Topic | Local page |
|-------|------------|
| Thread-based parallelism | [threading — Thread-based parallelism](threading-thread-based-parallelism/index.md) |
| Process-based parallelism | [multiprocessing — Process-based parallelism](multiprocessing-process-based-parallelism/index.md) |
| Shared memory across processes | [multiprocessing.shared_memory](multiprocessingshared_memory-shared-memory-for-direct-access-across-processes/index.md) |
| The concurrent package | [The concurrent package](the-concurrent-package/index.md) |
| Parallel task launchers | [concurrent.futures](concurrentfutures-launching-parallel-tasks/index.md) |
| Multiple interpreters | [concurrent.interpreters](concurrentinterpreters-multiple-interpreters-in-the-same-process/index.md) |
| Subprocess management | [subprocess](subprocess-subprocess-management/index.md) |
| Event scheduler | [sched](sched-event-scheduler/index.md) |
| Synchronized queues | [queue](queue-a-synchronized-queue-class/index.md) |
| Context variables | [contextvars](contextvars-context-variables/index.md) |
| Low-level threading | [_thread](_thread-low-level-threading-api/index.md) |
