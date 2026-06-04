# [http.cookiejar — Cookie handling for HTTP clients](https://docs.python.org/3/library/http.cookiejar.html)

[`http.cookiejar`](https://docs.python.org/3/library/http.cookiejar.html) stores **HTTP cookies** for clients: accept `Set-Cookie` responses, match requests by domain/path, enforce expiry, and optional policy hooks. Integrates with [`urllib.request`](../urllibrequest-extensible-library-for-opening-urls/index.md) via `HTTPCookieProcessor`. Reference: [http.cookiejar](https://docs.python.org/3/library/http.cookiejar.html).

---

## Jar implementations

| Class | Storage |
|-------|---------|
| `CookieJar` | In-memory |
| `FileCookieJar` | Abstract base for persistence |
| `LWPCookieJar` / `MozillaCookieJar` | Save/load cookie files |

---

## Example — manual cookie round-trip

```python
# Goal: add a cookie to CookieJar and serialize Cookie header
import http.cookiejar
import urllib.request

jar = http.cookiejar.CookieJar()
cookie = http.cookiejar.Cookie(
    version=0,
    name="id",
    value="42",
    port=None,
    port_specified=False,
    domain="example.com",
    domain_specified=True,
    domain_initial_dot=False,
    path="/",
    path_specified=True,
    secure=False,
    expires=None,
    discard=True,
    comment=None,
    comment_url=None,
    rest={},
    rfc2109=False,
)
jar.set_cookie(cookie)

request = urllib.request.Request("http://example.com/page")
jar.add_cookie_header(request)
assert request.get_header("Cookie") == "id=42"
```

---

## Policy

Subclass `CookiePolicy` to block third-party cookies or non-HTTPS cookies. Default policy accepts most cookies suitable for tooling and tests.
