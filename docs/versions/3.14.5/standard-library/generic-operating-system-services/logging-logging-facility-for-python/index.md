# [logging — Logging facility for Python](https://docs.python.org/3/library/logging.html)

The [`logging`](https://docs.python.org/3/library/logging.html) module implements **hierarchical, level-filtered event logging** for applications and libraries. Loggers named with `getLogger(__name__)` forward records up the namespace tree to handlers on ancestor loggers (typically the root). Handlers write to files, stderr, or custom destinations; formatters control layout. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/logging.html).

Related: [`logging.config`](../loggingconfig-logging-configuration/index.md) for dict/file configuration; [`logging.handlers`](../logginghandlers-logging-handlers/index.md) for rotation and network handlers; [`warnings`](../../development-tools/warnings-warning-control/index.md) for non-logging alerts.

---

## Core objects — overview

| Type | Role |
|------|------|
| `Logger` | Application-facing API: `debug`, `info`, `warning`, `error`, `critical` |
| `Handler` | Sends `LogRecord` to a destination (stream, file, socket) |
| `Formatter` | Layout string (`%(levelname)s`, `%(message)s`, …) |
| `Filter` | Fine-grained record acceptance beyond level |
| `LogRecord` | Snapshot of event metadata at emit time |

---

## Logger usage — [Logger Objects](https://docs.python.org/3/library/logging.html#logger-objects)

| API | Notes |
|-----|-------|
| `logging.getLogger(name=None)` | Never instantiate `Logger` directly |
| `logger.setLevel(level)` | Threshold for this logger |
| `logger.propagate` | If `True` (default), bubble to parent handlers |
| `logging.basicConfig(**kwargs)` | One-shot root setup (stream/file, level, format) |
| `logging.lastResort` | stderr handler when no config (warning+) |

```python
# Goal: module logger with hierarchical name
import logging

log = logging.getLogger("myapp.worker")
assert log.name == "myapp.worker"
assert logging.getLogger("myapp.worker") is log
```

```python
# Goal: capture log output in memory
import io
import logging

root = logging.getLogger()
root.handlers.clear()
buf = io.StringIO()
h = logging.StreamHandler(buf)
h.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
root.addHandler(h)
root.setLevel(logging.DEBUG)

child = logging.getLogger("app.worker")
child.info("started")
assert buf.getvalue().strip() == "INFO:app.worker:started"
root.handlers.clear()
```

```python
# Goal: level filtering on a logger
import logging

log = logging.getLogger("demo.levels")
log.setLevel(logging.WARNING)
assert log.isEnabledFor(logging.INFO) is False
assert log.isEnabledFor(logging.ERROR) is True
```

---

## Levels — [Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels)

| Constant | Value | Typical use |
|----------|-------|-------------|
| `DEBUG` | 10 | Verbose diagnostics |
| `INFO` | 20 | Normal operational messages |
| `WARNING` | 30 | Unexpected but handled situations |
| `ERROR` | 40 | Feature failure |
| `CRITICAL` | 50 | Process-level failure |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`getLogger(__name__)`** in every module | Names mirror package hierarchy |
| Configure **root once** at startup | Avoid duplicate handlers via propagation |
| Prefer **`logger.exception`** in except blocks | Includes traceback automatically |
| Use **`%` formatting** in log calls (`logger.info("x=%s", x)`) | Defers string work if level disabled |
| Avoid **`print`** for operational events | Loses levels, routing, and test hooks |
| Attach handlers to **one** logger in the chain | Prevents duplicate lines |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`basicConfig` too late** | No handlers on root | Call before other modules log |
| **Handler on child + propagate True** | Duplicate lines on root | Handler only on root or set `propagate=False` |
| **Logging in import time** | Runs before config | Defer to `main()` or lazy setup |
| **`debug(f"{expensive}")`** | f-string always evaluated | Pass args: `debug("v=%s", expensive())` |
| **Pickling loggers** | Not supported | Pass logger name and re-fetch |

---

## Configuration entry points

| Approach | When |
|----------|------|
| `logging.basicConfig` | Scripts and quick prototypes |
| `logging.config.dictConfig` | JSON/YAML-driven apps |
| `logging.config.fileConfig` | INI-style legacy configs |
| Manual `Handler`/`Formatter` | Libraries that must not configure global logging |

See [`logging.config`](../loggingconfig-logging-configuration/index.md) and [`logging.handlers`](../logginghandlers-logging-handlers/index.md) for production wiring.
