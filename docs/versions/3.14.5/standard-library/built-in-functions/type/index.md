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

### `type()` vs `isinstance()` with subclasses

```python
class Dog:
    pass

class Puppy(Dog):
    pass

pet = Puppy()
assert isinstance(pet, Dog)
assert type(pet) is Puppy
assert type(pet) is not Dog  # exact type, not ancestry
```

## Best practices

- Use `isinstance()` and `issubclass()` for type tests that should respect inheritance.

  ```python
  class Dog:
      pass

  class Puppy(Dog):
      pass

  pet = Puppy()
  assert isinstance(pet, Dog)
  assert type(pet) is not Dog
  ```

- Reserve three-argument `type()` for frameworks; normal code should use `class` syntax for readability.

  ```python
  Plugin = type("Plugin", (), {"run": lambda self: "ok"})
  assert Plugin().run() == "ok"

  class Greeter:
      def greet(self):
          return "hi"

  assert Greeter().greet() == "hi"
  ```

- Remember `type(x) is T` fails for subclasses—`isinstance(x, T)` is usually what you want.

  ```python
  class AdminUser:
      pass

  user = AdminUser()
  assert isinstance(user, AdminUser)
  assert type(user) is AdminUser
  ```
