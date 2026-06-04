# [xmlrpc — XMLRPC server and client modules](https://docs.python.org/3/library/xmlrpc.html)

The [`xmlrpc`](https://docs.python.org/3/library/xmlrpc.html) package exposes **XML-RPC** client and server modules for remote procedure calls over HTTP with XML payloads. It is legacy but still embedded in some tools. Submodules: [`xmlrpc.client`](../xmlrpcclient-xml-rpc-client-access/index.md), [`xmlrpc.server`](../xmlrpcserver-basic-xml-rpc-servers/index.md). Overview: [docs.python.org](https://docs.python.org/3/library/xmlrpc.html).

---

## Package layout

| Submodule | Role |
|-----------|------|
| `xmlrpc.client` | `ServerProxy`, `Binary`, `Fault`, transport hooks |
| `xmlrpc.server` | `SimpleXMLRPCServer`, `CGIXMLRPCRequestHandler` |

Import as `import xmlrpc.client`, not `import xmlrpc`.

---

## Example — local client/server round-trip

```python
# Goal: register RPC function and call via ServerProxy on ephemeral port
import threading
import xmlrpc.client
import xmlrpc.server


def add(a, b):
    return a + b


server = xmlrpc.server.SimpleXMLRPCServer(("127.0.0.1", 0), logRequests=False)
server.register_function(add, "add")
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

proxy = xmlrpc.client.ServerProxy(f"http://127.0.0.1:{port}", allow_none=True)
assert proxy.add(2, 3) == 5
server.shutdown()
```

---

## Security

XML-RPC parses XML from the network—**disable for untrusted peers** or place behind authentication. Prefer modern RPC (gRPC, REST+JSON) for new systems.

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [xmlrpc.client — XML-RPC client access](../xmlrpcclient-xml-rpc-client-access/index.md) | Proxy objects and transports |
| [xmlrpc.server — Basic XML-RPC servers](../xmlrpcserver-basic-xml-rpc-servers/index.md) | Publish callables over HTTP |
