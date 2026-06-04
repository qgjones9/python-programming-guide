# [xml.etree.ElementTree — The ElementTree XML API](https://docs.python.org/3/library/xml.etree.elementtree.html)

[`xml.etree.ElementTree`](https://docs.python.org/3/library/xml.etree.elementtree.html) (commonly imported as `ET`) is the **standard high-level XML API**: build and traverse element trees, parse from strings or files, serialize back to bytes/text, and run a **limited XPath-like** search syntax. Reference: [ElementTree API](https://docs.python.org/3/library/xml.etree.elementtree.html).

---

## Core types and functions

| Symbol | Role |
|--------|------|
| `Element` | Node with `.tag`, `.attrib`, `.text`, `.tail`, child list |
| `ElementTree` | Root wrapper; `.getroot()`, `.write()` |
| `ET.fromstring(data)` | Parse XML text/bytes to root `Element` |
| `ET.tostring(elem)` | Serialize subtree to bytes |
| `elem.find(path)` / `findall` / `findtext` | Subset XPath search |
| `ET.SubElement(parent, tag, **attrib)` | Create and attach a child |

---

## Supported XPath subset — [Supported XPath syntax](https://docs.python.org/3/library/xml.etree.elementtree.html#supported-xpath-syntax)

| Pattern | Meaning |
|---------|---------|
| `tag` | Direct child with tag name |
| `*` | Any direct child |
| `.//tag` | Descendant search |
| `{namespace}local` | Namespaced tag when namespaces are registered |

---

## Example — build, search, serialize

```python
# Goal: construct XML, query with find/findall, round-trip serialize
import xml.etree.ElementTree as ET

root = ET.Element("catalog")
book = ET.SubElement(root, "book", id="bk1")
ET.SubElement(book, "title").text = "Python"
ET.SubElement(book, "price").text = "29.95"

found = root.find(".//title")
assert found is not None and found.text == "Python"
assert [b.get("id") for b in root.findall("book")] == ["bk1"]

xml_bytes = ET.tostring(root, encoding="unicode")
reparsed = ET.fromstring(xml_bytes)
assert reparsed.findtext(".//price") == "29.95"
```

---

## Performance tips

| Tip | Detail |
|-----|--------|
| Use `ET.iterparse()` for huge files | Drop or clear processed subtrees to limit memory |
| Prefer `xml.etree.ElementTree` over `xml.dom.minidom` | Faster and simpler for typical tasks |
| Pass `encoding="utf-8"` explicitly in `tostring`/`write` | Avoid platform-default surprises |
