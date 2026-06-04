# [sys.monitoring — Execution event monitoring](https://docs.python.org/3/library/sys.monitoring.html)

[`sys.monitoring`](https://docs.python.org/3/library/sys.monitoring.html) is a **namespace inside `sys`**, not an importable top-level module. It provides a low-overhead API for **execution event callbacks** — calls, lines, returns, branches, exceptions — used by debuggers, coverage tools, and profilers (Python 3.12+). Reference: [docs.python.org](https://docs.python.org/3/library/sys.monitoring.html).

```python
import sys  # not: import sys.monitoring
```

---

## Tool identifiers — [Tool identifiers](https://docs.python.org/3/library/sys.monitoring.html#tool-identifiers)

| Constant | Reserved for |
|----------|--------------|
| `DEBUGGER_ID = 0` | Debuggers |
| `COVERAGE_ID = 1` | Coverage |
| `PROFILER_ID = 2` | Profilers |
| `OPTIMIZER_ID = 5` | Optimizers |

IDs 0–5 inclusive must be claimed with `use_tool_id(id, name)` before use. Release with `free_tool_id(id)`.

---

## Events — [Events](https://docs.python.org/3/library/sys.monitoring.html#events)

Events are **bit flags** OR'd together: `PY_START`, `PY_RETURN`, `CALL`, `LINE`, `RAISE`, branch/jump/instruction events, and others. **`BRANCH`** is deprecated in 3.14 — prefer `BRANCH_LEFT` / `BRANCH_RIGHT`.

Return **`sys.monitoring.DISABLE`** from a callback to turn off monitoring at that code location for performance (breakpoints pattern).

---

## Registering callbacks — [Registering callback functions](https://docs.python.org/3/library/sys.monitoring.html#registering-callback-functions)

1. `use_tool_id(tool_id, "name")`
2. `register_callback(tool_id, event, func)` — pass `None` to unregister
3. `set_events(tool_id, event_set)` globally and/or `set_local_events` per code object

```python
# Goal: count CALL events for a simple function
import sys

TOOL = sys.monitoring.PROFILER_ID
seen = []

def on_call(code, offset, callable_obj, arg0):
    seen.append(getattr(callable_obj, "__name__", repr(callable_obj)))

sys.monitoring.use_tool_id(TOOL, "demo")
sys.monitoring.register_callback(TOOL, sys.monitoring.events.CALL, on_call)
sys.monitoring.set_events(TOOL, sys.monitoring.events.CALL)

def target():
    return 42

assert target() == 42
assert "target" in seen
sys.monitoring.free_tool_id(TOOL)
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Return **`DISABLE`** outside hot paths | Keeps overhead near zero until breakpoint hit |
| Call **`restart_events()`** after disabling | Re-enables locations turned off via DISABLE |
| Pick a **reserved tool ID** when possible | Reduces collisions between tools |
| Prefer **`sys.monitoring`** over `settrace` for new tools | Finer-grained event control |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `import sys.monitoring` | `ModuleNotFoundError` | `import sys` then `sys.monitoring` |
| Reusing unclaimed tool ID | `ValueError` | Always `use_tool_id` first |
| Returning non-DISABLE objects from callbacks | Ignored | Only DISABLE has effect |

---

## See also

- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — parent module
- [Monitoring C API](https://docs.python.org/3/c-api/monitoring.html) — same events from C extensions
