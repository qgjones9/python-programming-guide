# [urllib.request — Extensible library for opening URLs](https://docs.python.org/3/library/urllib.request.html)

[`urllib.request`](https://docs.python.org/3/library/urllib.request.html) opens **URLs and `data:`/`file:` resources** through a pipeline of handlers (`HTTPHandler`, `HTTPCookieProcessor`, …) managed by `OpenerDirector`. High-level entry: `urlopen(url, data=None, timeout=...)`. Reference: [urllib.request](https://docs.python.org/3/library/urllib.request.html).

---

## Key types and functions

| Symbol | Role |
|--------|------|
| `urlopen(url, ...)` | Return file-like response object |
| `Request(url, data, headers, method=...)` | Mutable request before open |
| `build_opener(*handlers)` | Custom handler chain |
| `HTTPRedirectHandler`, `ProxyHandler` | Pluggable behavior |
| `install_opener(opener)` | Set global default opener |

Responses are [`addinfourl`](../urllibresponse-response-classes-used-by-urllib/index.md) objects with `.read()`, `.status`, and headers.

---

## Example — POST form data with Request

```python
# Goal: POST urlencoded body using in-memory response via data URL follow-up
import urllib.request
import urllib.parse

# Safe offline read via data URL
with urllib.request.urlopen("data:text/plain,ok") as resp:
    body = resp.read()
    assert body == b"ok"

encoded = urllib.parse.urlencode({"name": "Ada"}).encode()
req = urllib.request.Request(
    "data:text/plain,ignored",
    data=encoded,
    method="POST",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
assert req.data == b"name=Ada"
```

---

## Timeouts and errors

Always pass **`timeout=`** for network URLs. Failures raise [`urllib.error.URLError`](../urlliberror-exception-classes-raised-by-urllibrequest/index.md) or `HTTPError` (subclass with `.code`).

---

## Security

Do not pass user-controlled URLs directly to `urlopen` without SSRF checks (block loopback, metadata endpoints, `file:` if unintended).
