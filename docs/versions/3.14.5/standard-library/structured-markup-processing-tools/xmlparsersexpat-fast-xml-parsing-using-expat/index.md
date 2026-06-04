# [xml.parsers.expat — Fast XML parsing using Expat](https://docs.python.org/3/library/pyexpat.html)

[`xml.parsers.expat`](https://docs.python.org/3/library/pyexpat.html) exposes Python bindings to **James Clark’s Expat** XML parser. Higher-level modules (SAX, ElementTree’s default parser) build on Expat internally; use this module when you need **direct callback registration** or Expat-specific error codes. Module name in imports: `xml.parsers.expat`; documented as **pyexpat**. Reference: [Expat parser](https://docs.python.org/3/library/pyexpat.html).

---

## Parser model

| Piece | Role |
|-------|------|
| `xml.parsers.expat.ParserCreate(encoding=None)` | Construct parser; optional encoding name |
| `parser.StartElementHandler`, `CharacterDataHandler`, … | Assign callables |
| `parser.Parse(data, isFinal=False)` | Feed XML chunks |
| `xml.parsers.expat.ErrorString(code)` | Map numeric code to message |
| `xml.parsers.expat.errors` | Constants such as `XML_ERROR_SYNTAX` |

---

## Example — low-level element callback

```python
# Goal: use Expat directly to collect start-tag names
import xml.parsers.expat as expat

tags = []


def start(name, attrs):
    tags.append(name)


parser = expat.ParserCreate()
parser.StartElementHandler = start
parser.Parse("<root><a/><b/></root>", True)
assert tags == ["root", "a", "b"]
```

---

## When to use Expat directly

| Case | Recommendation |
|------|----------------|
| Normal application XML | [`xml.etree.ElementTree`](../xmletreeelementtree-the-elementtree-xml-api/index.md) |
| Streaming with standard handler API | [`xml.sax`](../xmlsax-support-for-sax2-parsers/index.md) |
| Custom C-speed parser with fine control | `xml.parsers.expat` |

Expat does **not** validate against DTDs or schemas; it checks well-formedness only.
