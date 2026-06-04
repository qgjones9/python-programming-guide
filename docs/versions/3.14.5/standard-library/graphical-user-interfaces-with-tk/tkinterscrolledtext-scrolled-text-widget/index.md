# [tkinter.scrolledtext — Scrolled Text Widget](https://docs.python.org/3/library/tkinter.scrolledtext.html)

**`tkinter.scrolledtext.ScrolledText`** combines a **`Text`** widget and vertical **`Scrollbar`** inside a **`Frame`**, with scroll commands already wired. It inherits **`grid`** and **`pack`** from the frame so you can treat it like any other container widget. Canonical docs: [tkinter.scrolledtext.html](https://docs.python.org/3/library/tkinter.scrolledtext.html).

---

## Scope

| Attribute | Role |
|-----------|------|
| **`frame`** | Surrounding `Frame` holding text + scrollbar |
| **`vbar`** | Vertical scrollbar widget |
| (text API) | All standard **`Text`** methods: `insert`, `get`, `delete`, tags, … |

Use **`ScrolledText`** when you need a log pane, REPL output, or multi-line editor without manually connecting **`yscrollcommand`**.

---

### ScrolledText class — [ScrolledText](https://docs.python.org/3/library/tkinter.scrolledtext.html#tkinter.scrolledtext.ScrolledText)

Construction accepts the same keyword options as **`Text`** (`wrap`, `width`, `height`, `font`, …) plus frame packing options forwarded to the outer frame.

```python
# Goal: simulate append-only log buffer logic (no tkinter required)
class LogBuffer:
    def __init__(self):
        self._lines = []

    def append(self, line):
        self._lines.append(line)

    def get_all(self):
        return "\n".join(self._lines)

log = LogBuffer()
log.append("started")
log.append("done")
assert log.get_all() == "started\ndone"
```

```python
# Goal: populate a ScrolledText widget (illustrative — requires tkinter + display)
# from tkinter import Tk
# from tkinter.scrolledtext import ScrolledText
# root = Tk()
# txt = ScrolledText(root, width=40, height=10, wrap="word")
# txt.pack(fill="both", expand=True)
# txt.insert("end", "Line 1\n")
# txt.insert("end", "Line 2\n")
# assert "Line 1" in txt.get("1.0", "end")
# root.destroy()
assert True
```

---

## Advanced access

When you need finer control:

- **`widget.vbar.set(0, 1)`** — manual scroll position (rare).
- **`widget.frame.grid(...)`** instead of packing the composite—call geometry on **`frame`** if you bypass inherited managers.
- For horizontal scrolling, build **`Text` + Scrollbar`** manually; **`ScrolledText`** only wires vertical scrolling.

---

## Best practices

| Practice | Why |
|----------|-----|
| Set **`wrap="word"`** for prose logs | Avoids mid-word breaks |
| Use **`state="disabled"`** for read-only logs | Prevents accidental edits; toggle for append |
| Bind **`<<Modified>>`** or poll for autoscroll | Keep view at end during streaming output |
| Prefer **`Text` + tags** for syntax coloring | `ScrolledText` is still a `Text` underneath |

---

## See also

- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — `Text` widget and scrollcommand pattern
- [IDLE](../idle-python-editor-and-shell/index.md) — multi-line editor built on tkinter text widgets
