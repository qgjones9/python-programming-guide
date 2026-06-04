# [Networking and Interprocess Communication](https://docs.python.org/3/library/ipc.html)

The standard library groups **sockets**, **TLS**, **I/O multiplexing**, **signals**, **memory mapping**, and **async I/O** under **Networking and Interprocess Communication**. Some modules are **same-machine only** (`signal`, `mmap`); others support **cross-host** protocols (`socket`, `ssl`, `asyncio`). Full API reference remains on [docs.python.org](https://docs.python.org/3/library/ipc.html); this hub orients you to each module and when to reach for it.

Related sections: [`socketserver`](../internet-protocols-and-support/socketserver-a-framework-for-network-servers/index.md) for threaded/forking servers, [`threading`](../concurrent-execution/threading-thread-based-parallelism/index.md) for thread-based IPC, and [`multiprocessing`](../concurrent-execution/multiprocessing-process-based-parallelism/index.md) for process pools and shared memory.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`asyncio`](asyncio-asynchronous-io/index.md) | Coroutine-based concurrent I/O, event loop, streams, subprocesses |
| [`socket`](socket-low-level-networking-interface/index.md) | BSD sockets: TCP/UDP, addresses, blocking/non-blocking I/O |
| [`ssl`](ssl-tlsssl-wrapper-for-socket-objects/index.md) | TLS/SSL wrapping, certificates, `SSLContext` |
| [`select`](select-waiting-for-io-completion/index.md) | Low-level `select`, `poll`, `epoll`, `kqueue` primitives |
| [`selectors`](selectors-high-level-io-multiplexing/index.md) | Portable high-level multiplexing over `select` backends |
| [`signal`](signal-set-handlers-for-asynchronous-events/index.md) | Unix signal handlers, alarms, masks (main thread) |
| [`mmap`](mmap-memory-mapped-file-support/index.md) | Memory-map files or anonymous regions for shared/zero-copy access |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| High-level async TCP client/server | [`asyncio`](asyncio-asynchronous-io/index.md) streams and `asyncio.run()` |
| Custom protocol on TCP/UDP | [`socket`](socket-low-level-networking-interface/index.md) + optional [`ssl`](ssl-tlsssl-wrapper-for-socket-objects/index.md) |
| Encrypt an existing socket | [`ssl.SSLContext.wrap_socket()`](ssl-tlsssl-wrapper-for-socket-objects/index.md) |
| Wait on many fds without asyncio | [`selectors.DefaultSelector`](selectors-high-level-io-multiplexing/index.md) |
| Need exact `epoll`/`kqueue` flags | [`select`](select-waiting-for-io-completion/index.md) directly |
| Handle SIGTERM/SIGINT in a CLI daemon | [`signal`](signal-set-handlers-for-asynchronous-events/index.md) |
| Share a large read-mostly file between processes | [`mmap`](mmap-memory-mapped-file-support/index.md) with `ACCESS_READ` or `MAP_SHARED` |
| Wake a thread from another thread | [`threading`](../concurrent-execution/threading-thread-based-parallelism/index.md) primitives — not signals |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **`selectors`** over raw **`select`** | Same portability goals; cleaner register/unregister API |
| Use **`ssl.create_default_context()`** unless you need legacy cipher/protocol knobs | Defaults track modern OpenSSL security guidance |
| Set **`server_hostname`** on TLS client wraps | Enables SNI and hostname verification |
| Call **`sock.setblocking(False)`** before registering with a selector | Blocking sockets stall the whole event loop |
| Unregister fds **before** `close()` | Avoids `KeyError` / undefined behavior in multiplexers |
| Install signal handlers only in the **main thread** | `signal.signal()` raises `ValueError` elsewhere |
| **`flush()`** buffered files before **`mmap`** on writable mappings | Kernel mapping may not see stdio buffer contents |
| Avoid locks inside signal handlers | Documented deadlock risk with `threading.Lock` |

```python
# Goal: pick the default multiplexer for the platform
import selectors

sel = selectors.DefaultSelector()
assert hasattr(sel, "register") and hasattr(sel, "select")
sel.close()
```

```python
# Goal: loopback TCP socket pair without network I/O
import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("127.0.0.1", 0))
listener.listen(1)
host, port = listener.getsockname()
client = socket.create_connection((host, port))
server, _ = listener.accept()
client.sendall(b"ping")
assert server.recv(4) == b"ping"
client.close()
server.close()
listener.close()
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Using `select` on regular files (Unix) | Always “ready”; no growth detection | Use polling/stat or async patterns for files |
| `select` on Windows with non-socket fds | Unsupported / unreliable | Sockets only on Windows |
| Forgetting `SO_REUSEADDR` on server restart | `EADDRINUSE` after quick restart | Set option before `bind()` |
| TLS with default context but no CA bundle | Verification failures on custom CAs | `load_verify_locations()` or system CAs |
| Long C extension holds GIL during compute | Signal handlers delayed | Keep CPU work in Python chunks or threads |
| In-place `mmap` slice assignment wrong size | `ValueError` | Match replacement byte length |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [asyncio — Asynchronous I/O](asyncio-asynchronous-io/index.md) | Event loop, coroutines, tasks, streams |
| [socket — Low-level networking interface](socket-low-level-networking-interface/index.md) | Addresses, socket objects, timeouts |
| [ssl — TLS/SSL wrapper for socket objects](ssl-tlsssl-wrapper-for-socket-objects/index.md) | `SSLContext`, verification, wrapping |
| [select — Waiting for I/O completion](select-waiting-for-io-completion/index.md) | `select`, `poll`, `epoll`, `kqueue` |
| [selectors — High-level I/O multiplexing](selectors-high-level-io-multiplexing/index.md) | `DefaultSelector`, `SelectorKey` |
| [signal — Set handlers for asynchronous events](signal-set-handlers-for-asynchronous-events/index.md) | Handlers, alarms, masks |
| [mmap — Memory-mapped file support](mmap-memory-mapped-file-support/index.md) | File and anonymous mappings |
