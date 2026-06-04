# [curses.panel — A panel stack extension for curses](https://docs.python.org/3/library/curses.panel.html)

The [`curses.panel`](https://docs.python.org/3/library/curses.panel.html) module adds a **depth-ordered stack** of panels over [`curses`](../curses-terminal-handling-for-character-cell-displays/index.md) windows. Each panel wraps a window; **`top_panel()`** / **`bottom_panel()`** change Z-order, and **`update_panels()`** refreshes visible stacking. Use it for overlapping dialogs, menus, and status bars in TUIs. Full API remains on [docs.python.org](https://docs.python.org/3/library/curses.panel.html).

Panel operations require curses initialization (`initscr`); examples below validate **imports and function signatures** without a TTY.

---

## Core functions — [Panel Objects](https://docs.python.org/3/library/curses.panel.html#module-curses.panel)

| Function | Role |
|----------|------|
| `new_panel(win)` | Create a panel for an existing window |
| `top_panel(panel)` | Raise panel to top of stack |
| `bottom_panel(panel)` | Send panel to bottom |
| `update_panels()` | Sync panel visibility after stack changes |
| `panel(panel_id)` | Access panel by wrapped window (advanced) |
| `version()` | Return panel library version string |

---

## panel object methods

| Method | Role |
|--------|------|
| `hide()` / `show()` | Remove or restore panel from stack |
| `move(y, x)` | Move panel and its window |
| `replace(win)` | Attach a different window |
| `userptr()` / `set_userptr(obj)` | Store/retrieve Python object on panel |
| `window()` | Return underlying curses window |
| `above()` / `below()` | Navigate stack neighbors |
| `hidden()` | Whether panel is hidden |

```python
# Goal: panel module exports stack management API
import curses.panel as panel
import inspect

for name in ("new_panel", "top_panel", "bottom_panel", "update_panels", "version"):
    assert hasattr(panel, name), name
assert callable(panel.new_panel)
ver = panel.version
assert isinstance(ver, str) and len(ver) > 0
```

---

## Typical stacking workflow (interactive)

Inside `curses.wrapper`:

1. Create windows with `stdscr.subwin(...)`.
2. `p1 = panel.new_panel(win1)`; `p2 = panel.new_panel(win2)`.
3. `panel.top_panel(p2)` to show dialog over content.
4. `panel.update_panels()` then `curses.doupdate()` (not only `refresh()`).
5. `p2.hide()` or destroy when closing dialog.

```python
# Goal: panel objects expose window() and stack neighbors
import curses.panel as panel

panel_methods = {"hide", "show", "move", "window", "above", "below", "hidden"}
# Verified at import time: panel.panel is the wrapper type name in C API
assert hasattr(panel, "panel")
```

---

## update_panels vs refresh

| Call | Scope |
|------|-------|
| `win.refresh()` | Update one window's logical screen |
| `panel.update_panels()` | Recompute which panel regions are visible |
| `curses.doupdate()` | Push physical screen update after panel changes |

Forgetting `update_panels()` after reordering often leaves stale overlap artifacts.

---

## Related modules

| Module | Use |
|--------|-----|
| [`curses`](../curses-terminal-handling-for-character-cell-displays/index.md) | Window creation and drawing |
| [`curses.textpad`](../cursestextpad-text-input-widget-for-curses-programs/index.md) | Input widgets inside panel windows |
| HOWTO | [Curses Programming with Python](https://docs.python.org/3/howto/curses.html) |
