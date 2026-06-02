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

- Use `issubclass` on classes, `isinstance` on instances—do not mix them up.
- Remember every class is a subclass of `object` unless you are using old-style patterns.
- For structural typing, consider `typing.Protocol` instead of inheritance checks alone.
