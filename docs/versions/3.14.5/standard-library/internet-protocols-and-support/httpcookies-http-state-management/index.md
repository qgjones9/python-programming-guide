# [http.cookies — HTTP state management](https://docs.python.org/3/library/http.cookies.html)

[`http.cookies`](https://docs.python.org/3/library/http.cookies.html) parses and serializes **HTTP cookie headers** on the server side using `SimpleCookie` and `Morsel` objects. Client-side storage and policy live in [`http.cookiejar`](../httpcookiejar-cookie-handling-for-http-clients/index.md). Reference: [http.cookies](https://docs.python.org/3/library/http.cookies.html).

---

## Core types

| Type | Role |
|------|------|
| `SimpleCookie` | Dict-like mapping of cookie name → `Morsel` |
| `Morsel` | Single cookie with `value`, `domain`, `path`, `expires`, flags |
| `CookieError` | Invalid cookie syntax |

Load from header string with `SimpleCookie.load()`; emit with `output()` or `js_output()` (deprecated pattern for JS).

---

## Example — set and serialize cookies

```python
# Goal: build Set-Cookie header values with SimpleCookie
from http.cookies import SimpleCookie

jar = SimpleCookie()
jar["session"] = "abc123"
jar["session"]["path"] = "/"
jar["session"]["httponly"] = True

header = jar.output(header="", sep="\n").strip()
assert "session=abc123" in header
assert "Path=/" in header
assert "HttpOnly" in header

loaded = SimpleCookie()
loaded.load("session=xyz; Path=/app")
assert loaded["session"].value == "xyz"
assert loaded["session"]["path"] == "/app"
```

---

## Security notes

| Flag | Purpose |
|------|---------|
| `HttpOnly` | Reduce XSS cookie theft |
| `Secure` | Send only over HTTPS |
| `SameSite` | CSRF mitigation (`Strict`, `Lax`, `None`) |

Always validate cookie values from untrusted clients.
