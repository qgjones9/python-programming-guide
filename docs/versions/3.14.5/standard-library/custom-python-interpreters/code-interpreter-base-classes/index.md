# [code — Interpreter base classes](https://docs.python.org/3/library/code.html)

The [`code`](https://docs.python.org/3/library/code.html) module implements building blocks for **interactive Python interpreters**: parsing source, maintaining a user namespace, printing tracebacks, and optionally emulating the standard `>>>` prompt. Use `InteractiveConsole` or `code.interact()` when you want a ready-made loop; subclass `InteractiveInterpreter` when you control input/output yourself. Full method reference remains on [docs.python.org](https://docs.python.org/3/library/code.html).

---

## Classes and convenience API

| Name | Purpose |
|------|---------|
| `InteractiveInterpreter(locals=None)` | Parse and execute in a namespace; no prompting |
| `InteractiveConsole(locals=None, filename='<console>', local_exit=False)` | Adds buffering, `push()`, and `sys.ps1` / `sys.ps2` prompts |
| `interact(banner=None, readfunc=None, local=None, exitmsg=None, local_exit=False)` | One-shot REPL using a new `InteractiveConsole` |
| `compile_command(source, filename='<input>', symbol='single')` | Same incomplete-line logic as the main interpreter (delegates to `codeop`) |

---

## InteractiveInterpreter — [Interactive Interpreter Objects](https://docs.python.org/3/library/code.html#interactive-interpreter-objects)

| Method | Behavior |
|--------|----------|
| `runsource(source, filename='<input>', symbol='single')` | Compile and run; returns `True` if more input needed |
| `runcode(code)` | Execute a code object; catches exceptions except `SystemExit` |
| `showsyntaxerror(filename=None)` | Print syntax error without stack trace |
| `showtraceback()` | Print exception traceback (strips one internal frame) |
| `write(data)` | Default writes to `sys.stderr`; override for custom UIs |

```python
# Goal: run complete source in a fresh console namespace
import code
import io
import sys

buf = io.StringIO()
interp = code.InteractiveInterpreter({"x": 0})
interp.write = buf.write
more = interp.runsource("x = x + 1\n")
assert more is False
assert interp.locals["x"] == 1
```

```python
# Goal: multiline def in one runsource executes completely
import code

interp = code.InteractiveInterpreter()
assert interp.runsource("def f():\n    return 1\n") is False
assert interp.locals["f"]() == 1
```

---

## InteractiveConsole — [Interactive Console Objects](https://docs.python.org/3/library/code.html#interactive-console-objects)

| Method | Purpose |
|--------|---------|
| `interact(banner=None, exitmsg=None)` | Run until EOF; optional banner and exit message |
| `push(line)` | Append a line to the buffer and call `runsource()` on the buffer |
| `resetbuffer()` | Discard buffered incomplete source |
| `raw_input(prompt='')` | Read a line (default: `sys.stdin`); raises `EOFError` on EOF |

```python
# Goal: push() buffers until a blank line completes the compound statement
import code

console = code.InteractiveConsole()
assert console.push("for i in range(2):") is True
assert console.push("    pass") is True
assert console.push("") is False
assert "i" in console.locals
```

---

## `compile_command` shortcut

```python
# Goal: distinguish exec vs eval compilation modes
import code

stmt = code.compile_command("1 + 2", symbol="single")
expr = code.compile_command("1 + 2", symbol="eval")
assert stmt is not None and expr is not None
ns = {}
exec(stmt, ns, ns)
assert eval(expr, ns, ns) == 3
```

---

## Design tips

| Practice | Why |
|----------|-----|
| Override `write()` for GUIs or logging | Default stderr may be wrong for embedded tools |
| Catch `KeyboardInterrupt` at the caller | Not always handled inside `runcode()` |
| Pass explicit `filename` in tracebacks | Parser defaults to `'<input>'` for strings |
| Use `local_exit=True` in embedded apps (3.13+) | Lets users type `exit()` without killing the host process |
