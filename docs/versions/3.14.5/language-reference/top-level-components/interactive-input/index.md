# [9.3. Interactive input](https://docs.python.org/3/reference/toplevel_components.html#interactive-input)

When Python runs on a **TTY** (typical REPL), input is parsed with **`interactive_input`**, not `file_input`:

```text
interactive_input: [stmt_list] NEWLINE | compound_stmt NEWLINE | ENDMARKER
```

Each prompt delivers **at most one** simple statement list or **one** compound statement, then a newline. The initial environment matches a [complete program](../complete-python-programs/index.md): names you bind at the prompt live in `__main__`.

---

## REPL vs script parsing

| Aspect | Interactive (`interactive_input`) | File (`file_input`) |
|--------|-----------------------------------|---------------------|
| Unit per read | One statement (or compound stmt) | Whole file until EOF |
| Compound `if` / `for` / `try` / … | Must be followed by an **extra blank line** | Block ends at dedent; no blank line required |
| End of input | `ENDMARKER` after each logical line group | `ENDMARKER` at EOF |

The extra blank line after a **top-level** compound statement lets the parser know the block is finished—otherwise the REPL would wait forever for more indented lines. This is why, after typing `for i in range(2):` and the loop body, you press **Enter on an empty line** before the next prompt.

```python
# Goal: a compound statement as one logical unit (file_input simulates "one submission")
block = """\
total = 0
for n in (1, 2, 3):
    total += n
"""
ns: dict[str, object] = {}
exec(compile(block, "<repl-block>", "exec"), ns, ns)
assert ns["total"] == 6
```

```python
# Goal: stmt_list — several simple statements on one interactive "line" (semicolon-separated)
# In the REPL you can type: x = 1; y = x + 1
ns: dict[str, object] = {}
exec(compile("x = 1; y = x + 1", "<stmt_list>", "exec"), ns, ns)
assert ns["y"] == 2
```

Parent: [9. Top-level components](../index.md)
