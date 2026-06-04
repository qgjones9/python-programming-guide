# [sys — System-specific parameters and functions](https://docs.python.org/3/library/sys.html)

The [`sys`](https://docs.python.org/3/library/sys.html) module exposes **interpreter implementation details**: command-line arguments, module search path, standard streams, recursion limits, async policy hooks, and audit events. Values differ by platform and build options. Canonical reference: [docs.python.org](https://docs.python.org/3/library/sys.html).

---

## Commonly used attributes

| Name | Role |
|------|------|
| `argv` | Command-line arguments (`argv[0]` is script or `-c` string) |
| `path` | Module search path (mutable list) |
| `version_info` | Tuple-like major/minor/micro/release level |
| `platform` | Substring identifying OS (`linux`, `win32`, …) |
| `stdin`, `stdout`, `stderr` | Standard I/O streams |
| `modules` | Dict of imported modules |
| `exc_info()` | Active exception `(type, value, traceback)` in handler |
| `exit()` / `exitfunc` legacy | Raise `SystemExit` with optional status |

---

## Functions and hooks

| API | Purpose |
|-----|---------|
| `getrecursionlimit()` / `setrecursionlimit()` | C stack depth guard for Python calls |
| `getsizeof(obj, default=…)` | Shallow size in bytes |
| `intern(string)` | Dedup immutable strings (implementation detail) |
| `settrace` / `setprofile` | Legacy tracing (see also [`sys.monitoring`](../sysmonitoring-execution-event-monitoring/index.md)) |
| `addaudithook(hook)` | Security auditing callbacks |
| `displayhook` | REPL expression result printing |

```python
# Goal: read interpreter identity and tweak path safely
import sys

major, minor = sys.version_info[:2]
assert major >= 3
original_len = len(sys.path)
sys.path.append("/tmp/demo")
assert len(sys.path) == original_len + 1
sys.path.pop()
assert sys.getrecursionlimit() > 100
```

---

## Standard streams and encoding

`sys.stdout.encoding` may be `None` when attached to a binary buffer; reconfigure with `reconfigure()` (3.7+) or wrap with `io.TextIOWrapper`. Line buffering behavior depends on TTY detection.

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`sys.version_info`** over parsing `version` string | Stable numeric comparisons |
| Avoid mutating **`sys.modules`** casually | Breaks import invariants |
| Use **`sys.exit(code)`** in CLI apps | Raises `SystemExit`; flushes stdio |
| Register **audit hooks** sparingly | Called on security-sensitive operations |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Assuming `platform == os.name` | Different granularity | Use both or `platform.system()` |
| Huge recursion limit | C stack overflow crash | Raise limit only when measured need |
| Reading `exc_info()` outside `except` | `(None, None, None)` | Capture inside handler |

---

## See also

- [`sys.monitoring`](../sysmonitoring-execution-event-monitoring/index.md) — modern event monitoring namespace
- [`sysconfig`](../sysconfig-provide-access-to-pythons-configuration-information/index.md) — build/install paths
- [`builtins`](../builtins-built-in-objects/index.md) — separate module for built-in names
