# [traceback — Print or retrieve a stack traceback](https://docs.python.org/3/library/traceback.html)

[`traceback`](https://docs.python.org/3/library/traceback.html) formats and prints **stack traces** outside the default exception hook — useful for logging, UIs, and testing. Python 3.11+ adds rich **`TracebackException`** objects with structured frame data. Reference: [docs.python.org](https://docs.python.org/3/library/traceback.html).

---

## Common functions

| API | Role |
|-----|------|
| `format_exc(limit=None, chain=True)` | String like printed traceback for active exception |
| `format_exception(exc_type, exc, tb, …)` | List of traceback strings |
| `print_exc(...)` | Write formatted traceback to stderr (default) |
| `extract_tb(tb, limit=…)` | List of `FrameSummary` tuples |
| `TracebackException.from_exception(exc, …)` | Structured traceback object (3.11+) |

Capture inside an `except` block — outside, `sys.exc_info()` is `(None, None, None)`.

---

## Example — formatting active exception

```python
# Goal: capture formatted traceback as string
import traceback

def boom():
    raise ValueError("demo failure")

try:
    boom()
except ValueError:
    text = traceback.format_exc()

assert "ValueError" in text
assert "demo failure" in text
assert "boom" in text
```

---

## Exception chaining

`chain=True` (default) includes **`__cause__`** and **`__context__`** sections (`The above exception was the direct cause…`). Pass `chain=False` to omit context links in logs.

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`logging.exception`** in handlers | Automatically includes traceback |
| Prefer **`TracebackException`** for structured UIs | Frame filenames/line numbers without parsing text |
| Limit **`limit=`** in tight loops | Avoid huge string builds |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Calling `format_exc()` outside `except` | `"NoneType: None\n"` | Capture inside handler |
| Logging tracebacks twice | Duplicate noise | One of logging or `print_exc` |

---

## See also

- [`sys`](../sys-system-specific-parameters-and-functions/index.md) — `exc_info()`, default excepthook
- [`warnings`](../warnings-warning-control/index.md) — separate channel from exceptions
