# [compile()](https://docs.python.org/3/library/functions.html#compile)

## Description

`compile()` compiles source code into a code object (or AST, depending on flags) that you run with `exec()` or `eval()`. The `mode` argument must be `'exec'`, `'eval'`, or `'single'`.

## What problem it solves

Dynamic code—REPLs, DSLs, templating, or cached bytecode—needs a compile step separate from execution. `compile()` attaches a filename for tracebacks and lets you control optimization and future imports via flags.

## Implementation options

### Compile and execute statements

```python
source = "result = 2 + 2"
code = compile(source, "<string>", "exec")
ns = {}
exec(code, ns, ns)
assert ns["result"] == 4
```

### Single-expression mode for eval

```python
expr = compile("3 * 7", "<expr>", "eval")
assert eval(expr) == 21
```

### `single` mode for one interactive statement

```python
code = compile("x = 40 + 2\n", "<stdin>", "single")
ns = {}
exec(code, ns)
assert ns["x"] == 42
```

### Future imports via compile flags

```python
from __future__ import annotations

source = "def f() -> int: return 1"
code = compile(source, "<mod>", "exec")
ns = {}
exec(code, ns)
assert ns["f"]() == 1
```

## Best practices

- Never `compile()` untrusted input without sandboxing—treat it like `exec()`.

  ```python
  source = "1 + 2"
  code = compile(source, "<trusted>", "eval")
  assert eval(code) == 3
  # Never: compile(user_input, "<web>", "exec")
  ```

- Pass a meaningful `filename` (even `"<template>"`) so stack traces are debuggable.

  ```python
  code = compile("raise ValueError('bad')", "my_template.py", "exec")
  assert code.co_filename == "my_template.py"
  try:
      exec(code)
  except ValueError as exc:
      frame = exc.__traceback__.tb_next.tb_frame
      assert frame.f_code.co_filename == "my_template.py"
  ```

- For AST manipulation, prefer `ast.parse()`; use `compile()` when you need executable code objects.

  ```python
  import ast

  tree = ast.parse("x = 1 + 2")
  assert isinstance(tree, ast.Module)
  code = compile(tree, "<ast>", "exec")
  ns = {}
  exec(code, ns)
  assert ns["x"] == 3
  ```
