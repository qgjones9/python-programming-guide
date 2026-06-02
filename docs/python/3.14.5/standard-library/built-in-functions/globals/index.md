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

## Best practices

- Inside functions, `globals()` returns the enclosing module's dict, not local variables—use `locals()` for function scope.
- Modifying the dict returned by `globals()` updates real module variables; treat it carefully.
- Avoid relying on `globals()` in everyday code; explicit parameters and return values are clearer.
