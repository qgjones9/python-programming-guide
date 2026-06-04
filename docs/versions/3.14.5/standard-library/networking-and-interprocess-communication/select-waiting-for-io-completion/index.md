# [select — Waiting for I/O completion](https://docs.python.org/3/library/select.html)

The [`select`](https://docs.python.org/3/library/select.html) module wraps OS **I/O multiplexing** primitives: `select()`, `poll()`, `epoll()`, `devpoll()`, and `kqueue()`. On **Windows**, only **sockets** are supported for `select()`. Prefer [`selectors`](../selectors-high-level-io-multiplexing/index.md) for portable application code unless you need exact kernel flags. **Not available on WASI.**

---

## select() — [select.select](https://docs.python.org/3/library/select.html#select.select)

Waits on three fd sets until at least one is ready or timeout elapses.

| Iterable | Waits for |
|----------|-----------|
| `rlist` | Readable |
| `wlist` | Writable |
| `xlist` | “Exceptional” (platform-defined; often OOB) |

Returns `(ready_r, ready_w, ready_x)` subsets of the arguments.

```python
# Goal: detect readable data on a socket pair
import select
import socket

rsock, wsock = socket.socketpair()
wsock.send(b"x")
ready, _, _ = select.select([rsock], [], [], 1.0)
assert rsock in ready
data = rsock.recv(1)
assert data == b"x"
rsock.close()
wsock.close()
```

```python
# Goal: zero timeout polls without blocking
import os
import select

r, w = os.pipe()
os.write(w, b"1")
ready, _, _ = select.select([r], [], [], 0)
assert r in ready
os.close(r)
os.close(w)
```

---

## poll() — [Polling objects](https://docs.python.org/3/library/select.html#polling-objects)

`poll()` scales with the **number of registered fds**, not the maximum fd value.

| Constant | Meaning |
|----------|---------|
| `POLLIN` | Data to read |
| `POLLOUT` | Ready for write |
| `POLLPRI` | Urgent data |
| `POLLERR` / `POLLHUP` | Error / hang-up |

```python
# Goal: register and poll a pipe fd
import os
import select

poller = select.poll()
r, w = os.pipe()
poller.register(r, select.POLLIN)
os.write(w, b"z")
events = poller.poll(1000)
assert (r, select.POLLIN) in events
os.close(r)
os.close(w)
```

---

## epoll() — [Edge and level trigger polling](https://docs.python.org/3/library/select.html#edge-and-level-trigger-polling-epoll-objects)

Linux **epoll** supports edge-trigger (`EPOLLET`) and one-shot (`EPOLLONESHOT`) modes.

```python
# Goal: epoll register/poll when available (Linux)
import os
import select

if hasattr(select, "epoll"):
    ep = select.epoll()
    r, w = os.pipe()
    ep.register(r, select.EPOLLIN)
    os.write(w, b"e")
    ready = ep.poll(1.0)
    assert any(fd == r and ev & select.EPOLLIN for fd, ev in ready)
    ep.unregister(r)
    ep.close()
    os.close(r)
    os.close(w)
```

---

## Platform notes

| API | Availability |
|-----|--------------|
| `select.select` | Unix sockets+files; Windows sockets only |
| `poll` | Most Unix |
| `epoll` | Linux ≥ 2.5.44 |
| `kqueue` / `kevent` | BSD, macOS |
| `devpoll` | Solaris derivatives |

`select.PIPE_BUF` is the minimum guaranteed atomic pipe write size (≥ 512 per POSIX).

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`selectors`** in application code | Same backends, safer register/unregister |
| Retry or handle **EINTR** via PEP 475 behavior | Timeouts recomputed after signals (3.5+) |
| Do not use `select` on **regular files** for growth detection | Files always appear ready on Unix |
| Close polling objects (`epoll.close()`, context managers) | Frees kernel control fds |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Re-registering same fd on `devpoll` | Undefined — `modify` or unregister first |
| Large `rlist` with high max fd | O(n) scan — use `poll`/`epoll` |
| Empty three-list `select` on Windows | Platform-dependent; avoid |

---

## See also

- [`selectors`](../selectors-high-level-io-multiplexing/index.md) — recommended high-level API
