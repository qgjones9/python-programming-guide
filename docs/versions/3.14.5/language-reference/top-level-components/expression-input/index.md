# [9.4. Expression input](https://docs.python.org/3/reference/toplevel_components.html#expression-input)

[`eval()`](https://docs.python.org/3/library/functions.html#eval) parses its string argument as **`eval_input`**:

```text
eval_input: expression_list NEWLINE* ENDMARKER
```

Leading whitespace is ignored. Unlike [file input](../file-input/index.md), you cannot put statements (`import`, `for`, `def`, …) in an `eval()` string—only an **expression_list** (e.g. a single expression, or a tuple display via comma syntax).

---

## `eval()` vs `exec()`

| API | Input grammar | Typical use |
|-----|---------------|-------------|
| `eval(expr, …)` | `eval_input` | Compute a value from a string |
| `exec(code, …)` | `file_input` | Run statements for side effects |

Use `compile(text, "<name>", "eval")` when you need a code object without calling `eval()` immediately. Mode `"single"` is for interactive display of one expression (REPL echoes the result).

```python
# Goal: eval_input — bare expression
assert eval("3 * 7") == 21
```

```python
# Goal: expression_list — comma builds a tuple display
assert eval("1, 2, 3") == (1, 2, 3)
assert eval("'a', 'b'") == ("a", "b")
```

```python
# Goal: compile(..., "eval") matches eval() grammar
obj = compile("{k: k * 2 for k in range(3)}", "<e>", "eval")
assert eval(obj) == {0: 0, 1: 2, 2: 4}
```

```python
# Goal: eval() cannot parse statements — use exec / file_input instead
try:
    compile("import sys", "<x>", "eval")
except SyntaxError:
    ok = True
else:
    ok = False
assert ok
```

Parent: [9. Top-level components](../index.md)
