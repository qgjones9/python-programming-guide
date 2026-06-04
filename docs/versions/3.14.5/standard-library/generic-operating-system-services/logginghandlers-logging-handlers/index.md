# [logging.handlers — Logging handlers](https://docs.python.org/3/library/logging.handlers.html)

The [`logging.handlers`](https://docs.python.org/3/library/logging.handlers.html) module supplies **production handlers** beyond `StreamHandler` and `FileHandler`: size- and time-based rotation, syslog, SMTP, HTTP, and cross-thread/process queues. Reference these classes by fully qualified name in [`dictConfig`](../loggingconfig-logging-configuration/index.md). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/logging.handlers.html).

Related: [`logging`](../logging-logging-facility-for-python/index.md) base handler API; [`queue`](../../concurrent-execution/queue-a-synchronized-queue-class/index.md) used by `QueueHandler`/`QueueListener`.

---

## Handler catalog — overview

| Handler | Destination | Typical use |
|---------|-------------|-------------|
| `RotatingFileHandler` | File, size-capped | App logs with rollover at N bytes |
| `TimedRotatingFileHandler` | File, time-capped | Daily/hourly log files |
| `WatchedFileHandler` | File (Unix) | Reload when logrotate renames file |
| `SMTPHandler` | Email | Critical alerts |
| `SysLogHandler` | Unix syslog | Centralized logging |
| `HTTPHandler` | HTTP POST/GET | Remote log collectors |
| `QueueHandler` | `queue.Queue` | Non-blocking emit in hot paths |
| `QueueListener` | Drains queue to real handlers | Background writer thread |
| `MemoryHandler` | Buffer until flush level | Reduce I/O for low-priority noise |

---

## Rotating file handlers — [RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)

| Parameter | Role |
|-----------|------|
| `filename` | Log file path |
| `maxBytes` | Rollover threshold (RotatingFileHandler) |
| `backupCount` | Number of `.1`, `.2`, … backups kept |
| `when` / `interval` | Schedule for TimedRotatingFileHandler |

```python
# Goal: rotating file handler writes and rolls at size
import logging
import logging.handlers
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "app.log"
    logger = logging.getLogger("demo.rotate")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    handler = logging.handlers.RotatingFileHandler(
        path, maxBytes=50, backupCount=2, encoding="utf-8"
    )
    logger.addHandler(handler)
    logger.info("first line that is long enough to matter")
    handler.flush()
    assert path.exists()
    logger.removeHandler(handler)
    handler.close()
```

```python
# Goal: QueueHandler + QueueListener decouple emit from I/O
import io
import logging
import logging.handlers
import queue

log_queue = queue.Queue()
stream = io.StringIO()
target = logging.StreamHandler(stream)
target.setFormatter(logging.Formatter("%(message)s"))

listener = logging.handlers.QueueListener(log_queue, target)
listener.start()

qh = logging.handlers.QueueHandler(log_queue)
logger = logging.getLogger("demo.queue")
logger.handlers.clear()
logger.addHandler(qh)
logger.setLevel(logging.INFO)
logger.info("async path")
listener.stop()
assert stream.getvalue().strip() == "async path"
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Set **`encoding="utf-8"`** on file handlers | Consistent log bytes across platforms |
| Tune **`backupCount`** with disk budgets | Rotation without unbounded growth |
| Use **`QueueHandler`** in async or latency-sensitive code | Emit returns quickly |
| Match **`when='midnight'`** to UTC vs local | Document timezone for ops |
| **`close()`** handlers on shutdown | Flush buffers (especially SMTP/HTTP) |

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| **`maxBytes` too small** | Constant rotation thrashing | Size for typical burst + one record |
| Multiple processes **same file** | Interleaved garbled lines | One process per file or use QueueListener |
| **`WatchedFileHandler` on Windows** | Not available | Use TimedRotating or external shipper |
| Forgetting **`listener.start()`** | Queue fills, records lost | Start listener before logging |
| **`SMTPHandler` blocking** | Stalls request thread | QueueHandler + background listener |
