# [resource — Resource usage information](https://docs.python.org/3/library/resource.html)

The [`resource`](https://docs.python.org/3/library/resource.html) module reports **process resource usage** and sets **soft/hard limits** for CPU time, memory, file descriptors, and core size on Unix (`getrusage`, `getrlimit`, `setrlimit`). Unix-only. Full resource ID tables remain on [docs.python.org](https://docs.python.org/3/library/resource.html).

Related: [`os.times`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md); [`signal`](../../generic-operating-system-services/signal-set-handlers-for-asynchronous-events/index.md) for `SIGXCPU`.

---

## Core functions — [Resource Limits](https://docs.python.org/3/library/resource.html#resource-limits)

| Function | Role |
|----------|------|
| `resource.getrusage(who)` | CPU/time stats (`RUSAGE_SELF`, `RUSAGE_CHILDREN`) |
| `resource.getrlimit(resource)` | Current `(soft, hard)` limit pair |
| `resource.setrlimit(resource, limits)` | Set limits (may require privileges) |
| `resource.getpagesize()` | System page size in bytes |

```python
# Goal: read CPU user time for current process (Unix)
import importlib.util

if importlib.util.find_spec("resource"):
    import resource

    usage = resource.getrusage(resource.RUSAGE_SELF)
    assert usage.ru_utime >= 0.0
    assert usage.ru_maxrss >= 0
else:
    import sys

    assert sys.platform == "win32"
```

---

## Common limit constants

| Constant | Limits |
|----------|--------|
| `RLIMIT_CPU` | CPU seconds (`SIGXCPU` / `SIGKILL`) |
| `RLIMIT_NOFILE` | Open file descriptors |
| `RLIMIT_AS` / `RLIMIT_DATA` | Address space / data segment |
| `RLIMIT_CORE` | Core dump size |

```python
# Goal: inspect NOFILE soft/hard limits (Unix)
import importlib.util

if importlib.util.find_spec("resource"):
    import resource

    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    assert 0 <= soft <= hard or hard == resource.RLIM_INFINITY
```

---

## `getrusage` fields (selected)

| Field | Meaning |
|-------|---------|
| `ru_utime` / `ru_stime` | User / system CPU seconds |
| `ru_maxrss` | Peak resident set size |
| `ru_majflt` / `ru_minflt` | Page fault counts |

---

## Best practices

| Practice | Why |
|----------|-----|
| Lower limits in **sandboxed workers** | Contain runaway jobs |
| Never assume **`RLIM_INFINITY`** fits in `int` on all platforms | Compare carefully |
| Use **`time.monotonic()`** for wall-clock; `getrusage` for CPU | Different metrics |

---

## See also

- [`os.times`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md) — lighter-weight timing
- [`subprocess`](../../subprocess-management/subprocess-subprocess-management/index.md) — child `RUSAGE_CHILDREN`
