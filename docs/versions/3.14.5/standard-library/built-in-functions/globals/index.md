# [globals()](https://docs.python.org/3/library/functions.html#globals)

## Description

Returns the dictionary implementing the current module namespace (global variables visible at the call site).

## What problem it solves

Metaprogramming, debuggers, and dynamic execution sometimes need read access to module-level bindings.

## Implementation options

### Option 1: Inspect module-level names

```python
TEST_VAR = 42

g = globals()
assert "TEST_VAR" in g
assert g["TEST_VAR"] == 42
```

### Option 2: Pass namespace to exec for isolated setup

```python
ns = {"TEST_VAR": 42}
exec("computed = TEST_VAR * 2", ns)
assert ns["computed"] == 84
```

### Option 3: Read `__name__` from the module namespace

```python
g = globals()
assert "__name__" in g
assert isinstance(g["__name__"], str)
```

### Option 4: Share globals between nested exec calls

```python
namespace = {}
exec("x = 1", namespace)
exec("y = x + 1", namespace)
assert namespace["x"] == 1
assert namespace["y"] == 2
```

## Best practices

- Inside functions, `globals()` returns the enclosing module's dict, not local variables—use `locals()` for function scope.

  ```python
  MODULE_FLAG = True

  def demo():
      local_flag = False
      return "local_flag" in globals(), "local_flag" in locals()

  in_globals, in_locals = demo()
  assert in_globals is False
  assert in_locals is True
  assert globals()["MODULE_FLAG"] is True
  ```

- Modifying the dict returned by `globals()` updates real module variables; treat it carefully.

  ```python
  def set_module_counter(value):
      globals()["COUNTER"] = value

  set_module_counter(10)
  assert COUNTER == 10
  ```

- Avoid relying on `globals()` in everyday code; explicit parameters and return values are clearer.

  ```python
  def add(a, b):
      return a + b

  assert add(2, 3) == 5
  ```
