# [codeop — Compile Python code](https://docs.python.org/3/library/codeop.html)

The [`codeop`](https://docs.python.org/3/library/codeop.html) module supports **incremental compilation** for REPL-style input: given a string (possibly built from several lines), it tells you whether the text is valid Python, incomplete (need more lines), or invalid. It also provides `Compile` and `CommandCompiler` classes that **remember `__future__` imports** across subsequent compilations. Most programs should use [`code`](../code-interpreter-base-classes/index.md) instead of calling `codeop` directly. Full API reference remains on [docs.python.org](https://docs.python.org/3/library/codeop.html).

---

## `compile_command` — [codeop.compile_command](https://docs.python.org/3/library/codeop.html#codeop.compile_command)

| Return value | Meaning |
|--------------|---------|
| `code` object | Complete, valid source (same as `compile()`) |
| `None` | Valid **prefix** — user should enter more lines |
| `SyntaxError` raised | Complete but syntactically invalid |
| `OverflowError` / `ValueError` | Invalid literal in otherwise complete source |

| Parameter | Values |
|-----------|--------|
| `symbol` | `'single'` (default, one statement), `'exec'` (sequence), `'eval'` (expression) |
| `filename` | Stored on the code object; default `'<input>'` |

```python
# Goal: None means "need another line"
import codeop

assert codeop.compile_command("class C:") is None
complete = codeop.compile_command("class C:\n    pass\n")
assert complete is not None
```

```python
# Goal: symbol='eval' for expressions only
import codeop

co = codeop.compile_command("len('hi')", symbol="eval")
assert co is not None
assert eval(co) == 2
```

```python
# Goal: invalid syntax raises SyntaxError
import codeop

try:
    codeop.compile_command("def (")
except SyntaxError:
    pass
else:
    raise AssertionError("expected SyntaxError")
```

---

## Stateful compilers — [Compile and CommandCompiler](https://docs.python.org/3/library/codeop.html#codeop.Compile)

| Class | `__call__` signature | Remembers `__future__` |
|-------|----------------------|-------------------------|
| `codeop.Compile` | Like built-in `compile()` | Yes |
| `codeop.CommandCompiler` | Like `compile_command()` | Yes |

After the user enters `from __future__ import annotations`, a `Compile` instance applies that feature to later compilations without re-parsing the future import each time.

```python
# Goal: CommandCompiler chains future-aware partial input
import codeop

cc = codeop.CommandCompiler()
first = cc("from __future__ import annotations\n")
assert first is not None  # future import is a complete statement
second = cc("def f() -> int:\n    return 1\n", symbol="exec")
assert second is not None
ns = {}
exec(second, ns, ns)
assert ns["f"]() == 1
```

---

## Relationship to `code`

| Layer | Module |
|-------|--------|
| REPL classes, tracebacks, buffering | `code` |
| Incomplete-line detection, future-aware compile | `codeop` |

`code.compile_command` is a thin wrapper around `codeop.compile_command` for convenience.

---

## Pitfalls

| Pitfall | Detail |
|---------|--------|
| Trailing garbage after valid prefix | Parser may accept a prefix and ignore trailing tokens in rare cases; treat as upstream quirk |
| Wrong `symbol` for input | `'eval'` rejects statements; `'single'` rejects bare expressions in some cases |
| Using `codeop` without `code` | You must implement prompting (`>>>` vs `...`) yourself when `compile_command` returns `None` |
