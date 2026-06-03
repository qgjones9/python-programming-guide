# [locals()](https://docs.python.org/3/library/functions.html#locals)

## Description

`locals()` returns a mapping object representing the current local symbol table. At module scope (and in some exec/eval contexts) it may match `globals()`. Behavior in optimized scopes (functions) returns a snapshot whose updates may not write back to local variables.

## What problem it solves

Debugging, templating, and dynamic execution need to inspect or copy the names bound in the current scope.

## Implementation options

### Inspect bindings inside a function

```python
def demo():
    x = 10
    y = "ok"
    return locals()

snap = demo()
assert snap["x"] == 10
assert snap["y"] == "ok"
```

### Format a simple template from local names

```python
def render():
    title = "Report"
    count = 3
    return f"{title}: {count} items"

assert render() == "Report: 3 items"
```

### Read keys from a snapshot

```python
def demo():
    a = 1
    b = 2
    return sorted(locals())

assert demo() == ["a", "b"]
```

## Best practices

- Do not rely on mutating `locals()` to change function variables in optimized scopes (PEP 667).

  ```python
  def demo():
      x = 1
      snap = locals()
      snap["x"] = 99
      return x

  assert demo() == 1  # local x unchanged
  ```

- Prefer explicit parameters and return values over magic locals inspection in production code.

  ```python
  def greet(name: str) -> str:
      return f"Hello, {name}!"

  assert greet("Ada") == "Hello, Ada!"
  ```

- Use `locals()` mainly for debuggers, REPL tooling, and framework introspection.

  ```python
  def debug_snapshot():
      x = 10
      y = "ok"
      return {k: v for k, v in locals().items() if not k.startswith("_")}

  assert debug_snapshot() == {"x": 10, "y": "ok"}
  ```
