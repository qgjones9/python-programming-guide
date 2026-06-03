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

## Best practices

- Never `compile()` untrusted input without sandboxing—treat it like `exec()`.
- Pass a meaningful `filename` (even `"<template>"`) so stack traces are debuggable.
- For AST manipulation, prefer `ast.parse()`; use `compile()` when you need executable code objects.
- In `'single'` or `'eval'` mode, multi-line input must end with a newline.
