# [exec()](https://docs.python.org/3/library/functions.html#exec)

## Description

`exec(source, globals=None, locals=None)` executes Python statements from a string or code object. It returns `None`; side effects live in the namespace dicts you pass (or the current scope when omitted).

## What problem it solves

REPLs, plugins, and code generators sometimes run dynamically built statement blocks—not single expressions. `exec()` separates compile (`compile()`) from execution and keeps effects in an explicit namespace when you need isolation.

## Implementation options

### Execute a block of assignments in a fresh namespace

```python
namespace = {}
exec("a = 1; b = a + 2", namespace)
assert namespace["b"] == 3
```

### Compile once, execute many times

```python
code = compile("total += value", "<string>", "exec")
namespace = {"total": 0}
for value in (10, 20, 30):
    namespace["value"] = value
    exec(code, namespace)
assert namespace["total"] == 60
```

### Class-body-like scope with separate globals and locals

```python
globals_ns = {"base": 10}
locals_ns = {}
exec("result = base + 5", globals_ns, locals_ns)
assert locals_ns["result"] == 15
assert "result" not in globals_ns
```

## Best practices

- Treat `exec()` like `eval()`: never run untrusted input; it is not a sandbox.

  ```python
  code = compile("result = 2 + 2", "<trusted>", "exec")
  ns = {}
  exec(code, ns)
  assert ns["result"] == 4
  # Never: exec(user_supplied_code)
  ```

- Pass an explicit namespace dict so side effects stay isolated from your module globals.

  ```python
  ns = {}
  exec("value = 42", ns)
  assert ns["value"] == 42
  assert "value" not in globals()
  ```

- When globals and locals are separate dicts, top-level assignments go to locals—use one dict for both when you need module-like behavior.

  ```python
  g, l = {}, {}
  exec("x = 1", g, l)
  assert l.get("x") == 1
  assert "x" not in g

  ns = {}
  exec("y = 2", ns, ns)
  assert ns["y"] == 2
  ```
