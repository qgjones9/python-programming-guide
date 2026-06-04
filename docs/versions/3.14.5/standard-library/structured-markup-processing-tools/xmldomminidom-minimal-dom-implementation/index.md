# [xml.dom.minidom — Minimal DOM implementation](https://docs.python.org/3/library/xml.dom.minidom.html)

[`xml.dom.minidom`](https://docs.python.org/3/library/xml.dom.minidom.html) is a **lightweight DOM Level 1–style** implementation: parse XML into a mutable tree, walk nodes, and serialize with `toxml()` / `toprettyxml()`. It is slower and heavier than ElementTree but familiar if you know browser DOM APIs. Reference: [minidom documentation](https://docs.python.org/3/library/xml.dom.minidom.html).

---

## Common entry points

| Function | Role |
|----------|------|
| `minidom.parseString(s)` | Parse XML text into a `Document` |
| `minidom.parse(filename_or_file)` | Parse from path or file object |
| `doc.getElementsByTagName(name)` | Live NodeList of matching elements |
| `node.toxml()` / `toprettyxml(indent="  ")` | Serialize subtree |

---

## Example — parse and mutate

```python
# Goal: parse XML with minidom, update text, serialize
import xml.dom.minidom as minidom

doc = minidom.parseString(b"<team><player>Ada</player></team>")
players = doc.getElementsByTagName("player")
assert len(players) == 1
players[0].firstChild.replaceWholeText("Grace")

out = doc.toxml()
assert "<player>Grace</player>" in out
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Prefer ElementTree for new projects | Better performance and simpler API |
| Call `unlink()` on large trees when done | Helps break reference cycles in long-running processes |
| Avoid `toprettyxml()` in production hot paths | Pretty printing adds overhead and extra whitespace |
