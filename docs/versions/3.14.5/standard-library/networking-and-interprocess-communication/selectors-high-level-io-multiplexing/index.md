# [selectors — High-level I/O multiplexing](https://docs.python.org/3/library/selectors.html)

[`selectors`](https://docs.python.org/3/library/selectors.html) (added in 3.4) provides **`BaseSelector`** and concrete backends (`EpollSelector`, `PollSelector`, …) built on [`select`](../select-waiting-for-io-completion/index.md). **`DefaultSelector`** picks the fastest implementation for the current OS. **Not available on WASI.**

---

## Core types — [Classes](https://docs.python.org/3/library/selectors.html#classes)

| Symbol | Role |
|--------|------|
| `DefaultSelector` | Alias to best backend (`EpollSelector` on Linux, etc.) |
| `SelectorKey` | `namedtuple`: `fileobj`, `fd`, `events`, `data` |
| `EVENT_READ` / `EVENT_WRITE` | Bit masks for registration |
| `BaseSelector.register` | Monitor a file object |
| `BaseSelector.select(timeout)` | Returns `[(key, events), ...]` |

```python
# Goal: register a socketpair and read when ready
import selectors
import socket

sel = selectors.DefaultSelector()
rsock, wsock = socket.socketpair()
key = sel.register(rsock, selectors.EVENT_READ, data=b"buf")
wsock.send(b"1")
events = sel.select(timeout=1.0)
assert len(events) == 1
k, mask = events[0]
assert k.fileobj is rsock and mask & selectors.EVENT_READ
assert rsock.recv(1) == b"1"
sel.unregister(rsock)
sel.close()
rsock.close()
wsock.close()
```

```python
# Goal: modify watched events on an existing registration
import os
import selectors

sel = selectors.DefaultSelector()
r, w = os.pipe()
key = sel.register(r, selectors.EVENT_READ)
sel.modify(r, selectors.EVENT_READ | selectors.EVENT_WRITE, data="pipe")
assert key.fd == r
sel.unregister(r)
sel.close()
os.close(r)
os.close(w)
```

---

## Selector hierarchy

```
BaseSelector
├── SelectSelector
├── PollSelector
├── EpollSelector
├── DevpollSelector
└── KqueueSelector
```

Instantiate a specific class only when you must reproduce behavior on a given backend; otherwise use `DefaultSelector`.

---

## Callback pattern — [Examples](https://docs.python.org/3/library/selectors.html#examples)

Attach callables via `data=` and dispatch after `select()` (official docs show an echo server loop).

```python
# Goal: dispatch via key.data callback without a forever loop
import selectors
import socket

def on_read(sock, mask):
    return sock.recv(16)

sel = selectors.DefaultSelector()
a, b = socket.socketpair()
sel.register(a, selectors.EVENT_READ, on_read)
b.send(b"ping")
for key, mask in sel.select(0.5):
    chunk = key.data(key.fileobj, mask)
    assert chunk == b"ping"
sel.close()
a.close()
b.close()
```

---

## Best practices

| Practice | Why |
|----------|-----|
| **`unregister` before `close`** | Prevents `KeyError` and fd reuse bugs |
| Use **`modify`** instead of unregister+register | More efficient on epoll/kqueue |
| Set sockets **non-blocking** when using callbacks | Avoid blocking entire `select` |
| Treat **empty `select` result** after signal as normal | PEP 475 may restart with new timeout |
| Use context manager: `with DefaultSelector() as sel:` | Ensures `close()` |

---

## Common pitfalls

| Pitfall | Mitigation |
|---------|------------|
| Registering same `fileobj` twice | Raises `KeyError` |
| Windows: registering pipes | Use sockets only on Windows |
| Storing mutable state only in closure | Prefer `key.data` for per-connection state |

---

## See also

- [`select`](../select-waiting-for-io-completion/index.md) — low-level primitives and constants
