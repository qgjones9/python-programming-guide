# [vars()](https://docs.python.org/3/library/functions.html#vars)

## Description

`vars([object])` returns the `__dict__` attribute for objects that have one. Called with no arguments, it behaves like `locals()`. Classes expose a mapping proxy; instances usually have a mutable dict.

## What problem it solves

Inspecting or bulk-updating an object's attribute namespace—debugging, simple serializers, or copying configuration fields without listing every name manually.

## Implementation options

### Read an instance namespace

```python
class Profile:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Profile("Ada", 36)
assert vars(p) == {"name": "Ada", "age": 36}
```

### Bulk-update from a mapping

```python
class Settings:
    theme = "light"
    page_size = 25

s = Settings()
vars(s).update({"theme": "dark", "page_size": 50})
assert s.theme == "dark" and s.page_size == 50
```

### Inspect a module-like object's dict

```python
class Box:
    pass

box = Box()
box.item = "key"
assert "item" in vars(box)
```

## Best practices

- Objects with `__slots__` and no `__dict__` raise `TypeError`—use `getattr`/`dir` or slot-aware logic.
- Treat `vars()` without arguments like `locals()`—snapshot semantics differ; do not rely on it for persistence.
- Prefer explicit attributes in application code; use `vars()` mainly for introspection and generic utilities.
