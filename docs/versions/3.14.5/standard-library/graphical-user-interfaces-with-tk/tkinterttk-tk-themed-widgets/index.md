# [tkinter.ttk — Tk themed widgets](https://docs.python.org/3/library/tkinter.ttk.html)

**`tkinter.ttk`** exposes Tk **8.5+ themed widgets**—separating behavior from appearance so apps pick up native styling on Windows, macOS, and X11 (with anti-aliased fonts where supported). Canonical docs: [tkinter.ttk.html](https://docs.python.org/3/library/tkinter.ttk.html).

Import after classic tkinter when you want ttk names to override defaults:

```python
# Goal: import order when replacing classic widgets (illustrative)
# from tkinter import *
# from tkinter.ttk import *  # Button, Label, Frame, … now themed
assert True
```

---

## Widget set

| Widget | Notes |
|--------|-------|
| **Replaced classics** | `Button`, `Checkbutton`, `Entry`, `Frame`, `Label`, `LabelFrame`, `Menubutton`, `PanedWindow`, `Radiobutton`, `Scale`, `Scrollbar`, `Spinbox` |
| **New in ttk** | `Combobox`, `Notebook`, `Progressbar`, `Separator`, `Sizegrip`, `Treeview` |

All inherit from **`ttk.Widget`**. Styling uses **`ttk.Style`**, not per-widget **`fg`/`bg`**.

---

### Using Ttk — [Using Ttk](https://docs.python.org/3/library/tkinter.ttk.html#using-ttk)

Classic vs themed styling:

| Classic `tkinter` | Themed `ttk` |
|-------------------|--------------|
| `Label(text="Test", fg="black", bg="white")` | `Style().configure("BW.TLabel", foreground="black", background="white")` then `Label(text="Test", style="BW.TLabel")` |

Each extra widget with the same look reuses the **style name**, not duplicate color kwargs.

```python
# Goal: encode a ttk style map entry (pure data structure)
style_config = {"BW.TLabel": {"foreground": "black", "background": "white"}}
entry = style_config["BW.TLabel"]
assert entry["foreground"] == "black"
```

---

### Standard options — [Standard Options](https://docs.python.org/3/library/tkinter.ttk.html#standard-options)

| Option | Role |
|--------|------|
| **`class`** | Window class for option database and default layout (read-only after create) |
| **`cursor`** | Mouse cursor; empty string inherits from parent |
| **`takefocus`** | `0`, `1`, or `""` for keyboard traversal |
| **`style`** | Named custom style (e.g. `"BW.TLabel"`) |

Scrollable widgets add **`xscrollcommand`** / **`yscrollcommand`**. Label-like widgets add **`text`**, **`textvariable`**, **`image`**, **`compound`**, **`underline`**.

---

### Style class — [Style](https://docs.python.org/3/library/tkinter.ttk.html#style)

Central styling API:

| Method | Purpose |
|--------|---------|
| **`configure(style, **kw)`** | Set default option values for a style |
| **`map(style, **kw)`** | State-dependent options (e.g. `[("active", "blue")]`) |
| **`layout(style)`** | Element layout for the style |
| **`theme_names()`**, **`theme_use(name)`** | List/activate platform themes (`clam`, `alt`, `default`, …) |

```python
# Goal: build state map tuples as ttk.Style.map expects
foreground_map = [("disabled", "gray"), ("active", "blue")]
states = [pair[0] for pair in foreground_map]
assert states == ["disabled", "active"]
```

---

### Widget reference highlights

| Widget | Typical use |
|--------|-------------|
| **`Notebook`** | Tabbed panels |
| **`Treeview`** | Tables and tree lists (`heading`, `column`, `insert`) |
| **`Progressbar`** | Determinate/indeterminate progress |
| **`Combobox`** | Editable dropdown |
| **`Separator`** | Visual divider |
| **`Sizegrip`** | Resize handle for windows |

Each supports **`identify`**, **`instate`**, and state flags like **`disabled`**, **`active`**, **`selected`**.

---

### ttk Widget base — [Widget](https://docs.python.org/3/library/tkinter.ttk.html#widget)

Shared methods include **`instate(statespec, callback=None)`**, **`state(statespec=None)`**, and **`identify(...)`** for hit-testing elements. Do not instantiate **`Widget`** directly.

```python
# Goal: minimal ttk notebook tab model (illustrative — requires tkinter)
# from tkinter import Tk
# from tkinter import ttk
# root = Tk()
# nb = ttk.Notebook(root)
# nb.pack(fill="both", expand=True)
# tab1 = ttk.Frame(nb)
# nb.add(tab1, text="First")
# nb.add(ttk.Frame(nb), text="Second")
# root.destroy()
assert True
```

---

## Best practices

| Practice | Why |
|----------|-----|
| Use **`ttk` for all new widgets** | Consistent cross-platform appearance |
| Centralize colors in **`Style`** | One place to theme the whole app |
| Call **`theme_use()`** early | Before constructing widgets |
| Read **Tile migration notes** when porting old tk apps | Option names differ from classic widgets |
| Pair **`Treeview`** with **`Scrollbar`** via **`yscrollcommand`** | Same pattern as classic widgets |

---

## See also

- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — geometry managers and event loop
- [Graphical user interfaces with Tk](../index.md) — section hub
