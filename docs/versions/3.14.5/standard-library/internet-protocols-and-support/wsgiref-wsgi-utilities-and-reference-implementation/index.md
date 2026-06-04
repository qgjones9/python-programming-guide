# [wsgiref — WSGI Utilities and Reference Implementation](https://docs.python.org/3/library/wsgiref.html)

[`wsgiref`](https://docs.python.org/3/library/wsgiref.html) implements **PEP 3333 WSGI** helpers: validate apps, build environ dicts, manipulate headers, and run a tiny reference HTTP server. Frameworks (Flask, Django WSGI) replace most of this in production. Reference: [wsgiref package](https://docs.python.org/3/library/wsgiref.html).

---

## Submodules

| Submodule | Role |
|-----------|------|
| `wsgiref.util` | `request_uri`, `application_uri`, `shift_path_info`, … |
| `wsgiref.headers` | `Headers` mapping for response headers |
| `wsgiref.simple_server` | `make_server`, `WSGIRequestHandler` |
| `wsgiref.validate` | Middleware checking WSGI compliance |
| `wsgiref.handlers` | Base server/gateway classes |

---

## Example — call a WSGI app with a synthetic environ

```python
# Goal: invoke a WSGI callable and collect response status/headers/body
from io import BytesIO
from wsgiref.util import setup_testing_defaults


def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"hello"]


environ = {}
setup_testing_defaults(environ)
environ["PATH_INFO"] = "/"
environ["REQUEST_METHOD"] = "GET"

captured = {}

def start(status, headers, exc_info=None):
    captured["status"] = status
    captured["headers"] = headers

body = b"".join(app(environ, start))
assert captured["status"] == "200 OK"
assert body == b"hello"
```

---

## Testing tip

Combine `wsgiref.validate.validator` middleware during development to catch incorrect status/header/body iterator usage early.
