# [Tkinter Dialogs](https://docs.python.org/3/library/dialog.html)

The **Tkinter Dialogs** chapter groups modal helper modules built on **`tkinter.commondialog.Dialog`**: **`simpledialog`** (typed input), **`filedialog`** (open/save/directory pickers), and the shared **`commondialog`** base. Canonical docs: [dialog.html](https://docs.python.org/3/library/dialog.html).

---

## Module overview

| Module | Primary use |
|--------|-------------|
| **`tkinter.simpledialog`** | `askstring`, `askinteger`, `askfloat`; custom `Dialog` subclass |
| **`tkinter.filedialog`** | Native open/save/directory dialogs; legacy `FileDialog` classes |
| **`tkinter.commondialog`** | Base `Dialog` with `show()` |

Related: [`tkinter.messagebox`](../tkintermessagebox-tkinter-message-prompts/index.md), [`tkinter.colorchooser`](../tkintercolorchooser-color-choosing-dialog/index.md).

---

### simpledialog — [tkinter.simpledialog](https://docs.python.org/3/library/dialog.html#module-tkinter.simpledialog)

| Function | Returns |
|----------|---------|
| **`askfloat(title, prompt, **kw)`** | `float` or `None` |
| **`askinteger(title, prompt, **kw)`** | `int` or `None` |
| **`askstring(title, prompt, **kw)`** | `str` or `None` |

Subclass **`Dialog`** and override **`body(master)`** (build form, return focus widget) and optionally **`buttonbox()`** for custom buttons.

```python
# Goal: validate simpledialog keyword patterns for numeric bounds
def clamp_initial(value, minimum, maximum):
    if value is None:
        return minimum
    return max(minimum, min(maximum, value))

assert clamp_initial(150, 0, 100) == 100
assert clamp_initial(None, 0, 100) == 0
```

---

### filedialog — [tkinter.filedialog](https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog)

#### Native static functions

| Function | Returns |
|----------|---------|
| **`askopenfilename` / `askopenfilenames`** | Path string(s) or `()` / `""` |
| **`asksaveasfilename`** | Destination path or `""` |
| **`askdirectory`** | Directory path or `""` |
| **`askopenfile` / `askopenfiles` / `asksaveasfile`** | Open file object(s) in given **`mode`** |

Common keyword options:

| Option | Effect |
|--------|--------|
| **`parent`** | Host window for modality |
| **`title`** | Dialog caption |
| **`initialdir`**, **`initialfile`** | Starting location/selection |
| **`filetypes`** | Sequence of `(label, pattern)` tuples, e.g. `("Python", "*.py")` |
| **`defaultextension`** | Appended on save when user omits suffix |
| **`multiple`** | Allow multi-select (open dialogs) |
| **`mustexist`** | Directory must exist (`askdirectory`) |

```python
# Goal: build filetypes tuple for a Python project dialog
filetypes = [
    ("Python files", "*.py"),
    ("Text files", "*.txt"),
    ("All files", "*.*"),
]
labels = [label for label, _ in filetypes]
assert labels[0] == "Python files"
assert "*.py" in filetypes[0][1]
```

```python
# Goal: typical open-file flow (illustrative — requires tkinter + display)
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename
# root = Tk()
# root.withdraw()
# path = askopenfilename(
#     parent=root,
#     title="Open script",
#     filetypes=[("Python", "*.py"), ("All", "*.*")],
# )
# root.destroy()
assert True
```

#### Class hierarchy (legacy / custom)

| Class | Role |
|-------|------|
| **`Open`**, **`SaveAs`** | Native save/load windows |
| **`FileDialog`** | Toolkit-neutral file browser; subclass for custom behavior |
| **`LoadFileDialog`**, **`SaveFileDialog`** | Prebuilt OK handlers validating selection |
| **`Directory`** | Directory picker from scratch |

---

### commondialog — [tkinter.commondialog](https://docs.python.org/3/library/dialog.html#module-tkinter.commondialog)

**`Dialog(master=None, **options)`** — base for color, message, and file dialogs. Call **`show(**options)`** to display modally; keyword args can override constructor options.

---

## Best practices

| Practice | Why |
|----------|-----|
| Always set **`parent`** | Correct stacking and modality |
| Treat empty string / `None` as cancel | Do not open paths blindly |
| Use **`filetypes`** with a final `*.*` row | Lets power users pick any extension |
| Prefer **`ask*filename`** over **`ask*file`** when you need path strings | Easier lifetime management than file objects |
| Subclass **`simpledialog.Dialog`** only when built-ins are insufficient | Keeps validation logic in one place |

---

## See also

- [`tkinter.messagebox`](../tkintermessagebox-tkinter-message-prompts/index.md) — alerts and confirmations
- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — root window setup
