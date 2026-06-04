# [logging.config — Logging configuration](https://docs.python.org/3/library/logging.config.html)

The [`logging.config`](https://docs.python.org/3/library/logging.config.html) module wires the logging object graph from **declarative configuration**: Python dicts (`dictConfig`), INI files (`fileConfig`), or a listening socket for live reload. Use it at application startup so libraries can log through pre-configured handlers. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/logging.config.html).

Related: [`logging`](../logging-logging-facility-for-python/index.md) core API; [`logging.handlers`](../logginghandlers-logging-handlers/index.md) for handler classes referenced in config.

---

## Configuration APIs — overview

| Function | Input | Use when |
|----------|-------|----------|
| `dictConfig(config)` | `dict` matching schema | JSON/YAML loaded in code |
| `fileConfig(fname, …)` | INI file path | Legacy deployments |
| `listen(port, …)` | TCP port | Remote reconfiguration (advanced) |
| `stopListening()` | — | Shut down config listener |

---

## dictConfig schema — [Configuration dictionary schema](https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema)

| Top-level key | Purpose |
|---------------|---------|
| `version` | Must be `1` |
| `formatters` | Named formatter specs |
| `handlers` | Named handler specs (class + kwargs) |
| `loggers` | Per-logger level, handlers, propagate |
| `root` | Root logger settings |
| `incremental` | Merge instead of replace (optional) |
| `disable_existing_loggers` | Default `True` — clears old loggers |

```python
# Goal: configure root logger from a dict
import io
import logging
import logging.config

buf = io.StringIO()
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"brief": {"format": "%(levelname)s:%(message)s"}},
        "handlers": {
            "stream": {
                "class": "logging.StreamHandler",
                "formatter": "brief",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {"level": "INFO", "handlers": ["stream"]},
    }
)
# Redirect stdout handler to our buffer for assertion
root = logging.getLogger()
root.handlers[0].stream = buf
logging.info("configured")
assert buf.getvalue().strip() == "INFO:configured"
root.handlers.clear()
```

```python
# Goal: per-module logger level in dictConfig
import logging
import logging.config

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "noisy.lib": {"level": "WARNING"},
        },
        "root": {"level": "DEBUG"},
    }
)
lib = logging.getLogger("noisy.lib")
assert lib.isEnabledFor(logging.INFO) is False
assert lib.isEnabledFor(logging.WARNING) is True
```

---

## fileConfig — [Configuration file format](https://docs.python.org/3/library/logging.config.html#configuration-file-format)

INI sections: `[loggers]`, `[handlers]`, `[formatters]`, plus per-logger/handler sections. Prefer **`dictConfig`** for new projects — easier to generate from app settings and version-control.

---

## Best practices

| Practice | Why |
|----------|-----|
| Call **`dictConfig` once** in `main()` | Libraries should not configure logging |
| Set **`disable_existing_loggers=False`** in libraries' docs | Avoid silencing third-party loggers unexpectedly |
| Validate config with a **schema** in CI | Typos in class paths fail at runtime |
| Use **`ext://`** for stream references | `ext://sys.stderr` resolves import paths safely |
| Keep secrets **out of config files** | Inject handler URLs via environment at load time |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Missing **`version: 1`** | `ValueError` from dictConfig | Always include version key |
| Wrong handler **`class`** path | ImportError at configure time | Use fully qualified names |
| **`incremental` misuse** | Partial updates surprise | Read schema for merge semantics |
| Configuring **before** imports that log | Lost early messages | Configure as first step in `main` |
| **`fileConfig` defaults** | Disables existing loggers | Match `disable_existing_loggers` needs |
