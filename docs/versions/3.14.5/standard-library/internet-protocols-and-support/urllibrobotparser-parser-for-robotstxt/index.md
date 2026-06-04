# [urllib.robotparser — Parser for robots.txt](https://docs.python.org/3/library/urllib.robotparser.html)

[`urllib.robotparser`](https://docs.python.org/3/library/urllib.robotparser.html) reads a **`robots.txt` file** and answers whether a given user-agent may fetch a URL path. Used by crawlers and polite fetchers—not a security boundary (sites may ignore robots rules). Reference: [RobotFileParser](https://docs.python.org/3/library/urllib.robotparser.html).

---

## RobotFileParser workflow

| Step | Method |
|------|--------|
| Construct | `RobotFileParser(url='https://example.com/robots.txt')` |
| Load rules | `read()` from URL, `parse(lines)`, or `set_url` + `read()` |
| Query | `can_fetch(useragent, url)` → `bool` |
| Crawl delay | `crawl_delay(useragent)` if declared |

---

## Example — parse rules from string lines

```python
# Goal: evaluate allow/disallow rules offline
import urllib.robotparser as robotparser

rp = robotparser.RobotFileParser()
rp.parse(
    [
        "User-agent: *",
        "Disallow: /admin/",
    ]
)

assert rp.can_fetch("*", "https://example.com/public/page")
assert not rp.can_fetch("*", "https://example.com/admin/settings")
```

---

## Limitations

| Limitation | Detail |
|------------|--------|
| Not authenticated access control | Malicious clients ignore robots.txt |
| Wildcards and `$` suffix | Supported per modern robots.txt conventions in recent Python versions |
| Must fetch robots.txt yourself | Parser does not HTTP-fetch unless you call `read()` with URL set |
