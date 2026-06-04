# [trace — Trace or track Python statement execution](https://docs.python.org/3/library/trace.html)

The **`trace`** module monitors **which lines execute** and how often—useful for coverage-style reports and debugging unexpected control flow. It can run as **`python -m trace`**. Canonical reference: [trace.html](https://docs.python.org/3/library/trace.html).

---

## Purpose

Unlike [`cProfile`](the-python-profilers/index.md) (function timing), `trace` focuses on **line execution counts** and optional **coverage** reports showing missed lines.

---

## Key components

| Name | Role |
|------|------|
| `Trace(count, trace, countfiles)` | Programmatic tracer |
| `Trace.runfunc(func, *args)` | Run callable under trace |
| `Trace.run(code, filename)` | Execute source string |
| CLI `-m trace --count` | Generate annotated listings |

---

## Example — count line executions

```python
import trace

tracer = trace.Trace(count=True, trace=False)

def sample():
    x = 0
    for i in range(3):
        x += i
    return x

result = tracer.runfunc(sample)
assert result == 3
results = tracer.results
assert results is not None
```

---

## Example — run code object with tracing

```python
import trace

code = compile("a = 1 + 2\na", "<demo>", "exec")
tr = trace.Trace(count=True, trace=False)
tr.run(code)
assert tr.results is not None
```

---

## CLI patterns (interactive session)

| Flag | Effect |
|------|--------|
| `--count` | Prefix line counts in `--file` output |
| `--trace` | Print lines as executed |
| `--listfuncs` | Print functions as entered |
| `--missing` | Report lines never run |

---

## Best practices

| Practice | Why |
|----------|-----|
| Combine with unit tests | Shows dead branches after test runs |
| Filter stdlib with `--ignore-dir` | Keeps reports focused on your package |
| Prefer dedicated coverage tools for CI | `coverage.py` integrates with pytest |

---

## See also

- [`sys.settrace`](https://docs.python.org/3/library/sys.html#sys.settrace)
- [`tracemalloc`](tracemalloc-trace-memory-allocations/index.md)
