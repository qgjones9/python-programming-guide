# [exec()](https://docs.python.org/3/library/functions.html#exec)

## Description

Dynamically executes Python statements from a string or compiled code object in optional global and local namespaces.

## What problem it solves

Plugins, REPLs, and code-generation tools sometimes need to run dynamically constructed statement blocks rather than single expressions.

## Implementation options

### Option 1: Execute a block of assignments

```python
namespace = {}
exec("a = 1; b = a + 2", namespace)
assert namespace["b"] == 3
```

### Option 2: Compile once, execute many times

```python
code = compile("total += value", "<string>", "exec")
namespace = {"total": 0}
for value in (10, 20, 30):
    namespace["value"] = value
    exec(code, namespace)
assert namespace["total"] == 60
```

## Best practices

- Treat `exec()` like `eval()`: never run untrusted input; it is not a sandbox.
- Pass an explicit namespace dict so side effects stay isolated from your module globals.
- When globals and locals are separate dicts, top-level assignments behave like class-body scope—use one dict for both when you need module-like behavior.
