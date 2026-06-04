# [IDLE — Python editor and shell](https://docs.python.org/3/library/idle.html)

**IDLE** (Integrated Development and Learning Environment) is CPython’s bundled editor and interactive Python shell, implemented in the **`idlelib`** package on top of **`tkinter`**. Canonical docs: [idle.html](https://docs.python.org/3/library/idle.html).

IDLE is **optional**—some distributions omit `idlelib` and tkinter together.

---

## Features

| Feature | Benefit |
|---------|---------|
| Cross-platform shell + editor | Same workflow on Windows, macOS, and Unix |
| Syntax colorizing | Keywords, strings, and errors highlighted |
| Multi-window editor | Undo stack (1000 levels), smart indent, call tips, completion |
| Search / replace / grep | Find in file or across directories |
| Debugger | Breakpoints, stepping, namespace inspection |
| Configuration dialogs | Fonts, themes, key bindings |

---

## Window types

| Window | Role |
|--------|------|
| **Shell** | Interactive interpreter; `>>>` prompts |
| **Editor** | `.py` (and text) files; run module with F5 |
| **Output** | Subclass of editor for tools like *Find in Files* |

On Windows/Linux each window has its own menu bar; on macOS one application menu adapts to the focused window.

---

### Menus — [Menus](https://docs.python.org/3/library/idle.html#menus)

Highlights by menu (Shell and Editor unless noted):

| Menu | Notable commands |
|------|------------------|
| **File** | New, Open, Open Module, Recent Files, Module Browser, Path Browser, Save/Save As, Print, Exit |
| **Edit** | Undo/Redo, Cut/Copy/Paste, Find/Replace, Go to Line, Expand Word |
| **Format** (Editor) | Indent region, comment/uncomment, format paragraph |
| **Run** (Editor) | Run module, check module, configure path |
| **Shell** | Restart shell, previous/next history |
| **Debug** | Debugger toggle, stack viewer, breakpoints |
| **Options** | Configure IDLE, code context, zoom height |
| **Window** | Cascade/tile, list open windows |
| **Help** | IDLE help, Python docs |

Calling **`exit()`** or **`close()`** in the Shell closes it; closing the last window quits IDLE.

---

### Startup and code execution — [Startup and Code Execution](https://docs.python.org/3/library/idle.html#startup-and-code-execution)

| Mode | Behavior |
|------|----------|
| **`python -m idlelib`** | Launch IDLE |
| **Run → Run Module** (F5) | Executes editor buffer in a fresh namespace with `__name__ == '__main__'` |
| **Shell input** | Each statement/expression runs interactively; `_` holds last result |

Environment variables and startup files follow normal Python rules; IDLE adds GUI-specific config under **`~/.idlerc/`** (options, key bindings, themes).

```python
# Goal: detect whether idlelib is available in this interpreter
import importlib.util

spec = importlib.util.find_spec("idlelib")
idle_available = spec is not None
# idle_available is False when idlelib is not packaged (common on minimal Linux builds)
assert isinstance(idle_available, bool)
```

```python
# Goal: launch IDLE from the command line (illustrative — requires idlelib + tkinter)
# python -m idlelib
# python -m idlelib path/to/script.py  # open file in editor
assert True
```

---

## Configuration tips

| Setting | Location / note |
|---------|-------------------|
| Theme and font | Options → Configure IDLE → Highlights / Fonts |
| Initial window size | General tab |
| Autocomplete | Extensions tab; `AutoComplete` extension |
| Path for imports | Run → Configure … → General → `sys.path` |

---

## Best practices

| Practice | Why |
|----------|-----|
| Use IDLE for **learning and quick scripts** | Zero setup beyond stdlib |
| Switch to a full IDE for **large projects** | IDLE lacks project tooling |
| **Restart shell** after reloading changed modules | Avoid stale imports |
| Save before **Run Module** | Unsaved buffers use a temp file name in tracebacks |
| Prefer **`python -m idlelib`** over platform shortcuts | Ensures matching interpreter version |

---

## See also

- [`tkinter`](../tkinter-python-interface-to-tcltk/index.md) — GUI toolkit underlying IDLE
- [Graphical user interfaces with Tk](../index.md) — section hub
