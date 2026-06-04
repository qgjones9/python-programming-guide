# [webbrowser — Convenient web-browser controller](https://docs.python.org/3/library/webbrowser.html)

[`webbrowser`](https://docs.python.org/3/library/webbrowser.html) locates the user’s **desktop browser** and opens URLs in a new tab or window. Useful for CLI tools and documentation generators—not for headless HTTP fetching ([`urllib.request`](../urllibrequest-extensible-library-for-opening-urls/index.md) handles that). Reference: [webbrowser](https://docs.python.org/3/library/webbrowser.html).

---

## Main API

| Function | Role |
|----------|------|
| `webbrowser.open(url, new=0, autoraise=True)` | Open URL (`new=1` new window, `2` new tab) |
| `webbrowser.open_new(url)` / `open_new_tab(url)` | Explicit window/tab |
| `webbrowser.get(using=None)` | Return a `Browser` controller |
| `webbrowser.register(name, constructor, ...)` | Add custom browser backend |

Environment variables such as **`BROWSER`** override detection on Unix.

---

## Example — resolve browser without opening

```python
# Goal: inspect registered browser types offline
import webbrowser

controller = webbrowser.get()
assert hasattr(controller, "open")
assert isinstance(webbrowser._browsers, dict)
assert webbrowser.open.__name__ == "open"
```

---

## Command-line interface

`python -m webbrowser [-t | -n] url` opens a URL from the shell; see [Command-line interface](https://docs.python.org/3/library/webbrowser.html#command-line-interface).

---

## Limitations

| Limitation | Detail |
|------------|--------|
| Requires graphical/desktop session | No-op or errors in headless CI |
| Not sandboxed | Only pass trusted URLs |
