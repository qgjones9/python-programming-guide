# [tkinter.colorchooser — Color choosing dialog](https://docs.python.org/3/library/tkinter.colorchooser.html)

**`tkinter.colorchooser`** exposes a modal native color-picker dialog. The convenience function **`askcolor()`** is what most apps call; the **`Chooser`** class (subclass of **`Dialog`**) offers the same behavior with more control. Canonical docs: [tkinter.colorchooser.html](https://docs.python.org/3/library/tkinter.colorchooser.html).

---

## Scope

| API | Role |
|-----|------|
| **`askcolor(color=None, **options)`** | Show dialog; return selected color or `None` |
| **`Chooser(master=None, **options)`** | Class-based dialog; call **`show()`** |

Return value of **`askcolor()`**: a tuple **`(color, hex_string)`** when the user picks a color—e.g. **`((255, 0, 0), '#ff0000')`**—or **`(None, None)`** on cancel.

---

### askcolor — [askcolor](https://docs.python.org/3/library/tkinter.colorchooser.html#tkinter.colorchooser.askcolor)

| Option | Effect |
|--------|--------|
| **`color`** | Initial color (name or `#rrggbb`) |
| **`parent`** | Logical parent window (dialog stays on top) |
| **`title`** | Dialog window title |

```python
# Goal: interpret askcolor return values without opening a dialog
def parse_askcolor_result(result):
    rgb, hex_value = result
    if rgb is None:
        return None
    r, g, b = rgb
    assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255
    return hex_value

picked = parse_askcolor_result(((255, 128, 0), "#ff8000"))
assert picked == "#ff8000"
cancelled = parse_askcolor_result((None, None))
assert cancelled is None
```

```python
# Goal: typical usage (illustrative — requires tkinter + display)
# from tkinter import Tk
# from tkinter.colorchooser import askcolor
# root = Tk()
# root.withdraw()
# result = askcolor(parent=root, title="Pick a highlight color")
# if result[0] is not None:
#     rgb, hex_color = result
# root.destroy()
assert True
```

---

### Chooser class — [Chooser](https://docs.python.org/3/library/tkinter.colorchooser.html#tkinter.colorchooser.Chooser)

Inherits from **`tkinter.commondialog.Dialog`**. Instantiate with a **`master`**, then **`show()`** blocks until the user selects or cancels—same pattern as other commondialog subclasses.

---

## Best practices

| Practice | Why |
|----------|-----|
| Pass **`parent=root`** | Keeps dialog above your application window |
| Handle **`(None, None)`** | User cancelled—do not treat as an error |
| Store **hex strings** for persistence | Portable across sessions; convert to RGB when needed |
| **`withdraw()`** the root for picker-only flows | Avoid flashing an empty main window |

---

## See also

- [Tkinter Dialogs](../tkinter-dialogs/index.md) — `commondialog` base and file dialogs
- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — root window and event loop
