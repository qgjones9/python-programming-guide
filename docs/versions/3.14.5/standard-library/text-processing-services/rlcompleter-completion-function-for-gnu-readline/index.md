# [rlcompleter — Completion function for GNU readline](https://docs.python.org/3/library/rlcompleter.html)

[`rlcompleter`](https://docs.python.org/3/library/rlcompleter.html) supplies a **`Completer`** class whose `complete(text, state)` method matches Python **keywords**, **`__main__` globals**, **`builtins`**, and **dotted attribute paths**—the default tab completion for the classic interactive interpreter when [`readline`](../readline-gnu-readline-interface/index.md) is available. Full behavior notes remain on [docs.python.org](https://docs.python.org/3/library/rlcompleter.html).

On Unix with readline present, importing `rlcompleter` installs an instance automatically (unless Python is run with **`-S`**). On platforms without readline, you can still instantiate `Completer` for custom UIs.

---

## Completer.complete(text, state)

Readline calls the completer repeatedly with **`state`** `0`, `1`, `2`, … until the method returns **`None`**.

| `text` shape | Completion source |
|--------------|-------------------|
| No `.` in `text` | Keywords, `__main__` names, builtins |
| Dotted (`obj.attr`) | Safe evaluation of prefix + `dir()` on result |

Evaluation avoids calling functions but may invoke **`__getattr__`** on objects while resolving the prefix. Exceptions during evaluation are suppressed and yield no matches.

```python
# Goal: complete Python keywords from a Completer instance
import rlcompleter

comp = rlcompleter.Completer()
matches = []
state = 0
while True:
    m = comp.complete("wh", state)
    if m is None:
        break
    matches.append(m)
    state += 1
assert any(m.strip() == "while" for m in matches)
```

---

## Dotted completion

For `text` like `"str.up"`, the completer evaluates the expression before the final dot (here `str`) and filters `dir()` results.

```python
# Goal: attribute completion on a builtin type
import rlcompleter

comp = rlcompleter.Completer()
matches = []
state = 0
while True:
    m = comp.complete("str.is", state)
    if m is None:
        break
    matches.append(m)
    state += 1
assert "str.isdigit" in matches or any(x.startswith("str.is") for x in matches)
```

---

## Wiring into readline

Classic REPL setup binds Tab to `complete` and optionally loads history—typically in **`PYTHONSTARTUP`**:

| Step | API |
|------|-----|
| Bind Tab | `readline.parse_and_bind("tab: complete")` |
| Install completer | Automatic on `import rlcompleter`; or `readline.set_completer(Completer().complete)` |
| Delimiters | Default breaks on non-identifier characters; adjust with `set_completer_delims` |

```python
# Goal: explicit readline + Completer wiring
try:
    import readline
    import rlcompleter
except ImportError:
    pass
else:
    readline.parse_and_bind("tab: complete")
    comp = rlcompleter.Completer()
    readline.set_completer(comp.complete)
    assert readline.get_completer() is not None
    readline.set_completer(None)
```

---

## Best practices and pitfalls

| Practice | Why |
|----------|-----|
| Subclass or replace **`set_completer`** for domain commands | Default completer only knows Python symbols |
| Keep **`__main__` namespace tidy** | Completer exposes every global name |
| Avoid side-effect **`__getattr__`** on objects you inspect | Dotted completion may trigger descriptors |
| Use **`-S`** to disable auto-import | Scripts that must not touch readline state |
| Prefer **`PYTHON_BASIC_REPL=1`** when testing readline | 3.13+ default REPL skips readline |

**Pitfall:** `complete` returns **`None`** both when exhausted and when no prefix matches—drive it with incrementing `state`, not by checking for `None` on the first call alone.

```python
# Goal: distinguish no matches vs exhausted iterator
import rlcompleter

comp = rlcompleter.Completer()
first = comp.complete("qqqqqq_not_a_keyword", 0)
assert first is None
assert comp.complete("qqqqqq_not_a_keyword", 1) is None
```

For lower-level completion control (delimiters, display hooks), see [readline — Completion](../readline-gnu-readline-interface/index.md).
