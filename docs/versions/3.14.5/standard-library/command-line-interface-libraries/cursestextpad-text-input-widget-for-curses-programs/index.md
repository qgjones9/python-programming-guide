# [curses.textpad — Text input widget for curses programs](https://docs.python.org/3/library/curses.textpad.html)

The [`curses.textpad`](https://docs.python.org/3/library/curses.textpad.html) module provides [`Textbox`](https://docs.python.org/3/library/curses.textpad.html#curses.textpad.Textbox), an **editable text field** inside a curses window with **Emacs-like** key bindings (Ctrl-A beginning of line, Ctrl-K kill, and so on). Use it for forms and prompts in full-screen TUIs built with [`curses`](../curses-terminal-handling-for-character-cell-displays/index.md). Full API remains on [docs.python.org](https://docs.python.org/3/library/curses.textpad.html).

Rendering requires an initialized curses window (typically via `curses.wrapper`); examples below validate the **API surface** and validator contracts without a TTY.

---

## Textbox class

Constructor: `Textbox(win, insert_mode=False, *, max_width=None)`.

| Parameter | Role |
|-----------|------|
| `win` | Curses window containing the edit region |
| `insert_mode` | Insert vs overstrike when typing |
| `max_width` | Limit editable width (keyword-only) |

| Method | Role |
|--------|------|
| `edit(validate=None)` | Run edit loop until Enter; optional per-key validator |
| `do_command(ch)` | Process one keystroke |
| `gather()` | Return window contents as `str` |
| `stripspaces` | Class attribute: strip trailing spaces on gather (default `True`) |

```python
# Goal: Textbox class exposes edit/gather and constructor parameters
import curses.textpad as textpad
import inspect

assert hasattr(textpad, "Textbox")
tb = textpad.Textbox
assert callable(getattr(tb, "edit", None))
assert callable(getattr(tb, "gather", None))
assert "win" in inspect.signature(tb.__init__).parameters
```

---

## Edit loop and validation

Pass `validate=callable` to `edit()` to accept or reject keys before they are applied. Return `0` to reject, non-zero to accept.

```python
# Goal: validator accepts digits and Enter, rejects other keys
import curses.textpad as textpad

def digits_only(ch):
    if ch == 10:  # Enter
        return 1
    return ch in (ord(c) for c in "0123456789")

assert digits_only(ord("5")) == 1
assert digits_only(ord("x")) == 0
assert callable(textpad.Textbox.edit)
```

---

## Typical usage pattern (interactive)

In a real app inside `curses.wrapper`:

1. Create a subwindow for the field.
2. `box = textpad.Textbox(subwin)`.
3. `box.edit()` blocks until the user presses Enter.
4. `value = box.gather().strip()`.

---

## Emacs-like bindings (reference)

| Key | Action |
|-----|--------|
| Ctrl-A | Beginning of line |
| Ctrl-E | End of line |
| Ctrl-B / Ctrl-F | Back / forward char |
| Ctrl-H / Backspace | Delete left |
| Ctrl-D | Delete under cursor |
| Ctrl-K | Kill to end of line |
| Ctrl-L | Refresh |
| Enter | End editing |

Exact behavior depends on terminal key encoding; use `keypad(True)` on the parent window.

---

## Related modules

| Module | Use |
|--------|-----|
| [`curses`](../curses-terminal-handling-for-character-cell-displays/index.md) | Screen setup, subwindows, colors |
| [`curses.ascii`](../cursesascii-utilities-for-ascii-characters/index.md) | Classify control characters in validators |
| [`readline`](../../text-processing-services/readline-gnu-readline-interface/index.md) | Line editing for non-curses CLIs |
