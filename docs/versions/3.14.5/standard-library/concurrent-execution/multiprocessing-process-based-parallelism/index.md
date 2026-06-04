# [multiprocessing — Process-based parallelism](https://docs.python.org/3/library/multiprocessing.html)

The [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) module spawns **child processes** with an API that mirrors [`threading`](../threading-thread-based-parallelism/index.md): `Process`, locks, queues, and pools. Separate interpreters **bypass the GIL** for CPU-bound Python. IPC uses pickling over pipes or shared memory. Full guide (start methods, `Manager`, logging): [docs.python.org](https://docs.python.org/3/library/multiprocessing.html).

---

## Start methods — [Contexts and start methods](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods)

| Method | Behavior | Typical platform |
|--------|----------|------------------|
| `spawn` | Fresh interpreter; safest default (Windows, macOS 3.8+) | Cross-platform |
| `fork` | Copy parent process (Unix; fast but inherits parent state) | Linux default historically |
| `forkserver` | Server process forks workers | Unix optimization |

```python
# Goal: inspect available start methods
import multiprocessing as mp

methods = mp.get_all_start_methods()
assert "spawn" in methods
```

**Windows / spawn:** guard entry point with `if __name__ == "__main__":` before creating `Process` or `Pool`.

---

## `Process` and `Queue`

```python
# Goal: module exports and start-method introspection
import multiprocessing as mp

assert callable(mp.Process)
assert callable(mp.Queue)
assert mp.cpu_count() >= 1
assert "spawn" in mp.get_all_start_methods()
```

Guard `Process` / `Pool` creation with `if __name__ == "__main__":` when using **spawn** (required on Windows; recommended everywhere).

---

## Pools and executors

| API | Role |
|-----|------|
| `Pool(processes)` | `map`, `apply_async`, `imap` over worker processes |
| `ProcessPoolExecutor` | Same pool idea via [concurrent.futures](../concurrentfutures-launching-parallel-tasks/index.md) |
| `Manager()` | Shared proxy objects (`list`, `dict`, `Namespace`) in server process |

`maxtasksperchild` recycles workers after N tasks to curb memory growth.

---

## Synchronization and data

| Type | Use |
|------|-----|
| `Lock`, `RLock`, `Semaphore` | Cross-process locks |
| `Queue`, `Pipe` | Message passing |
| `Value`, `Array` | Shared ctypes scalars/arrays |
| `shared_memory` | [POSIX-style segments](../multiprocessingshared_memory-shared-memory-for-direct-access-across-processes/index.md) |

Only **picklable** objects cross process boundaries by default.

---

## Logging and debugging

Child processes need **`logging` configuration** re-applied after start. Use `multiprocessing.log_to_stderr()` or pass listener setup via `initializer` on pools.

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Forgot `__main__` guard | Wrap `Process`/`Pool` creation |
| Passing unpicklable lambdas | Use top-level functions |
| `fork` + threads in parent | Deadlock risk; prefer `spawn` |
| Large data per task | Use `initializer` + global or shared memory |

---

## See also

- [multiprocessing.shared_memory](../multiprocessingshared_memory-shared-memory-for-direct-access-across-processes/index.md)
- [subprocess](../subprocess-subprocess-management/index.md) — external programs
- [concurrent.futures](../concurrentfutures-launching-parallel-tasks/index.md)
