# [type()](https://docs.python.org/3/library/functions.html#type)

## Description

With one argument, `type(object)` returns the object's type (usually the same as `object.__class__`). With three arguments, `type(name, bases, dict)` creates a new class object dynamically—like a programmatic `class` statement.

## What problem it solves

Introspection ("what kind of object is this?") and metaprogramming (factory-generated classes, plugins, serializers) without writing a `class` block per variant.

## Implementation options

### Inspect a value's type

```python
assert type(42) is int
assert type("hi") is str
```

### Prefer `isinstance` for type checks with inheritance

```python
class AdminUser:
    pass

user = AdminUser()
assert isinstance(user, AdminUser)
assert type(user) is AdminUser
```

### Build a class at runtime

```python
Dynamic = type("Dynamic", (), {"answer": 42, "greet": lambda self: "hi"})
obj = Dynamic()
assert obj.answer == 42
assert obj.greet() == "hi"
```

## Best practices

- Use `isinstance()` and `issubclass()` for type tests that should respect inheritance.
- Reserve three-argument `type()` for frameworks; normal code should use `class` syntax for readability.
- Remember `type(x) is T` fails for subclasses—`isinstance(x, T)` is usually what you want.
