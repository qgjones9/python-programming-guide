# [inspect — Inspect live objects](https://docs.python.org/3/library/inspect.html)

[`inspect`](https://docs.python.org/3/library/inspect.html) introspects **live Python objects**: signatures, source code, stack frames, coroutine status, class hierarchies, and AST helpers. Frameworks (pytest, FastAPI, IDEs) depend on it for reflection. Reference: [docs.python.org](https://docs.python.org/3/library/inspect.html).

---

## Frequently used API

| Function | Role |
|----------|------|
| `signature(callable)` | `Signature` with parameters and defaults |
| `getsource(obj)` | Source text (requires `.py` file) |
| `getfile(obj)` / `getmodule(obj)` | Origin file/module |
| `stack()` / `currentframe()` | Stack frame records |
| `isfunction`, `ismethod`, `isclass`, `iscoroutinefunction`, … | Type guards |
| `getmembers(obj, predicate=…)` | `(name, value)` pairs |
| `cleandoc(docstring)` | Normalize docstring indentation |

---

## Signatures and binding

```python
# Goal: introspect function parameters
import inspect

def greet(name: str, loud: bool = False) -> str:
    """Return a greeting, optionally uppercased."""
    return name.upper() if loud else name

sig = inspect.signature(greet)
params = list(sig.parameters)
assert params == ["name", "loud"]
bound = sig.bind("alice", loud=True)
assert bound.arguments["loud"] is True
assert "greeting" in inspect.getdoc(greet)
```

---

## Frames and stacks

`inspect.stack()` returns list of `FrameInfo` named tuples — useful for logging caller context. Avoid holding frame references longer than necessary (reference cycles with locals).

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer **`signature()` over `__code__.co_varnames`** | Handles keyword-only and positional-only params |
| Use **`getsource` failures** gracefully | Extension modules lack Python source |
| Pair with [`annotationlib`](../annotationlib-functionality-for-introspecting-annotations/index.md) on 3.14+ | Annotations may be deferred |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| `getsource` on REPL-defined functions | OSError / no file | Guard with try/except |
| Inspecting wrapped functions | Misses decorator metadata | `inspect.unwrap()` |
| `stack()` in hot paths | Allocates frame copies | Cache or log at coarser granularity |

---

## See also

- [`annotationlib`](../annotationlib-functionality-for-introspecting-annotations/index.md) — annotation-specific introspection
- [`dataclasses`](../dataclasses-data-classes/index.md) — generated methods visible via inspect
