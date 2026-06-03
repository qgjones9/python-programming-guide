# [ascii()](https://docs.python.org/3/library/functions.html#ascii)

## Description

`ascii()` behaves like `repr()` but escapes non-ASCII characters using `\x`, `\u`, or `\U` escapes so the result is safe for ASCII-only environments (similar to Python 2 `repr` for strings).

## What problem it solves

Logs, debug consoles, and protocols limited to ASCII need a readable yet transport-safe representation of arbitrary objects—especially strings containing emoji or accented characters. `ascii()` guarantees the output fits in ASCII.

## Implementation options

### Escaping non-ASCII text

```python
text = "café ☕"
assert ascii(text) == "'caf\\xe9 \\u2615'"
assert repr(text) == "'café ☕'"  # repr keeps Unicode literals
```

### Inspecting arbitrary objects

```python
data = {"label": "über"}
shown = ascii(data)
assert "\\xfc" in shown or "\\u" in shown  # non-ASCII escaped in output
assert isinstance(shown, str)
assert all(ord(c) < 128 for c in shown)
```

## Best practices

- Use `repr()` when you want human-readable Unicode in the REPL; use `ascii()` for ASCII-only logs or wire formats.
- Do not confuse `ascii()` with encoding: it returns a `str` display form, not `bytes`.
- For production logging of user content, still apply redaction policies—`ascii()` only solves character-set safety.
