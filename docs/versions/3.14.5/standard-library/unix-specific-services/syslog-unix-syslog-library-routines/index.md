# [syslog — Unix syslog library routines](https://docs.python.org/3/library/syslog.html)

The [`syslog`](https://docs.python.org/3/library/syslog.html) module sends messages to the **Unix syslog** facility (`syslogd`, `journald` on Linux). It wraps `openlog`, `syslog`, and `closelog` with Pythonic helpers and priority constants. Unix-only. Full option flags remain on [docs.python.org](https://docs.python.org/3/library/syslog.html).

Related: [`logging`](../../generic-operating-system-services/logging-logging-facility-for-python/index.md) with `SysLogHandler`; [`os`](../../generic-operating-system-services/os-miscellaneous-operating-system-interfaces/index.md).

---

## Core functions — [Examples](https://docs.python.org/3/library/syslog.html#examples)

| Function | Role |
|----------|------|
| `syslog.openlog(ident, logoption, facility)` | Configure identity and default facility |
| `syslog.syslog(priority, message)` | Send one message |
| `syslog.closelog()` | Close logger connection |
| `syslog.LOG_PID`, `LOG_CONS`, … | `openlog` options |
| `syslog.LOG_USER`, `LOG_DAEMON`, … | Facility codes |
| `syslog.LOG_INFO`, `LOG_ERR`, … | Priority levels |

```python
# Goal: openlog/syslog/closelog cycle (Unix)
import importlib.util

if importlib.util.find_spec("syslog"):
    import syslog

    syslog.openlog("python-demo", syslog.LOG_PID, syslog.LOG_USER)
    syslog.syslog(syslog.LOG_INFO, "demo message")
    syslog.closelog()
    assert syslog.LOG_INFO != syslog.LOG_ERR
else:
    import sys

    assert sys.platform == "win32"
```

---

## Priority ordering

Lower numeric value = higher urgency for some constants; use named **`LOG_*`** levels rather than memorizing numbers.

| Level | Typical use |
|-------|-------------|
| `LOG_DEBUG` | Verbose diagnostics |
| `LOG_INFO` | Normal operations |
| `LOG_WARNING` | Recoverable issues |
| `LOG_ERR` | Errors |
| `LOG_CRIT` / `LOG_ALERT` / `LOG_EMERG` | Severe / immediate action |

```python
# Goal: syslog.syslog accepts priority-or-message overload (Unix)
import importlib.util

if importlib.util.find_spec("syslog"):
    import syslog

    syslog.openlog("demo")
    syslog.syslog("message with default priority")
    syslog.syslog(syslog.LOG_WARNING, "explicit priority")
    syslog.closelog()
```

---

## Integration with `logging`

For applications, prefer **`logging.handlers.SysLogHandler`**—it formats records and maps levels to syslog priorities while keeping local file handlers.

---

## Best practices

| Practice | Why |
|----------|-----|
| Call **`openlog` once** at startup | Sets consistent `ident` in `/var/log` |
| Include **PID** via `LOG_PID` | Disambiguate multi-process services |
| Avoid sensitive data in messages | Syslog is often world-readable |
| Guard imports on **Windows CI** | Module absent |

---

## See also

- [`logging.handlers.SysLogHandler`](../../generic-operating-system-services/logging-logging-facility-for-python/index.md) — stdlib logging bridge
- [`resource`](../resource-resource-usage-information/index.md) — process metrics
