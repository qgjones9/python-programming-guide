# [xml.dom.pulldom — Support for building partial DOM trees](https://docs.python.org/3/library/xml.dom.pulldom.html)

[`xml.dom.pulldom`](https://docs.python.org/3/library/xml.dom.pulldom.html) combines **SAX-style streaming** with **DOM subtrees**: the parser yields `(event, node)` pairs; call `expandNode()` to materialize a full DOM fragment under the current element. Ideal when only portions of a large document need random access. Reference: [pulldom API](https://docs.python.org/3/library/xml.dom.pulldom.html).

---

## Key symbols

| Symbol | Role |
|--------|------|
| `parse(stream_or_string)` | Return a `DOMEventStream` iterator |
| `parseString(string)` | Parse in-memory XML |
| `DOMEventStream.expandNode(node)` | Build complete DOM for current element |
| Events `START_ELEMENT`, `END_ELEMENT`, … | Drive processing loop |

---

## Example — expand only matching elements

```python
# Goal: stream XML and expand DOM for selected tags only
import xml.dom.pulldom as pulldom

xml = "<root><item id='1'/><item id='2'/></root>"
stream = pulldom.parseString(xml)

seen_ids = []
for event, node in stream:
    if event == pulldom.START_ELEMENT and node.tagName == "item":
        stream.expandNode(node)
        seen_ids.append(node.getAttribute("id"))

assert seen_ids == ["1", "2"]
```

---

## When to choose pulldom

| Scenario | Recommendation |
|----------|----------------|
| Need DOM methods on occasional elements | pulldom |
| Never need random access | Pure SAX ([`xml.sax`](../xmlsax-support-for-sax2-parsers/index.md)) |
| Whole document fits in memory | ElementTree or minidom |
