# [4.4. Runtime Components](https://docs.python.org/3/reference/executionmodel.html#runtime-components)

Python programs run on a **host** (OS, hardware). The reference describes a **conceptual** layering of process resources, threads, and Python-specific runtime state (global runtime → interpreter → thread state). Implementations may collapse layers; exposed APIs such as [`threading`](https://docs.python.org/3/library/threading.html) and the [`interpreters`](https://docs.python.org/3/library/interpreters.html) module map loosely to these ideas. Canonical text: [Runtime Components](https://docs.python.org/3/reference/executionmodel.html#runtime-components).

Parent: [4. Execution model](../index.md)

---

## 4.4.1. General computing model — [General Computing Model](https://docs.python.org/3/reference/executionmodel.html#general-computing-model)

| Layer | Role |
|-------|------|
| **Host machine** | Physical or virtual hardware + OS services |
| **Process** | Program instance; owns memory, file descriptors, environment |
| **Thread** | Independent execution of machine code within a process |

| Property | Processes | Threads (same process) |
|----------|-----------|-------------------------|
| Isolation | Strong | Weak — share address space |
| Creation cost | Higher | Lower |
| Coordination | IPC, files, sockets | Locks, queues; must avoid unsynchronized shared mutable state |

A Python program **starts with one thread**; it may add more via `threading` where the platform allows. Concurrent threads are **not synchronized** by default—shared memory can change underfoot.

```python
# Goal: threads share process-global objects; synchronize mutations
import threading

counter = {"n": 0}
lock = threading.Lock()

def worker():
    for _ in range(1000):
        with lock:
            counter["n"] += 1

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

assert counter["n"] == 4000
```

---

## 4.4.2. Python runtime model — [Python Runtime Model](https://docs.python.org/3/reference/executionmodel.html#python-runtime-model)

Conceptual stack for a running Python program:

| Layer | Holds (conceptually) |
|-------|----------------------|
| Process | Host resources |
| **Python global runtime** | Set of interpreters; shared implementation-defined resources |
| **Interpreter** | `sys.modules`, import machinery, much of “the Python you think of” |
| **Thread state** | Current exception, Python stack, per-thread interpreter bookkeeping |
| **Bytecode execution** | What runs Python code in a thread (not the same word as “interpreter” above) |

| Term | Clarification |
|------|----------------|
| **Main interpreter** | First interpreter; some implementations give it special duties |
| **Main thread** | Host thread where the runtime started; may handle signals |
| **Python thread** | Usually a `threading.Thread`; sometimes means a **thread state** |
| **Multiple interpreters** | Isolated `sys.modules` etc. in one process (`interpreters` module) |

```python
# Goal: each thread can hold thread-local data invisible to others
import threading

local = threading.local()

def set_and_read(value):
    local.tag = value
    return local.tag

results = []
t1 = threading.Thread(target=lambda: results.append(set_and_read("a")))
t2 = threading.Thread(target=lambda: results.append(set_and_read("b")))
t1.start()
t2.start()
t1.join()
t2.join()

assert sorted(results) == ["a", "b"]
```

```python
# Goal: asyncio coroutines typically run on one thread per loop
import asyncio

async def twice():
    await asyncio.sleep(0)
    return 2

assert asyncio.run(twice()) == 2
```

---

## Growing the runtime

| Mechanism | Effect |
|-----------|--------|
| [`threading`](https://docs.python.org/3/library/threading.html) | More host threads + thread states in an interpreter |
| [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html) / [`subprocess`](https://docs.python.org/3/library/subprocess.html) | Separate processes (stronger isolation) |
| [`interpreters`](https://docs.python.org/3/library/interpreters.html) | Additional interpreters in one process |
| [`asyncio`](https://docs.python.org/3/library/asyncio.html) | Concurrent coroutines, often single-threaded per event loop |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Unlocked reads/writes to shared lists/dicts | Rare corruption, heisenbugs | `threading.Lock`, `queue.Queue`, or processes |
| CPU-bound work on many threads (CPython) | GIL limits parallel CPU | `multiprocessing`, native extensions, or subprocess pool |
| Assuming “main thread” == “only thread” | Background threads keep running after main logic | Join daemons or use explicit shutdown |
| Mixing multiple interpreters casually | Objects must not cross interpreter boundaries | Read `interpreters` docs; share via IPC |
| Confusing **interpreter** vs **bytecode interpreter** | Misread runtime docs | Global “interpreter” = runtime instance; bytecode loop runs inside thread state |
