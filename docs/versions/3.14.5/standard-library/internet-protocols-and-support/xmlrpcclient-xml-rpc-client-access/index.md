# [xmlrpc.client — XML-RPC client access](https://docs.python.org/3/library/xmlrpc.client.html)

[`xmlrpc.client`](https://docs.python.org/3/library/xmlrpc.client.html) marshals Python objects to **XML-RPC requests** and unmarshals responses via `ServerProxy` (attribute-style RPC), `Binary`, `Fault`, and pluggable `Transport`. Reference: [xmlrpc.client](https://docs.python.org/3/library/xmlrpc.client.html).

---

## ServerProxy usage

| Topic | Detail |
|-------|--------|
| Construction | `ServerProxy(uri, transport=None, encoding='utf-8', allow_none=False)` |
| Calls | `proxy.method(arg1, arg2)` → HTTP POST with XML body |
| Faults | Server errors raise `Fault` with `.faultCode` and `.faultString` |
| Types | Supports int, float, bool, str, bytes (`Binary`), lists, structs (dict) |

Use `allow_none=True` only when the server accepts nil elements.

---

## Example — in-process server call

```python
# Goal: ServerProxy invokes registered function on local XML-RPC server
import threading
import xmlrpc.client
import xmlrpc.server


server = xmlrpc.server.SimpleXMLRPCServer(("127.0.0.1", 0), logRequests=False)
server.register_function(pow)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

proxy = xmlrpc.client.ServerProxy(f"http://127.0.0.1:{port}")
assert proxy.pow(2, 8) == 256
server.shutdown()
```

---

## Transport and HTTPS

Provide a custom `Transport` or `SafeTransport` subclass for certificates, proxies, or timeouts. Default `ServerProxy` uses HTTP unless given an `https://` URI with valid TLS setup.

---

## See also

- [`xmlrpc.server`](../xmlrpcserver-basic-xml-rpc-servers/index.md) for serving methods
