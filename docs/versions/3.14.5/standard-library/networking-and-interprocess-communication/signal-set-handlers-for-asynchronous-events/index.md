# [signal — Set handlers for asynchronous events](https://docs.python.org/3/library/signal.html)

The [`signal`](https://docs.python.org/3/library/signal.html) module installs **Unix signal handlers** and exposes constants for `SIG*`, masks, and alarms. Handlers run in the **main thread** at interpreter checkpoints—not inside the C signal handler. Behavior differs on **WebAssembly** emulated platforms.

Related: [`asyncio` event loop signal APIs](../asyncio-asynchronous-io/index.md), [`threading`](../concurrent-execution/thread-based-parallelism/index.md) for inter-thread wakeups.

---

## General rules — [General rules](https://docs.python.org/3/library/signal.html#general-rules)

| Rule | Implication |
|------|-------------|
| Handlers persist until reset | BSD-style semantics emulated on all platforms |
| `SIGINT` default | Becomes `KeyboardInterrupt` unless parent changed handler |
| `SIGPIPE` default | Ignored so broken pipes raise `BrokenPipeError` in Python |
| Not for thread IPC | Use `threading.Event` / `Queue` instead |
| No locks in handlers | Risk of deadlock documented |

---

## signal() — [signal.signal](https://docs.python.org/3/library/signal.html#signal.signal)

```python
# Goal: read default SIGINT handler and valid signal set
import signal

handler = signal.getsignal(signal.SIGINT)
assert handler in (signal.SIG_DFL, signal.SIG_IGN) or callable(handler)
assert signal.SIGINT in signal.valid_signals()
```

```python
# Goal: temporarily ignore SIGUSR1 when available
import signal

if hasattr(signal, "SIGUSR1"):
    old = signal.signal(signal.SIGUSR1, signal.SIG_IGN)
    assert signal.getsignal(signal.SIGUSR1) == signal.SIG_IGN
    signal.signal(signal.SIGUSR1, old)
```

---

## Enums — [Module contents](https://docs.python.org/3/library/signal.html#module-contents)

Since 3.5, `Signals`, `Handlers`, and `Sigmasks` are `IntEnum` collections; `getsignal()` may return `Signals` members.

| Enum | Members |
|------|---------|
| `Handlers` | `SIG_DFL`, `SIG_IGN` |
| `Sigmasks` | `SIG_BLOCK`, `SIG_UNBLOCK`, `SIG_SETMASK` |
| `Signals` | `SIGINT`, `SIGTERM`, `SIGCHLD`, … (platform-dependent) |

```python
# Goal: compare SIG_DFL with Handlers enum
import signal

assert signal.SIG_DFL == signal.Handlers.SIG_DFL
assert signal.SIG_IGN == signal.Handlers.SIG_IGN
```

---

## alarm() — [signal.alarm](https://docs.python.org/3/library/signal.html#signal.alarm)

Schedule `SIGALRM` once after `seconds` (Unix). Returns time remaining on previous alarm.

```python
# Goal: alarm API returns int remainder on Unix
import signal
import sys

if hasattr(signal, "alarm"):
    remaining = signal.alarm(0)  # cancel any pending alarm
    assert isinstance(remaining, int)
```

---

## pause() and sigwait — [signal.pause](https://docs.python.org/3/library/signal.html#signal.pause)

`pause()` blocks until a signal arrives; `sigwait()` waits synchronously on a signal set (pthread).

---

## pthread masks — [pthread_sigmask](https://docs.python.org/3/library/signal.html#signal.pthread_sigmask)

Block or unblock signals in the **calling thread** without affecting other threads.

```python
# Goal: block and unblock SIGUSR2 in main thread when supported
import signal

if hasattr(signal, "pthread_sigmask") and hasattr(signal, "SIGUSR2"):
    signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR2])
    pending = signal.sigpending()
    assert isinstance(pending, set)
    signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGUSR2])
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Keep handlers **minimal** | Defer work to main loop; set a flag or write to `os.pipe` |
| Only register from **main thread** | Otherwise `ValueError` |
| Use **`signal.set_wakeup_fd`** with selectors | Integrate signals into event loop safely |
| Avoid catching **`SIGFPE`/`SIGSEGV`** in Python | Re-raises; use `faulthandler` for sync faults |
| Document **SIGCHLD** semantics | Platform-specific persistence vs other signals |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Long pure-C computation | Handler delayed until C returns |
| Raising in handler | Exception appears in main thread arbitrarily |
| Using signals between threads | Use threading primitives |
| `alarm` in multi-threaded code | Alarm is process-wide; easy to confuse |

---

## See also

- [`faulthandler`](../../debugging-and-profiling/faulthandler-dump-the-python-traceback/index.md) — synchronous fault dumps
