# [The concurrent package](https://docs.python.org/3/library/concurrent.html)

The [`concurrent`](https://docs.python.org/3/library/concurrent.html) namespace groups **high-level concurrency helpers** added in the 3.x series. It is not a single implementation module — import from submodules instead. Official listing: [docs.python.org](https://docs.python.org/3/library/concurrent.html).

---

## Submodules

| Submodule | Purpose |
|-----------|---------|
| [`concurrent.futures`](../concurrentfutures-launching-parallel-tasks/index.md) | `ThreadPoolExecutor`, `ProcessPoolExecutor`, `Future` (since 3.2) |
| [`concurrent.interpreters`](../concurrentinterpreters-multiple-interpreters-in-the-same-process/index.md) | Subinterpreter lifecycle and cross-interpreter queues (since 3.14) |

```python
# Goal: confirm submodules are importable (interpreters requires 3.14+)
import sys
import concurrent.futures

assert hasattr(concurrent.futures, "ThreadPoolExecutor")
if sys.version_info >= (3, 14):
    import concurrent.interpreters

    assert hasattr(concurrent.interpreters, "create")
```

---

## When to use which submodule

| Need | Import |
|------|--------|
| Map/filter work over a thread or process pool | `concurrent.futures` |
| Isolated Python heaps in one OS process | `concurrent.interpreters` |
| Raw `threading` or `multiprocessing` control | See sibling pages under [Concurrent Execution](../index.md) |

---

## See also

- [concurrent.futures — Launching parallel tasks](../concurrentfutures-launching-parallel-tasks/index.md)
- [concurrent.interpreters — Multiple interpreters](../concurrentinterpreters-multiple-interpreters-in-the-same-process/index.md)
- [Concurrent Execution hub](../index.md)
