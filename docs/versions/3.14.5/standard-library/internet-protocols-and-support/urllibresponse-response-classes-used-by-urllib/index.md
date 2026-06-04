# [urllib.response — Response classes used by urllib](https://docs.python.org/3/library/urllib.request.html#module-urllib.response)

[`urllib.response`](https://docs.python.org/3/library/urllib.request.html#module-urllib.response) defines **base classes** for objects returned by [`urllib.request`](../urllibrequest-extensible-library-for-opening-urls/index.md). Application code usually treats responses as file-like objects from `urlopen`; subclass these types when implementing custom handlers.

---

## Class hierarchy

| Class | Role |
|-------|------|
| `addbase` | Adds `.fp`, `.fileno()`, `.read()`, context manager support |
| `addclosehook` | Calls a hook when response is closed |
| `addinfo` | Adds `.info()` returning message headers (`email.message.Message`) |
| `addinfourl` | Combines info + close hook; typical `urlopen` result |

---

## Example — inspect addinfourl metadata

```python
# Goal: open data URL and read status/headers from addinfourl
import urllib.request
import urllib.response

with urllib.request.urlopen("data:text/plain;charset=utf-8,hello") as resp:
    assert isinstance(resp, urllib.response.addinfourl)
    assert resp.read() == b"hello"
    headers = resp.info()
    assert headers.get_content_type() == "text/plain"
```

---

## Implementing handlers

Custom `urllib.request` handlers return objects compatible with `addinfourl` so callers can rely on `.read()`, `.info()`, and context-manager cleanup.
