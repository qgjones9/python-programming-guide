# [readline — GNU readline interface](https://docs.python.org/3/library/readline.html)

The [`readline`](https://docs.python.org/3/library/readline.html) module wraps **GNU Readline** (or **libedit** on some platforms) for line editing, persistent history, and programmable tab completion. It affects the interactive interpreter prompt and any code using built-in [`input()`](https://docs.python.org/3/library/functions.html#input) when readline is linked. Full API remains on [docs.python.org](https://docs.python.org/3/library/readline.html).

**Availability:** not supported on Android, iOS, or WASI. The module is optional in some builds—import defensively in portable tools. On macOS, `readline.backend` (`"readline"` or `"editline"`) selects which library is active (3.13+).

**Note:** Python 3.13’s default REPL does not use readline unless **`PYTHON_BASIC_REPL`** enables the classic interactive shell.

---

## Configuration and backend

| Item | Role |
|------|------|
| `~/.inputrc` | GNU readline init file (key bindings) |
| `~/.editrc` | libedit configuration on macOS |
| `readline.parse_and_bind(string)` | Execute an init line programmatically |
| `readline.read_init_file([filename])` | Load an init file |
| `readline.backend` | `"readline"` or `"editline"` |

```python
# Goal: programmatic tab binding (when readline is present)
try:
    import readline
except ImportError:
    pass
else:
    readline.parse_and_bind("tab: complete")
    if hasattr(readline, "backend"):
        assert readline.backend in ("readline", "editline")
```

---

## Line buffer

| Function | Role |
|----------|------|
| `get_line_buffer()` | Current editable line text |
| `insert_text(string)` | Insert at cursor |
| `redisplay()` | Refresh screen from buffer |

```python
# Goal: manipulate the line buffer without a TTY
try:
    import readline
except ImportError:
    pass
else:
    readline.insert_text("print('hi')")
    buf = readline.get_line_buffer()
    assert "print('hi')" in buf
    readline.insert_text("")  # reset not required for assert-only demo
```

---

## History

| Function | Role |
|----------|------|
| `add_history(line)` | Append a line to in-memory history |
| `get_history_item(index)` | 1-based fetch |
| `remove_history_item(pos)` | Delete by 0-based position |
| `replace_history_item(pos, line)` | Replace entry |
| `clear_history()` | Empty history (if supported) |
| `get_current_history_length()` | Count of stored entries |
| `read_history_file` / `write_history_file` | Load/save `~/.history` by default |
| `append_history_file(n, file)` | Append last *n* entries (3.5+) |
| `set_history_length` / `get_history_length` | Cap persisted size |
| `set_auto_history(enabled)` | Auto-add lines from `input()` (3.6+) |

```python
# Goal: in-memory history without touching ~/.history
try:
    import readline
except ImportError:
    pass
else:
    start = readline.get_current_history_length()
    readline.add_history("x = 1")
    readline.add_history("y = 2")
    assert readline.get_history_item(start + 1) == "x = 1"
    assert readline.get_history_item(start + 2) == "y = 2"
```

---

## Completion hooks

| Function | Role |
|----------|------|
| `set_completer(func)` | `func(text, state)` returns next match or `None` |
| `get_completer()` | Current completer callable |
| `set_completer_delims(string)` | Characters that break words |
| `get_completer_delims()` | Current delimiter set |
| `get_begidx()` / `get_endidx()` | Completion span in buffer |
| `set_completion_display_matches_hook(func)` | Custom match listing |

Pair with [`rlcompleter`](../rlcompleter-completion-function-for-gnu-readline/index.md) for Python identifier completion at the REPL.

```python
# Goal: minimal word completer
try:
    import readline
except ImportError:
    pass
else:
    words = ["alpha", "alphabet", "beta"]

    def completer(text, state):
        matches = [w for w in words if w.startswith(text)]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)
    assert readline.get_completer()( "al", 0) == "alpha"
    assert readline.get_completer()( "al", 1) == "alphabet"
    readline.set_completer(None)
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Guard **`import readline`** | Missing on mobile/WASI and some embed builds |
| Cap history with **`set_history_length`** | Avoid unbounded `~/.history` growth |
| Use **`append_history_file`** for concurrent sessions | Reduces overwrite races vs full rewrite |
| Register **`atexit`** handlers to persist history | Pattern shown in upstream docs |
| Set **`PYTHONSTARTUP`** for shared config | Central place for parse/bind and history load |

**Pitfalls:**

- libedit vs GNU readline use **different config files** and history formats.
- Completion indices (`get_begidx` / `get_endidx`) may differ between backends.
- Auditing events on history file I/O were added in 3.14—security tools may log those paths.

For a persistent-history template, see upstream [Example](https://docs.python.org/3/library/readline.html#example) (`~/.python_history` with `atexit`).
