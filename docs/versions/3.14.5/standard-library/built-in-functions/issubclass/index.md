# [issubclass()](https://docs.python.org/3/library/functions.html#issubclass)

## Description

`issubclass(class, classinfo)` returns `True` if `class` is a subclass of `classinfo`. A class is considered a subclass of itself. `classinfo` may be a tuple of classes or a union type.

## What problem it solves

Framework and plugin code needs to verify inheritance relationships—whether a registered class extends a base API, or whether metaclass hooks apply.

## Implementation options

### Direct and indirect inheritance

```python
class Animal:
    pass

class Dog(Animal):
    pass

assert issubclass(Dog, Animal)
assert issubclass(Dog, Dog)
assert not issubclass(Animal, Dog)
```

### Test against several allowed bases

```python
class Serializer:
    pass

class JsonSerializer(Serializer):
    pass

allowed = (Serializer, type(None))
assert issubclass(JsonSerializer, allowed)
```

### Contrast with isinstance on instances

```python
class A:
    pass

class B(A):
    pass

obj = B()
assert isinstance(obj, A)
assert issubclass(B, A)
```

## Best practices

- Use `issubclass` on classes and `isinstance` on instances—do not mix them up.

  ```python
  class Animal:
      pass

  class Dog(Animal):
      pass

  pet = Dog()
  assert isinstance(pet, Animal)
  assert issubclass(Dog, Animal)

  try:
      issubclass(pet, Animal)
  except TypeError:
      pass
  else:
      raise AssertionError("expected TypeError")
  ```

- Remember every new-style class is a subclass of `object`.

  ```python
  class Widget:
      pass

  assert issubclass(Widget, object)
  assert issubclass(Widget, Widget)
  ```

- For structural typing, consider `typing.Protocol` instead of inheritance checks alone.

  ```python
  from typing import Protocol

  class Closeable(Protocol):
      def close(self) -> None: ...

  class FileLike:
      def close(self):
          pass

  def shutdown(resource: Closeable) -> None:
      resource.close()

  shutdown(FileLike())  # structural match, no shared base class required
  ```
