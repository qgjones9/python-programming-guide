# [Debugging and Profiling](https://docs.python.org/3/library/debug.html)

The **Debugging and Profiling** section covers **interactive debuggers**, **post-mortem tracebacks**, **execution profilers**, **timing micro-benchmarks**, **line tracing**, and **memory allocation tracking**. Auditing hooks (`sys.addaudithook`) provide security visibility into runtime events. Full reference: [debug.html](https://docs.python.org/3/library/debug.html).

---

## Module overview

| Module / topic | Primary use |
|----------------|-------------|
| [Audit events table](audit-events-table/index.md) | Catalog of `sys.audit` event names and arguments |
| [`bdb`](bdb-debugger-framework/index.md) | Base debugger framework used by `pdb` |
| [`faulthandler`](faulthandler-dump-the-python-traceback/index.md) | Dump tracebacks on crashes, hangs, or signals |
| [`pdb`](pdb-the-python-debugger/index.md) | Interactive source-level debugger |
| [The Python Profilers](the-python-profilers/index.md) | `cProfile` and `profile` deterministic profiling |
| [`timeit`](timeit-measure-execution-time-of-small-code-snippets/index.md) | Micro-benchmark small snippets |
| [`trace`](trace-trace-or-track-python-statement-execution/index.md) | Line coverage and execution counts |
| [`tracemalloc`](tracemalloc-trace-memory-allocations/index.md) | Track Python memory allocations |

---

## Choosing a tool

| Goal | Tool |
|------|------|
| Step through code interactively | [`pdb`](pdb-the-python-debugger/index.md) |
| Find slow functions in production-like runs | [`cProfile`](the-python-profilers/index.md) |
| Compare two implementations' speed | [`timeit`](timeit-measure-execution-time-of-small-code-snippets/index.md) |
| Find memory leaks or spikes | [`tracemalloc`](tracemalloc-trace-memory-allocations/index.md) |
| See which lines ran during a test | [`trace`](trace-trace-or-track-python-statement-execution/index.md) |
| Debug segfaults / deadlock dumps | [`faulthandler`](faulthandler-dump-the-python-traceback/index.md) |
| Monitor security-sensitive operations | [Audit hooks](audit-events-table/index.md) |

```python
# Goal: quick timing vs profiling decision
import timeit
import cProfile
import io

elapsed = timeit.timeit("sum(range(1000))", number=10000)
assert elapsed > 0

pr = cProfile.Profile()
pr.enable()
sum(range(1000))
pr.disable()
stats = pr.getstats()
assert len(stats) > 0
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [Audit events table](audit-events-table/index.md) | `sys.audit` events for imports, compilation, sockets, and more |
| [bdb — Debugger framework](bdb-debugger-framework/index.md) | Breakpoints, stepping, and debugger base classes |
| [faulthandler — Dump the Python traceback](faulthandler-dump-the-python-traceback/index.md) | Fatal error and timeout traceback dumps |
| [pdb — The Python Debugger](pdb-the-python-debugger/index.md) | Post-mortem and inline breakpoints |
| [The Python Profilers](the-python-profilers/index.md) | `cProfile`, `profile`, and `pstats` analysis |
| [timeit — Measure execution time of small code snippets](timeit-measure-execution-time-of-small-code-snippets/index.md) | Reliable micro-benchmarks |
| [trace — Trace or track Python statement execution](trace-trace-or-track-python-statement-execution/index.md) | Coverage reports and execution tracing |
| [tracemalloc — Trace memory allocations](tracemalloc-trace-memory-allocations/index.md) | Allocation snapshots and top statistics |
