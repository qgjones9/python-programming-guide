# [eval()](https://docs.python.org/3/library/functions.html#eval)

## Description

`eval(expression, globals=None, locals=None)` parses and evaluates a single Python expression from a string or code object. Optional namespace dicts control which names are visible during evaluation.

## What problem it solves

Calculators, tiny DSLs, and config templates sometimes need to interpret dynamic expressions. `eval()` avoids building a full parser—but it runs arbitrary code if misused, so restrict namespaces and prefer safer parsers for untrusted input.

## Implementation options

### Simple arithmetic with variables in scope

```python
x = 10
result = eval("x * 2 + 5")
assert result == 25
```

### Restricted globals (no full builtins)

```python
safe_globals = {"__builtins__": {}}
assert eval("2 + 3", safe_globals) == 5
```

### Prefer `ast.literal_eval` for untrusted literal strings

```python
import ast

data = ast.literal_eval("[1, 2, {'a': 3}]")
assert data == [1, 2, {"a": 3}]
# literal_eval rejects: eval("__import__('os').system('rm -rf /')")
```

## Best practices

- Never pass untrusted user input to `eval()`; use `ast.literal_eval()` for strings containing only literals.

  ```python
  import ast

  safe = ast.literal_eval("[1, 2, {'a': 3}]")
  assert safe == [1, 2, {"a": 3}]
  # ast.literal_eval("__import__('os')")  # ValueError / malformed
  ```

- Restrict globals when evaluation is necessary: pass a minimal dict and omit or override `__builtins__`.

  ```python
  x = 10
  safe_globals = {"__builtins__": {}, "x": x}
  assert eval("x * 2", safe_globals) == 20
  # eval("__import__('os')", safe_globals)  # NameError
  ```

- Prefer explicit parsing, JSON, or a proper DSL over `eval()` in application code.

  ```python
  import json

  config_text = '{"retries": 3}'
  config = json.loads(config_text)
  assert config["retries"] == 3
  # eval(config_text)  # works but invites arbitrary code if input changes
  ```
