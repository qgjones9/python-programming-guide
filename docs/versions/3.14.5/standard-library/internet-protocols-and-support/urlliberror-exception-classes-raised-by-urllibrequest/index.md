# [urllib.error — Exception classes raised by urllib.request](https://docs.python.org/3/library/urllib.error.html)

[`urllib.error`](https://docs.python.org/3/library/urllib.error.html) defines exceptions raised by [`urllib.request`](../urllibrequest-extensible-library-for-opening-urls/index.md) when transport or HTTP-level failures occur. Distinguish **connection errors** from **HTTP error status codes**. Reference: [urllib.error](https://docs.python.org/3/library/urllib.error.html).

---

## Exception types

| Class | When raised |
|-------|-------------|
| `URLError` | Network failure, timeout, unknown host (`.reason` often wraps `OSError`) |
| `HTTPError` | Subclass of `URLError`; response returned for 4xx/5xx when default handler runs (`.code`, `.headers`, file-like body) |

`HTTPError` is also a valid response object—you can read the error body from the server.

---

## Example — catch HTTPError and read code

```python
# Goal: demonstrate HTTPError attributes using a local minimal server
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.error


class NotFoundHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"missing")

    def log_message(self, format, *args):
        pass


server = HTTPServer(("127.0.0.1", 0), NotFoundHandler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

try:
    urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2)
except urllib.error.HTTPError as exc:
    assert exc.code == 404
    assert exc.read() == b"missing"
finally:
    server.shutdown()
```

---

## Handling pattern

Catch `HTTPError` when you need status-specific logic; catch `URLError` for broader connectivity issues. Always set timeouts on `urlopen`.
