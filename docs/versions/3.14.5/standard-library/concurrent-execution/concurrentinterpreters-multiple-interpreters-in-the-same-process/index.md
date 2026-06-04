# [concurrent.interpreters — Multiple interpreters in the same process](https://docs.python.org/3/library/concurrent.interpreters.html)

The [`concurrent.interpreters`](https://docs.python.org/3/library/concurrent.interpreters.html) module (3.14+) exposes **subinterpreters**: separate Python execution contexts in **one OS process**, each with isolated import state and `__main__`. Interpreters alone do not schedule work — combine with **threads** (`call_in_thread`) for parallelism. Subinterpreters can run **without sharing the GIL** (since 3.12), enabling multi-core use in a single process. Not available on WASI. Reference: [docs.python.org](https://docs.python.org/3/library/concurrent.interpreters.html).

---

## Key concepts — [Key details](https://docs.python.org/3/library/concurrent.interpreters.html#key-details)

| Property | Implication |
|----------|-------------|
| Isolated by default | No accidental cross-interpreter mutation |
| No implicit threads | You start OS threads explicitly |
| Limited sharing | Most objects copied via pickle; some immutables shared efficiently |
| Not for security boundaries | Same address space — extension modules can break isolation |

---

## Module functions

| Function | Returns |
|----------|---------|
| `create()` | New idle `Interpreter` |
| `get_current()` / `get_main()` | `Interpreter` wrappers |
| `list_all()` | All interpreters |
| `create_queue()` | Cross-interpreter `Queue` |

---

## `Interpreter` methods

| Method | Role |
|--------|------|
| `exec(code)` | Run source in interpreter’s `__main__` (current thread) |
| `call(callable, *args, **kwargs)` | Run callable; return value copied back |
| `call_in_thread(callable, ...)` | Run in new thread bound to interpreter |
| `prepare_main(ns=None, **kwargs)` | Bind names into subinterpreter `__main__` |
| `close()` | Destroy interpreter |

```python
# Goal: create interpreter and call a function (3.14+)
import sys

if sys.version_info >= (3, 14):
    from concurrent import interpreters

    interp = interpreters.create()

    def add(a, b):
        return a + b

    assert interp.call(add, 3, 4) == 7
    interp.close()
```

```python
# Goal: exec runs code in subinterpreter __main__ (3.14+)
import sys

if sys.version_info >= (3, 14):
    from concurrent import interpreters

    interp = interpreters.create()
    interp.exec("RESULT = 2 + 2")
    assert interp.call(lambda: RESULT) == 4
    interp.close()
```

---

## Cross-interpreter `Queue`

`create_queue()` returns a `queue.Queue`-like object whose items are **copied or shared** per type rules — primary message path between interpreters ([Communicating Between Interpreters](https://docs.python.org/3/library/concurrent.interpreters.html#communicating-between-interpreters)).

```python
# Goal: pass data through interpreter queue (3.14+)
import sys

if sys.version_info >= (3, 14):
    from concurrent import interpreters

    q = interpreters.create_queue()
    q.put("ping")
    assert q.get() == "ping"
```

---

## Concurrency model

Think **CSP/actors**: interpreters as isolated workers, threads as carriers, queues as channels. [`InterpreterPoolExecutor`](../concurrentfutures-launching-parallel-tasks/index.md) offers a familiar pool API over this stack.

Extension authors: [Isolating Extension Modules](https://docs.python.org/3/howto/isolating-extensions.html).

---

## Exceptions

| Type | When |
|------|------|
| `InterpreterError` | General failure |
| `InterpreterNotFoundError` | Target interpreter gone |
| `ExecutionFailed` | Uncaught exception in subinterpreter (`excinfo`) |
| `NotShareableError` | Object cannot cross boundary |

---

## See also

- [concurrent.futures](../concurrentfutures-launching-parallel-tasks/index.md) — `InterpreterPoolExecutor`
- [multiprocessing](../multiprocessing-process-based-parallelism/index.md) — process isolation (stronger)
- [The concurrent package](../the-concurrent-package/index.md)
