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

### Objects without `__dict__` (`__slots__`)

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x, self.y = x, y

try:
    vars(Point(1, 2))
except TypeError as exc:
    assert "no __dict__" in str(exc).lower() or "__dict__" in str(exc)
```

## Best practices

- Objects with `__slots__` and no `__dict__` raise `TypeError`—use `getattr`/`dir` or slot-aware logic.

  ```python
  class Point:
      __slots__ = ("x", "y")

      def __init__(self, x, y):
          self.x, self.y = x, y

  p = Point(1, 2)
  assert getattr(p, "x") == 1
  assert "x" in dir(p)
  try:
      vars(p)
  except TypeError:
      pass
  else:
      raise AssertionError("vars() requires __dict__")
  ```

- Treat `vars()` without arguments like `locals()`—snapshot semantics differ; do not rely on it for persistence.

  ```python
  def demo():
      local_name = "snapshot"
      snap = vars()
      assert snap["local_name"] == "snapshot"
      return snap

  result = demo()
  assert result["local_name"] == "snapshot"
  ```

- Prefer explicit attributes in application code; use `vars()` mainly for introspection and generic utilities.

  ```python
  class Profile:
      def __init__(self, name):
          self.name = name

  def copy_public_attrs(src, dest, names):
      for key in names:
          setattr(dest, key, getattr(src, key))

  src = Profile("Ada")
  dest = Profile("")
  copy_public_attrs(src, dest, ("name",))
  assert dest.name == "Ada"
  ```
