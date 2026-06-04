# [tkinter — Python interface to Tcl/Tk](https://docs.python.org/3/library/tkinter.html)

The **`tkinter`** package is Python’s standard binding to Tcl/Tk. It wraps Tcl commands as widget classes, adds Pythonic helpers (geometry managers as methods, option dictionaries), and ships with **`tkinter.constants`** for symbolic names like `LEFT` and `BOTH`. Canonical reference: [tkinter.html](https://docs.python.org/3/library/tkinter.html).

Run `python -m tkinter` to confirm installation and print the bundled Tcl/Tk version.

---

## Scope

| Topic | Covered here |
|-------|--------------|
| `Tk`, `Toplevel`, widget classes | Frame, Label, Button, Entry, Text, Canvas, … |
| Geometry managers | `pack()`, `grid()`, `place()` |
| Event loop | `mainloop()`, `update()`, `after()` |
| Tcl bridge | How Python calls map to Tcl/Tk commands |
| Threading | Cross-thread `tkinter` calls and event posting |

For themed widgets, see [`tkinter.ttk`](../tkinterttk-tk-themed-widgets/index.md).

---

### Architecture — [Architecture](https://docs.python.org/3/library/tkinter.html#architecture)

- Each **`Tk()`** instance creates a Tcl interpreter and a root toplevel window.
- Widgets form a **parent/child tree**; the first constructor argument is always the parent.
- Internally, method calls become Tcl strings executed by `_tkinter`.
- **Ttk** lives in a separate module but shares the same interpreter.

---

### Hello World — [A Hello World Program](https://docs.python.org/3/library/tkinter.html#a-hello-world-program)

Key steps every app follows:

1. Create **`Tk()`** root.
2. Build widgets inside a container (`ttk.Frame` recommended).
3. Apply a geometry manager (`grid`, `pack`, or `place`).
4. Enter **`mainloop()`** so events are processed.

```python
# Goal: minimal ttk hello-world structure (illustrative — requires tkinter + display)
# from tkinter import Tk
# from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()
assert True
```

---

### Important Tk concepts — [Important Tk Concepts](https://docs.python.org/3/library/tkinter.html#important-tk-concepts)

| Concept | Meaning |
|---------|---------|
| **Widgets** | Python objects (`Label`, `Button`, …) backed by Tcl widget paths |
| **Hierarchy** | Every widget except the root has a `master` parent |
| **Options** | Keyword args at construction or via `configure()` / `widget["option"]` |
| **Geometry** | Layout is explicit—widgets do not appear until packed/gridded/placed |
| **Event loop** | UI updates and callbacks run only while `mainloop()` (or `update()`) executes |

---

### Tcl/Tk mapping — [Understanding How Tkinter Wraps Tcl/Tk](https://docs.python.org/3/library/tkinter.html#understanding-how-tkinter-wraps-tcl-tk)

| Tkinter | Tcl/Tk equivalent |
|---------|-------------------|
| `ttk.Label(frm, text="Hi")` | `ttk::label .frm.lbl -text "Hi"` |
| `widget.grid(column=0, row=0)` | `grid .frm.lbl -column 0 -row 0` |
| `root.destroy()` | `destroy .` |
| `btn.invoke()` | `.frm.btn invoke` |

Use **`widget.configure()`** without arguments to introspect all options and current values; **`widget.keys()`** lists option names.

---

### Setting options — [Setting Options](https://docs.python.org/3/library/tkinter.html#setting-options)

Three equivalent styles after construction:

```python
# Goal: document option-setting patterns (illustrative widget setup)
class FakeButton:
    def __init__(self, fg="black", bg="white"):
        self._opts = {"fg": fg, "bg": bg}

    def __setitem__(self, key, value):
        self._opts[key] = value

    def config(self, **kwargs):
        self._opts.update(kwargs)

fred = FakeButton(fg="red", bg="blue")
fred["fg"] = "green"
fred.config(bg="yellow")
assert fred._opts == {"fg": "green", "bg": "yellow"}
```

---

### Geometry managers — [The Packer](https://docs.python.org/3/library/tkinter.html#the-packer)

| Manager | Typical use |
|---------|-------------|
| **`pack()`** | Stack widgets top/bottom/left/right; good for simple toolbars |
| **`grid()`** | Row/column tables; precise alignment |
| **`place()`** | Absolute or relative pixel placement; less common |

Common early bug: creating a widget but never calling a geometry manager—nothing appears on screen.

---

### Threading model — [Threading model](https://docs.python.org/3/library/tkinter.html#threading-model)

- Tcl/Tk runs a **single-threaded event loop** per interpreter.
- `tkinter` can marshal calls from other Python threads via the interpreter event queue.
- **Do not** run long computations inside callbacks—use `threading` + `queue.Queue` and poll with `root.after()`.
- Avoid multiple **`Tk()`** roots in one thread; use **`Toplevel`** for extra windows.

---

### Handy reference — [Handy Reference](https://docs.python.org/3/library/tkinter.html#handy-reference)

| Need | Where to look |
|------|---------------|
| Standard widget options | Tcl `options` man page; `widget.configure().keys()` |
| Widget-specific behavior | Tcl man page for that widget class |
| Window metrics | `winfo_*` methods (`winfo_width`, `winfo_x`, …) |
| Bindings and events | `bind()`, `bind_all()`, event patterns like `<Button-1>` |

---

## See also

- [`tkinter.ttk`](../tkinterttk-tk-themed-widgets/index.md) — themed widget set
- [Tkinter Dialogs](../tkinter-dialogs/index.md) — file and input dialogs
- [Graphical user interfaces with Tk](../index.md) — section hub
