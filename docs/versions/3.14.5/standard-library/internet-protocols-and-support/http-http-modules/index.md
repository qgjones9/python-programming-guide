# [http — HTTP modules](https://docs.python.org/3/library/http.html)

The [`http`](https://docs.python.org/3/library/http.html) package centralizes **HTTP constants**: status codes (`HTTPStatus`), methods, and shared definitions used by [`http.client`](../httpclient-http-protocol-client/index.md), [`http.server`](../httpserver-http-servers/index.md), and [`http.cookies`](../httpcookies-http-state-management/index.md). Reference: [http module](https://docs.python.org/3/library/http.html).

---

## HTTPStatus enum — [HTTP status codes](https://docs.python.org/3/library/http.html#http-status-codes)

| Member | Value | Typical meaning |
|--------|-------|-----------------|
| `HTTPStatus.OK` | 200 | Success |
| `HTTPStatus.MOVED_PERMANENTLY` | 301 | Permanent redirect |
| `HTTPStatus.BAD_REQUEST` | 400 | Client error |
| `HTTPStatus.NOT_FOUND` | 404 | Missing resource |
| `HTTPStatus.INTERNAL_SERVER_ERROR` | 500 | Server fault |

Each member exposes `.value`, `.phrase`, and `.description`.

---

## HTTP methods — [HTTP methods](https://docs.python.org/3/library/http.html#http-methods)

`http.HTTPMethod` (3.11+) enumerates `GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `OPTIONS`, `PATCH`, etc., for type-safe method names in client and server code.

---

## Example — classify status codes

```python
# Goal: use HTTPStatus for range checks and phrases
import http

assert http.HTTPStatus.OK.is_success
assert http.HTTPStatus.NOT_FOUND.is_client_error
assert http.HTTPStatus.BAD_GATEWAY.is_server_error
assert http.HTTPStatus.CREATED.phrase == "Created"
assert http.HTTPMethod.GET.value == "GET"
```

---

## Submodule map

| Submodule | Role |
|-----------|------|
| [`http.client`](../httpclient-http-protocol-client/index.md) | HTTP/1.1 client connections |
| [`http.server`](../httpserver-http-servers/index.md) | Simple HTTP servers |
| [`http.cookies`](../httpcookies-http-state-management/index.md) | Cookie objects for responses |
| [`http.cookiejar`](../httpcookiejar-cookie-handling-for-http-clients/index.md) | Client-side cookie storage |
