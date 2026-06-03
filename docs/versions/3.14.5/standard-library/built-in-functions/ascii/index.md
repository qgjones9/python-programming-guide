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

### Numbers and nested structures

```python
assert ascii(42) == "42"
nested = ascii([1, "naïve"])
assert "\\xe" in nested or "\\u" in nested  # non-ASCII in nested str escaped
```

## Best practices

- Use `repr()` when you want human-readable Unicode in the REPL; use `ascii()` for ASCII-only logs or wire formats.

  ```python
  text = "café ☕"
  assert repr(text) == "'café ☕'"
  assert ascii(text) == "'caf\\xe9 \\u2615'"
  assert all(ord(c) < 128 for c in ascii(text))
  ```

- Do not confuse `ascii()` with encoding: it returns a display `str`, not `bytes`.

  ```python
  label = "über"
  shown = ascii(label)
  assert isinstance(shown, str)
  # Incorrect: ascii(label).encode()  # double step; encode explicitly when you need bytes
  wire = label.encode("ascii", errors="backslashreplace")
  assert isinstance(wire, bytes)
  ```

- For production logging of user content, still apply redaction policies—`ascii()` only solves character-set safety.

  ```python
  user_input = "secret-token-42 ☕"
  safe_for_log = ascii(user_input)  # ASCII-safe, not redacted
  assert "secret" in safe_for_log  # still contains the secret — mask separately
  ```
