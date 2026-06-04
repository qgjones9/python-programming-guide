# [html.parser — Simple HTML and XHTML parser](https://docs.python.org/3/library/html.parser.html)

[`html.parser`](https://docs.python.org/3/library/html.parser.html) implements a **non-validating** HTML/XHTML scanner that calls methods on a subclass of `HTMLParser` as tags, data, and comments are encountered. It builds no DOM tree—override callbacks to collect structure or text. Full method list: [HTMLParser Methods](https://docs.python.org/3/library/html.parser.html#htmlparser-methods).

---

## Subclassing `HTMLParser`

| Callback | When it fires |
|----------|---------------|
| `handle_starttag(tag, attrs)` | Opening tag (attrs is `list[tuple[str, str \| None]]`) |
| `handle_endtag(tag)` | Closing tag |
| `handle_data(data)` | Text between tags |
| `handle_comment(data)` | `<!-- … -->` content |
| `handle_entityref(name)` / `handle_charref(name)` | Named or numeric character references |

Use `HTMLParser(convert_charrefs=True)` (default since 3.4) so character references become plain text in `handle_data`.

---

## Example — extract link hrefs

```python
# Goal: collect anchor href attributes from an HTML fragment
from html.parser import HTMLParser


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value:
                    self.links.append(value)


parser = LinkCollector()
parser.feed('<p>See <a href="/docs">docs</a> and <a href="#top">top</a>.</p>')
parser.close()
assert parser.links == ["/docs", "#top"]
```

---

## Limitations and alternatives

| Limitation | Alternative |
|------------|-------------|
| Not a full browser HTML5 parser | Third-party `html5lib` or `lxml.html` for messy real-world pages |
| No CSS selector queries | Build a tree with ElementTree/lxml or use BeautifulSoup |
| Untrusted input risks | Treat as convenience only; sanitize externally supplied HTML |
