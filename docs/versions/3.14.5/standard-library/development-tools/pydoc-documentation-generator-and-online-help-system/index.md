# [pydoc — Documentation generator and online help system](https://docs.python.org/3/library/pydoc.html)

`pydoc` generates **plain-text and HTML documentation** from live objects via introspection (`inspect`, `docstrings`). The built-in [`help()`](https://docs.python.org/3/library/functions.html#help) function delegates to it. The **`pydoc`** CLI can serve a local browser UI or render module pages to stdout. Canonical reference: [pydoc.html](https://docs.python.org/3/library/pydoc.html).

---

## Purpose

Use `pydoc` when you need **quick API reference** without building Sphinx docs: browse modules interactively, search by keyword, or dump a text page for a single object. It reads `__doc__` strings and signature information; it does not execute doctest blocks.

---

## API overview

| Entry point | Behavior |
|-------------|----------|
| `help(obj)` | Interactive pager in REPL; text summary in non-interactive contexts |
| `pydoc.render_doc(thing, renderer=pydoc.plaintext)` | Return formatted doc string |
| `pydoc.locate(path)` | Resolve `"pkg.mod.Class"` to an object |
| `pydoc.cli()` | Command-line interface (`python -m pydoc`) |

---

## Example — render plaintext documentation

```python
import pydoc
import io

def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b

text = pydoc.render_doc(add, renderer=pydoc.plaintext)
assert "add(" in text
assert "sum of two integers" in text
```

---

## Example — locate an object by dotted path

```python
import pydoc

path = pydoc.locate("collections.defaultdict")
from collections import defaultdict
assert path is defaultdict
```

---

## CLI usage (interactive session)

These commands are meant for a terminal, not `exec` blocks:

| Command | Effect |
|---------|--------|
| `python -m pydoc json` | Show module help |
| `python -m pydoc -k socket` | Keyword search across modules |
| `python -m pydoc -b` | Start browser server on an ephemeral port |

---

## Best practices

| Practice | Why |
|----------|-----|
| Write clear **one-line summaries** as the first docstring line | `pydoc` and `help()` lead with that line |
| Document parameters in **Google/NumPy/reST** style consistently | Renderers show raw docstrings unless you use Sphinx |
| Prefer **`python -m pydoc`** over importing private `pydoc` helpers | Public API is stable; internals may shift |
| Do not expose `pydoc` server on untrusted networks | `-b` serves arbitrary module introspection locally |

---

## See also

- [`inspect`](https://docs.python.org/3/library/inspect.html) — lower-level introspection
- [`doctest`](../doctest-test-interactive-python-examples/index.md) — executable examples in docstrings
