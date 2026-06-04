# [urllib — URL handling modules](https://docs.python.org/3/library/urllib.html)

The [`urllib`](https://docs.python.org/3/library/urllib.html) **package** groups submodules for opening URLs, parsing components, handling errors, and reading `robots.txt`. Import submodules explicitly (`import urllib.request`, `import urllib.parse`). Package overview: [docs.python.org](https://docs.python.org/3/library/urllib.html).

---

## Submodule map

| Submodule | Role |
|-----------|------|
| [`urllib.request`](../urllibrequest-extensible-library-for-opening-urls/index.md) | Open URLs; extensible `OpenerDirector` |
| [`urllib.parse`](../urllibparse-parse-urls-into-components/index.md) | Split, join, quote, and encode query strings |
| [`urllib.error`](../urlliberror-exception-classes-raised-by-urllibrequest/index.md) | `URLError`, `HTTPError` |
| [`urllib.response`](../urllibresponse-response-classes-used-by-urllib/index.md) | Response wrapper base classes |
| [`urllib.robotparser`](../urllibrobotparser-parser-for-robotstxt/index.md) | Parse and query robots.txt rules |

There is no `urllib.urlopen` at package level—use `urllib.request.urlopen`.

---

## Example — typical import pattern

```python
# Goal: parse a URL then fetch via data URL (no network)
import urllib.parse as parse
import urllib.request as request

url = "https://example.com/search?q=hello+world"
parts = parse.urlparse(url)
query = parse.parse_qs(parts.query)
assert query["q"] == ["hello world"]

with request.urlopen("data:text/plain,hi") as resp:
    assert resp.read() == b"hi"
```

---

## Modern alternatives

For production HTTP clients (connection pooling, HTTP/2, async), third-party libraries such as **requests** or **httpx** are common. The stdlib remains useful for minimal dependencies and teaching.
