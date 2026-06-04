# [xmlrpc.server — Basic XML-RPC servers](https://docs.python.org/3/library/xmlrpc.server.html)

[`xmlrpc.server`](https://docs.python.org/3/library/xmlrpc.server.html) publishes Python callables over **HTTP XML-RPC** using `SimpleXMLRPCServer`, `CGIXMLRPCRequestHandler`, and multicall helpers. Suitable for admin tools and tests—not hardened for hostile networks. Reference: [xmlrpc.server](https://docs.python.org/3/library/xmlrpc.server.html).

---

## SimpleXMLRPCServer

| Method | Role |
|--------|------|
| `register_function(callable, name=None)` | Expose function (default name: `__name__`) |
| `register_instance(obj)` | Expose `_methodName` public methods |
| `register_introspection_functions()` | `system.listMethods`, etc. |
| `serve_forever()` / `handle_request()` | Process loop |

Bind to **`127.0.0.1`** during development.

---

## Example — register and dispatch locally

```python
# Goal: register multiply and invoke through server dispatch path
import xmlrpc.server


def multiply(a, b):
    return a * b


server = xmlrpc.server.SimpleXMLRPCServer(("127.0.0.1", 0), logRequests=False)
server.register_function(multiply)
method = server._dispatch("multiply", (3, 4))
assert method == 12
server.server_close()
```

---

## CGI handler

`CGIXMLRPCRequestHandler` serves RPC from CGI environments—legacy deployment pattern; prefer WSGI/ASGI stacks for new web apps.

---

## Security

| Risk | Mitigation |
|------|------------|
| Arbitrary code exposure | Register only intended functions; disable introspection in production |
| XML bombs | Do not expose to untrusted clients without limits |

Pair with [`xmlrpc.client`](../xmlrpcclient-xml-rpc-client-access/index.md) for integration tests on localhost.
