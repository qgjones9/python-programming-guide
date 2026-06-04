# [tkinter.dnd — Drag and drop support](https://docs.python.org/3/library/tkinter.dnd.html)

**`tkinter.dnd`** adds **experimental** drag-and-drop between widgets in the same application (same or different windows). It will be **deprecated** when replaced by native Tk DND. Canonical docs: [tkinter.dnd.html](https://docs.python.org/3/library/tkinter.dnd.html).

!!! warning "Experimental API"
    Treat this module as legacy/experimental. Prefer planning for native Tk DND in future Tk versions; do not build long-term features solely on `tkinter.dnd`.

---

## Drag lifecycle

1. Bind **`ButtonPress`** (or similar) on the **source** widget.
2. Callback calls **`dnd_start(source, event)`** — returns a **`DndHandler`** or `None`.
3. Handler tracks **`Motion`** and **`ButtonRelease`** on the root.
4. **Target search** (top-down under pointer):
   - Widget must expose callable **`dnd_accept(source, event)`**.
   - If missing or returns `None`, walk to **parent**.
5. On drop: **`dnd_enter`**, **`dnd_commit`**, **`dnd_leave`**, **`dnd_end`** on participating objects.

---

### DndHandler — [DndHandler](https://docs.python.org/3/library/tkinter.dnd.html#tkinter.dnd.DndHandler)

| Method | Role |
|--------|------|
| **`cancel(event=None)`** | Abort drag |
| **`finish(event, commit=0)`** | End drag; **`commit=1`** signals successful drop |
| **`on_motion(event)`** | Find target under cursor while dragging |
| **`on_release(event)`** | Complete drag on button release |

---

### dnd_start — [dnd_start](https://docs.python.org/3/library/tkinter.dnd.html#tkinter.dnd.dnd_start)

Factory: **`dnd_start(source, event)`** begins tracking from the initiating event.

Target widgets implement:

| Method | When called |
|--------|-------------|
| **`dnd_accept(source, event)`** | Candidate target under pointer; return self or `None` |
| **`dnd_enter(source, event)`** | Pointer entered target |
| **`dnd_leave(source, event)`** | Pointer left target |
| **`dnd_commit(source, event)`** | Drop accepted |
| **`dnd_end(target, event)`** | Drag finished (source-side) |

```python
# Goal: model target lookup walking up the widget tree (pure Python)
class Widget:
    def __init__(self, name, parent=None, accept=None):
        self.name = name
        self.master = parent
        self.dnd_accept = accept

def find_drop_target(leaf, source):
    node = leaf
    while node is not None:
        accept = getattr(node, "dnd_accept", None)
        if callable(accept) and accept(source, None) is not None:
            return node
        node = node.master
    return None

root = Widget("root")
panel = Widget("panel", root, accept=lambda s, e: panel)
label = Widget("label", panel)
assert find_drop_target(label, "item") is panel
assert find_drop_target(Widget("solo"), "item") is None
```

```python
# Goal: wire a draggable label (illustrative — requires tkinter + tkinter.dnd)
# from tkinter import Tk, Label
# from tkinter.dnd import dnd_start
# root = Tk()
# class DragLabel(Label):
#     def dnd_accept(self, source, event):
#         return self
#     def dnd_commit(self, source, event):
#         self.config(text=f"Dropped from {source}")
# src = DragLabel(root, text="Drag me", relief="raised")
# src.bind("<ButtonPress>", lambda e: dnd_start(src, e))
# root.mainloop()
assert True
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Implement **`dnd_accept`** on every drop zone | Required for target discovery |
| Call **`finish(..., commit=1)`** only on valid drops | Avoids spurious commits |
| Document experimental status for users | API may disappear with Tk DND |
| Consider **click-to-move** for simple cases | Less fragile than custom DND |

---

## See also

- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — event bindings (`bind`, event patterns)
- [Graphical user interfaces with Tk](../index.md) — section hub
