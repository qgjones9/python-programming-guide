# [curses — Terminal handling for character-cell displays](https://docs.python.org/3/library/curses.html)

The [`curses`](https://docs.python.org/3/library/curses.html) module wraps the **ncurses** library for portable **terminal user interfaces** (TUIs): windows, colors, cursor control, and keyboard input on character-cell displays. Full API and the [Curses Programming with Python](https://docs.python.org/3/howto/curses.html) tutorial remain on [docs.python.org](https://docs.python.org/3/library/curses.html).

**Availability:** not Android, iOS, or WASI. Optional in some builds — import may fail if ncurses is missing.

Submodules: [`curses.ascii`](../cursesascii-utilities-for-ascii-characters/index.md), [`curses.textpad`](../cursestextpad-text-input-widget-for-curses-programs/index.md), [`curses.panel`](../cursespanel-a-panel-stack-extension-for-curses/index.md).

---

## Typical application shape

| Phase | API |
|-------|-----|
| Setup | `curses.wrapper(main)` — init, run, restore terminal |
| Screen | `stdscr = curses.initscr()` inside wrapper |
| Windows | `stdscr.subwin(nlines, ncols, begin_y, begin_x)` |
| Colors | `start_color()`, `init_pair(n, fg, bg)`, `color_pair(n)` |
| Input | `stdscr.getch()`, `keyname()`, `cbreak()` / `raw()` |
| Cleanup | `endwin()` (wrapper handles on exit) |

Most interactive examples require a real TTY; the blocks below validate **constants and imports** that work headless.

---

## Attributes and color constants — [Functions](https://docs.python.org/3/library/curses.html#functions)

| Name | Role |
|------|------|
| `A_BOLD`, `A_UNDERLINE`, `A_REVERSE`, … | Text attributes OR’d into `addstr` |
| `COLOR_BLACK` … `COLOR_WHITE` | Color indices for `init_pair` |
| `ACS_HLINE`, `ACS_VLINE`, … | Line-drawing chars (need initscr to render) |
| `LINES`, `COLS` | Terminal size (valid after init) |
| `curses.error` | Raised on ncurses failures |

```python
# Goal: module-level color and attribute constants (no TTY)
import curses

assert curses.COLOR_BLACK == 0
assert curses.COLOR_RED == 1
assert curses.A_BOLD != 0
assert curses.A_NORMAL == 0
assert issubclass(curses.error, Exception)
```

---

## wrapper() pattern

[`curses.wrapper(func)`](https://docs.python.org/3/library/curses.html#curses.wrapper) initializes curses, calls `func(stdscr)`, and restores the terminal even on exceptions.

```python
# Goal: document wrapper signature without requiring a TTY in CI
import curses
import inspect

sig = inspect.signature(curses.wrapper)
assert "func" in sig.parameters
# Apps define: def main(stdscr): stdscr.addstr(0, 0, "Hi"); stdscr.refresh()
```

---

## Input and terminal modes

| Mode | Function | Effect |
|------|----------|--------|
| Cbreak | `cbreak()` | Character-at-a-time input; signals still work |
| Raw | `raw()` | Like cbreak but disables signal processing |
| No echo | `noecho()` | Typed keys not shown |
| Keypad | `keypad(True)` | Decode function keys to `curses.KEY_*` |
| Timeout | `timeout(ms)` | `-1` block, `0` non-blocking, `>0` ms wait |

```python
# Goal: KEY_* constants exist for keypad decoding
import curses

assert curses.KEY_UP != curses.KEY_DOWN
assert curses.KEY_ENTER != curses.KEY_BACKSPACE
```

---

## Windows and drawing

| Method (on window) | Role |
|--------------------|------|
| `addstr(y, x, text, attr=0)` | Write text with optional attributes |
| `move(y, x)` | Move cursor |
| `refresh()` | Push window to screen |
| `getmaxyx()` / `getyx()` | Size and cursor position |
| `border()` / `box()` | Draw borders |

Interactive drawing requires `initscr()`; structure tests only:

```python
# Goal: Window class documents core methods
import curses

methods = {"addstr", "refresh", "getch", "subwin", "box"}
assert methods.issubset(dir(curses.window))
```

---

## 3.14: assume_default_colors

[`assume_default_colors(fg, bg)`](https://docs.python.org/3/library/curses.html#curses.assume_default_colors) (3.14+) maps terminal default fg/bg to color `-1` for transparency-friendly themes.

---

## Related documentation

| Resource | Link |
|----------|------|
| HOWTO tutorial | [Curses Programming with Python](https://docs.python.org/3/howto/curses.html) |
| ASCII helpers | [`curses.ascii`](../cursesascii-utilities-for-ascii-characters/index.md) |
| Text fields | [`curses.textpad`](../cursestextpad-text-input-widget-for-curses-programs/index.md) |
| Z-order panels | [`curses.panel`](../cursespanel-a-panel-stack-extension-for-curses/index.md) |
