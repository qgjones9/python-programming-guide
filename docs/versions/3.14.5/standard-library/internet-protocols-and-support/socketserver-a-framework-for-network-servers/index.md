# [socketserver — A framework for network servers](https://docs.python.org/3/library/socketserver.html)

[`socketserver`](https://docs.python.org/3/library/socketserver.html) factors **TCP/UDP server boilerplate**: bind, listen, accept, and dispatch each connection to a `BaseRequestHandler` subclass. [`http.server`](../httpserver-http-servers/index.md) builds on these classes. Reference: [socketserver](https://docs.python.org/3/library/socketserver.html).

---

## Server classes

| Class | Socket type |
|-------|-------------|
| `TCPServer` | Stream (connection-oriented) |
| `UDPServer` | Datagram |
| `ThreadingTCPServer` | TCP with per-client threads |
| `ForkingTCPServer` | TCP with forked child (Unix) |

Set `allow_reuse_address = True` on the class for quick dev restarts.

---

## Handler pattern

Subclass `BaseRequestHandler` and implement `handle(self)` with `self.request` (socket or bytes) and `self.client_address`.

---

## Example — one-shot TCP echo server

```python
# Goal: ThreadingTCPServer echo one request then shut down
import socketserver
import threading


class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        self.request.sendall(data)


server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), EchoHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

import socket

with socket.create_connection(("127.0.0.1", port), timeout=2) as sock:
    sock.sendall(b"ping")
    assert sock.recv(1024) == b"ping"

server.shutdown()
server.server_close()
```

---

## Mix-in variants

`ThreadingMixIn` and `ForkingMixIn` combine with `TCPServer`/`UDPServer` for concurrent clients; watch resource limits under load.
