# [eval()](https://docs.python.org/3/library/functions.html#eval)

## Description

Parses and evaluates a Python expression from a string (or code object) using optional global and local namespaces.

## What problem it solves

Some tools need to interpret small dynamic expressions—calculators, config templates, or DSLs—without writing a full parser.

## Implementation options

### Option 1: Evaluate a simple arithmetic expression

```python
x = 10
result = eval("x * 2 + 5")
assert result == 25
```

### Option 2: Use ast.literal_eval for safe literal parsing

```python
import ast

data = ast.literal_eval("[1, 2, {'a': 3}]")
assert data == [1, 2, {"a": 3}]
```

## Best practices

- Never pass untrusted user input to `eval()`; use `ast.literal_eval()` for strings containing only literals.
- Restrict globals when evaluation is necessary: pass a minimal dict and omit or override `__builtins__`.
- Prefer explicit parsing, JSON, or a proper DSL over `eval()` in application code.
