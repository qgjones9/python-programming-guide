# [tkinter.font — Tkinter font wrapper](https://docs.python.org/3/library/tkinter.font.html)

**`tkinter.font`** provides the **`Font`** class for creating and querying **named fonts** in Tk. Named fonts are reusable objects referenced by widgets instead of repeating family/size/weight tuples. Canonical docs: [tkinter.font.html](https://docs.python.org/3/library/tkinter.font.html).

---

## Weight and slant constants

| Constant | Meaning |
|----------|---------|
| **`NORMAL`** | Regular weight |
| **`BOLD`** | Bold weight |
| **`ITALIC`** | Italic slant |
| **`ROMAN`** | Upright (non-italic) slant |

---

### Font class — [Font](https://docs.python.org/3/library/tkinter.font.html#tkinter.font.Font)

Construction patterns:

| Argument | Role |
|----------|------|
| **`font=(family, size, options)`** | One-shot specifier tuple |
| **`name="MyFont"`** | Register a named font in Tk |
| **`exists=True`** | Bind to an already-defined named font |
| **`family`, `size`, `weight`, `slant`, `underline`, `overstrike`** | Keyword options when `font=` omitted |

**Size semantics:** positive **`size`** is points; negative absolute value is pixels.

| Method | Returns |
|--------|---------|
| **`actual(option=None)`** | Resolved font attributes |
| **`cget(option)`** | Single attribute |
| **`config(**options)`** | Update attributes |
| **`copy()`** | Duplicate font object |
| **`measure(text)`** | Pixel width of `text` in this font |
| **`metrics(...)`** | ascent, descent, linespace, fixed-width flag |

```python
# Goal: build a font specifier tuple the way tkinter.font expects
family, size = "Courier", 12
options = ("bold", "italic")
font_tuple = (family, size, " ".join(options))
assert font_tuple[0] == "Courier" and font_tuple[1] == 12
assert "bold" in font_tuple[2]
```

```python
# Goal: measure text width (illustrative — requires tkinter + display)
# from tkinter import Tk
# from tkinter import font
# root = Tk()
# root.withdraw()
# f = font.Font(family="Helvetica", size=14, weight=font.BOLD)
# width = f.measure("Hello")
# assert width > 0
# root.destroy()
assert True
```

---

### Module-level helpers

| Function | Purpose |
|----------|---------|
| **`families(root=None)`** | List font families available on the display |
| **`names(root=None)`** | List defined named fonts |
| **`nametofont(name, root=None)`** | `Font` wrapper for an existing Tk font name (since 3.10: optional **`root`**) |

---

## Best practices

| Practice | Why |
|----------|-----|
| Reuse **`Font`** objects | Avoid duplicate Tcl font registrations |
| Call **`measure()`** before truncating labels | Prevents clipped text in fixed-width columns |
| Prefer **named fonts** in ttk **`Style`** | Consistent typography across themed widgets |
| Check **`metrics("fixed")`** | Detect monospace fonts for column alignment |

---

## See also

- [`tkinter.ttk`](../tkinterttk-tk-themed-widgets/index.md) — style fonts via `ttk.Style`
- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — widget `font=` option
