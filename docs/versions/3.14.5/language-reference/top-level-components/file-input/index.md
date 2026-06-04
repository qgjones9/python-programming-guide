# [9.2. File input](https://docs.python.org/3/reference/toplevel_components.html#file-input)

All input read from **non-interactive** files (and equivalent strings) uses the **`file_input`** grammar:

```text
file_input: (NEWLINE | statement)* ENDMARKER
```

That is: zero or more newlines or statements, then end of input. There is no separate “expression-only” top level in this mode—use `eval()` and [expression input](../expression-input/index.md) for that.

---

## Where `file_input` applies

| Situation | Notes |
|-----------|--------|
| Parsing a **complete program** | From a file, `-c`, or non-TTY stdin |
| Parsing a **module** | Import machinery compiles module source with this grammar |
| String passed to **`exec()`** | Must be `file_input` (statements), not a bare expression |

Module bodies, `python script.py`, and `exec(compile(text, ..., "exec"))` all share this production. [`compile()`](https://docs.python.org/3/library/functions.html#compile) with mode `"exec"` expects `file_input`.

```python
# Goal: multi-statement file_input via exec (same as a .py file body)
src = """\
count = 0
for _ in range(3):
    count += 1
"""
ns: dict[str, object] = {}
exec(compile(src, "<file>", "exec"), ns, ns)
assert ns["count"] == 3
```

```python
# Goal: NEWLINE-only lines are allowed in file_input (blank lines between statements)
src = "a = 1\n\nb = 2\n"
ns: dict[str, object] = {}
exec(compile(src, "<file>", "exec"), ns, ns)
assert (ns["a"], ns["b"]) == (1, 2)
```

```python
# Goal: compile(..., "exec") vs eval — exec wants statements
code = compile("x = 4", "<s>", "exec")
ns: dict[str, object] = {}
exec(code, ns, ns)
assert ns["x"] == 4
```

Parent: [9. Top-level components](../index.md)
