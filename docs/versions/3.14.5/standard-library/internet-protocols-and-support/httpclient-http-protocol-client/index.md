# [http.client — HTTP protocol client](https://docs.python.org/3/library/http.client.html)

[`http.client`](https://docs.python.org/3/library/http.client.html) implements a **low-level HTTP/1.1 client** on top of sockets: `HTTPConnection`, `HTTPSConnection`, request/response objects, and constants. Higher-level fetching usually goes through [`urllib.request`](../urllibrequest-extensible-library-for-opening-urls/index.md). Reference: [http.client](https://docs.python.org/3/library/http.client.html).

---

## Typical flow

| Step | API |
|------|-----|
| Connect | `conn = HTTPConnection("host", port, timeout=...)` |
| Request | `conn.request("GET", "/path", headers={...})` |
| Response | `resp = conn.getresponse()` → `status`, `reason`, `read()` |
| Close | `conn.close()` |

Use `HTTPSConnection` for TLS (with optional `context=`).

---

## Example — parse a response from bytes (offline)

```python
# Goal: feed raw HTTP bytes into HTTPResponse without a live socket
from io import BytesIO
import http.client

raw = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nhello"


class FakeSocket:
    def __init__(self, data):
        self._data = data

    def makefile(self, mode, bufsize=-1):
        return BytesIO(self._data)


resp = http.client.HTTPResponse(FakeSocket(raw))
resp.begin()
assert resp.status == 200
assert resp.getheader("Content-Type") == "text/plain"
assert resp.read() == b"hello"
```

---

## Constants

`http.client.OK`, `NOT_FOUND`, `MOVED_PERMANENTLY`, etc. mirror numeric codes; prefer [`http.HTTPStatus`](../http-http-modules/index.md) in new code.

---

## Best practices

| Practice | Why |
|----------|-----|
| Always set **timeouts** | Avoid hung connections |
| Reuse connections with care | HTTP/1.1 keep-alive requires reading entire body before next request |
| Prefer urllib/httpx for simple GETs | Less boilerplate than manual `HTTPConnection` |
