# [http.server — HTTP servers](https://docs.python.org/3/library/http.server.html)

[`http.server`](https://docs.python.org/3/library/http.server.html) provides **`HTTPServer`** and **`BaseHTTPRequestHandler`** for quick static file or diagnostic HTTP services—ideal for local development, not production. Built on [`socketserver`](../socketserver-a-framework-for-network-servers/index.md). Reference: [http.server](https://docs.python.org/3/library/http.server.html).

---

## Key classes

| Class | Role |
|-------|------|
| `HTTPServer` | TCP server binding address and port |
| `BaseHTTPRequestHandler` | Subclass `do_GET`, `do_POST`, … |
| `SimpleHTTPRequestHandler` | Serve files from a directory |
| `ThreadingHTTPServer` | Handle clients in threads |

---

## Example — handler logic without leaving server running

```python
# Goal: serve a file with SimpleHTTPRequestHandler on localhost
import http.server
import os
import tempfile
import threading
import urllib.request


with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "note.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("ok")
    cwd = os.getcwd()
    os.chdir(tmp)
    try:
        server = http.server.HTTPServer(("127.0.0.1", 0), http.server.SimpleHTTPRequestHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/note.txt", timeout=2) as resp:
            assert resp.read() == b"ok"
        server.shutdown()
    finally:
        os.chdir(cwd)
```

---

## Security — [Security considerations](https://docs.python.org/3/library/http.server.html#security-considerations)

Never expose `SimpleHTTPRequestHandler` to untrusted networks: path traversal and arbitrary file read risks. Bind **`127.0.0.1`** only for local tools.

---

## CLI

`python -m http.server 8000` serves the current directory; see [Command-line interface](https://docs.python.org/3/library/http.server.html#command-line-interface).
