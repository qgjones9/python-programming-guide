# [Graphical user interfaces with Tk](https://docs.python.org/3/library/tk.html)

Tk/Tcl has long been bundled with Python. The standard library exposes it through **`tkinter`** (classic widgets) and **`tkinter.ttk`** (themed widgets from Tk 8.5+). Related modules cover dialogs, fonts, scrolling text, drag-and-drop (experimental), the **IDLE** editor, and **`turtle`** graphics. Full API prose stays on [docs.python.org](https://docs.python.org/3/library/tk.html); this hub orients you to each module and common integration patterns.

Tkinter is **optional** in some distributions—verify with `python -m tkinter` before building a GUI-dependent app.

---

## Module overview

| Module | Primary use |
|--------|-------------|
| [`tkinter`](tkinter-python-interface-to-tcltk/index.md) | Core widget classes, geometry managers, event loop |
| [`tkinter.ttk`](tkinterttk-tk-themed-widgets/index.md) | Modern themed widgets and `Style` configuration |
| [`tkinter.colorchooser`](tkintercolorchooser-color-choosing-dialog/index.md) | Native color-picker dialog |
| [Tkinter Dialogs](tkinter-dialogs/index.md) | `simpledialog`, `filedialog`, `commondialog` base |
| [`tkinter.messagebox`](tkintermessagebox-tkinter-message-prompts/index.md) | Info, warning, error, and yes/no prompts |
| [`tkinter.scrolledtext`](tkinterscrolledtext-scrolled-text-widget/index.md) | Text widget pre-wired to a vertical scrollbar |
| [`tkinter.font`](tkinterfont-tkinter-font-wrapper/index.md) | Named fonts, metrics, family enumeration |
| [`tkinter.dnd`](tkinterdnd-drag-and-drop-support/index.md) | Experimental in-app drag-and-drop |
| [IDLE](idle-python-editor-and-shell/index.md) | Interactive shell and editor built on tkinter |
| [`turtle`](turtle-turtle-graphics/index.md) | Logo-style drawing for learners and quick plots |

---

## Architecture at a glance

| Layer | Role |
|-------|------|
| **Tcl** | Embedded scripting language; each `Tk` instance owns an interpreter |
| **Tk** | Classic widget set; maps to X11, Cocoa, or GDI |
| **Ttk** | Themed widgets; styling via `ttk.Style`, not per-widget `fg`/`bg` |
| **`_tkinter`** | C extension bridging Python to Tcl/Tk (never import directly) |

Python calls assemble Tcl command strings; `_tkinter` evaluates them in the attached interpreter. Widget options in Python correspond to Tcl `-option` flags.

---

## Choosing the right module

| Task | Start here |
|------|------------|
| Build a desktop app window | [`tkinter`](tkinter-python-interface-to-tcltk/index.md) + [`tkinter.ttk`](tkinterttk-tk-themed-widgets/index.md) |
| Ask for a file path or directory | [`tkinter.filedialog`](tkinter-dialogs/index.md) |
| Simple numeric or string input | [`tkinter.simpledialog`](tkinter-dialogs/index.md) |
| Confirm destructive action | [`tkinter.messagebox`](tkintermessagebox-tkinter-message-prompts/index.md) |
| Multi-line log or editor pane | [`tkinter.scrolledtext`](tkinterscrolledtext-scrolled-text-widget/index.md) |
| Teach programming with drawing | [`turtle`](turtle-turtle-graphics/index.md) |
| Edit Python interactively | [IDLE](idle-python-editor-and-shell/index.md) (`idlelib`) |

---

## Cross-cutting best practices

| Practice | Why |
|----------|-----|
| Prefer **`ttk`** widgets for new UI | Native look; styling centralized in `Style` |
| Run **`root.mainloop()`** (or equivalent) | Widgets are not shown until geometry is managed and the loop runs |
| Keep event handlers **short** | Tcl/Tk is single-threaded; long work blocks repaints and input |
| Offload heavy work to **threads or processes** | Post results back to the GUI thread via `after()` or queues |
| Consult **Tcl/Tk man pages** for option details | Tkinter method names map to Tcl commands and `winfo_*` helpers |
| Treat **`tkinter.dnd`** as experimental | Due for deprecation when native Tk DND lands |

```python
# Goal: typical imports for a modern tkinter app (illustrative — requires tkinter)
# from tkinter import Tk
# from tkinter import ttk
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello").grid(column=0, row=0)
# root.mainloop()
assert True  # placeholder when tkinter is not installed in CI
```

---

## Common pitfalls

| Pitfall | What goes wrong | Mitigation |
|---------|-----------------|------------|
| Forgetting geometry management | Widget created but invisible | Call `grid()`, `pack()`, or `place()` |
| Mixing classic and ttk styling | `fg`/`bg` ignored on ttk widgets | Use `ttk.Style().configure(...)` |
| Blocking the event loop | Frozen UI during downloads | Use threads + `queue` + `after()` |
| Multiple `Tk()` instances | Shared event queue conflicts | One root per thread; prefer `Toplevel` |
| Outdated tutorials | Pre-8.5 widget APIs | Cross-check with Python 3.14 docs and ttk |

---

## Sections in this repo

| Section | Summary |
|---------|---------|
| [tkinter — Python interface to Tcl/Tk](tkinter-python-interface-to-tcltk/index.md) | Widget hierarchy, geometry, threading, Tcl bridge |
| [tkinter.ttk — Tk themed widgets](tkinterttk-tk-themed-widgets/index.md) | Themed widget set, `Style`, layouts |
| [tkinter.colorchooser — Color choosing dialog](tkintercolorchooser-color-choosing-dialog/index.md) | `askcolor()` modal picker |
| [Tkinter Dialogs](tkinter-dialogs/index.md) | File, folder, and simple input dialogs |
| [tkinter.messagebox — Tkinter message prompts](tkintermessagebox-tkinter-message-prompts/index.md) | Modal alerts and questions |
| [tkinter.scrolledtext — Scrolled Text Widget](tkinterscrolledtext-scrolled-text-widget/index.md) | Text + scrollbar composite |
| [tkinter.font — Tkinter font wrapper](tkinterfont-tkinter-font-wrapper/index.md) | Font objects and metrics |
| [tkinter.dnd — Drag and drop support](tkinterdnd-drag-and-drop-support/index.md) | Experimental DND handlers |
| [IDLE — Python editor and shell](idle-python-editor-and-shell/index.md) | `idlelib` features and menus |
| [turtle — Turtle graphics](turtle-turtle-graphics/index.md) | Logo-style drawing API |
