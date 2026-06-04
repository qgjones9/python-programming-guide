# [Internet Protocols and Support](https://docs.python.org/3/library/internet.html)

This chapter covers **pure-Python client and server modules** for URLs, HTTP, email protocols, UUIDs, IP addressing, and related web infrastructure. Most modules depend on the system [`socket`](../networking-and-interprocess-communication/socket-low-level-networking-interface/index.md) module. Full reference: [docs.python.org](https://docs.python.org/3/library/internet.html).

---

## Layered overview

| Layer | Modules |
|-------|---------|
| URLs and fetching | [`urllib`](urllib-url-handling-modules/index.md), [`urllib.parse`](urllibparse-parse-urls-into-components/index.md), [`urllib.request`](urllibrequest-extensible-library-for-opening-urls/index.md) |
| HTTP semantics | [`http`](http-http-modules/index.md), [`http.client`](httpclient-http-protocol-client/index.md), [`http.server`](httpserver-http-servers/index.md), cookies ([`http.cookies`](httpcookies-http-state-management/index.md), [`http.cookiejar`](httpcookiejar-cookie-handling-for-http-clients/index.md)) |
| Application servers | [`wsgiref`](wsgiref-wsgi-utilities-and-reference-implementation/index.md), [`socketserver`](socketserver-a-framework-for-network-servers/index.md) |
| Mail protocols | [`poplib`](poplib-pop3-protocol-client/index.md), [`imaplib`](imaplib-imap4-protocol-client/index.md), [`smtplib`](smtplib-smtp-protocol-client/index.md) |
| Other clients | [`ftplib`](ftplib-ftp-protocol-client/index.md), [`xmlrpc.client`](xmlrpcclient-xml-rpc-client-access/index.md) |
| Utilities | [`ipaddress`](ipaddress-ipv4ipv6-manipulation-library/index.md), [`uuid`](uuid-uuid-objects-according-to-rfc-9562/index.md), [`webbrowser`](webbrowser-convenient-web-browser-controller/index.md) |

---

## Choosing the right tool

| Task | Start here |
|------|------------|
| Parse or build URLs | [`urllib.parse`](urllibparse-parse-urls-into-components/index.md) |
| HTTP GET/POST to external services | [`urllib.request`](urllibrequest-extensible-library-for-opening-urls/index.md) or third-party `httpx`/`requests` |
| Inspect HTTP status names | [`http.HTTPStatus`](http-http-modules/index.md) |
| Lightweight local HTTP server | [`http.server`](httpserver-http-servers/index.md) |
| WSGI app testing | [`wsgiref`](wsgiref-wsgi-utilities-and-reference-implementation/index.md) |
| Validate CIDR or host addresses | [`ipaddress`](ipaddress-ipv4ipv6-manipulation-library/index.md) |
| Generate unique IDs | [`uuid`](uuid-uuid-objects-according-to-rfc-9562/index.md) |

---

## Security reminders

| Risk | Mitigation |
|------|------------|
| SSRF via `urllib.request` | Block private IPs; allowlist schemes and hosts |
| Binding `0.0.0.0` in dev servers | Use `127.0.0.1`; never expose `http.server` to the internet |
| Cleartext credentials (FTP/POP/SMTP) | Prefer TLS variants (`FTP_TLS`, `POP3_SSL`, `SMTP_SSL`) |
| XML-RPC entities | Treat as legacy; harden or replace for untrusted peers |

```python
# Goal: combine URL parsing with HTTP status constants
import urllib.parse as urlparse
import http

parts = urlparse.urlparse("https://example.com/path?q=1")
assert parts.netloc == "example.com"
assert http.HTTPStatus.OK == 200
assert http.HTTPStatus.NOT_FOUND.phrase == "Not Found"
```

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [webbrowser — Convenient web-browser controller](webbrowser-convenient-web-browser-controller/index.md) | Open URLs in a desktop browser |
| [wsgiref — WSGI Utilities and Reference Implementation](wsgiref-wsgi-utilities-and-reference-implementation/index.md) | WSGI environ helpers and test server |
| [urllib — URL handling modules](urllib-url-handling-modules/index.md) | Package overview |
| [urllib.request — Extensible library for opening URLs](urllibrequest-extensible-library-for-opening-urls/index.md) | Fetch URLs with handlers and openers |
| [urllib.response — Response classes used by urllib](urllibresponse-response-classes-used-by-urllib/index.md) | `addbase`, `addinfourl` wrappers |
| [urllib.parse — Parse URLs into components](urllibparse-parse-urls-into-components/index.md) | Split, join, quote URLs |
| [urllib.error — Exception classes raised by urllib.request](urlliberror-exception-classes-raised-by-urllibrequest/index.md) | `URLError`, `HTTPError` |
| [urllib.robotparser — Parser for robots.txt](urllibrobotparser-parser-for-robotstxt/index.md) | Crawl permission rules |
| [http — HTTP modules](http-http-modules/index.md) | Status codes, methods, constants |
| [http.client — HTTP protocol client](httpclient-http-protocol-client/index.md) | Low-level HTTP/1.1 client |
| [ftplib — FTP protocol client](ftplib-ftp-protocol-client/index.md) | FTP and FTP_TLS sessions |
| [poplib — POP3 protocol client](poplib-pop3-protocol-client/index.md) | POP3 mail retrieval |
| [imaplib — IMAP4 protocol client](imaplib-imap4-protocol-client/index.md) | IMAP4 mail access |
| [smtplib — SMTP protocol client](smtplib-smtp-protocol-client/index.md) | Send mail via SMTP |
| [uuid — UUID objects according to RFC 9562](uuid-uuid-objects-according-to-rfc-9562/index.md) | UUID generation and parsing |
| [socketserver — A framework for network servers](socketserver-a-framework-for-network-servers/index.md) | TCP/UDP server skeleton |
| [http.server — HTTP servers](httpserver-http-servers/index.md) | Simple static/ CGI HTTP server |
| [http.cookies — HTTP state management](httpcookies-http-state-management/index.md) | Cookie header parsing (server-side) |
| [http.cookiejar — Cookie handling for HTTP clients](httpcookiejar-cookie-handling-for-http-clients/index.md) | Client cookie storage |
| [xmlrpc — XMLRPC server and client modules](xmlrpc-xmlrpc-server-and-client-modules/index.md) | XML-RPC overview |
| [xmlrpc.client — XML-RPC client access](xmlrpcclient-xml-rpc-client-access/index.md) | Remote procedure calls |
| [xmlrpc.server — Basic XML-RPC servers](xmlrpcserver-basic-xml-rpc-servers/index.md) | Publish RPC methods |
| [ipaddress — IPv4/IPv6 manipulation library](ipaddress-ipv4ipv6-manipulation-library/index.md) | Networks, hosts, CIDR math |
