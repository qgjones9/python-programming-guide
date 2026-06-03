# [classmethod()](https://docs.python.org/3/library/functions.html#classmethod)

## Description

`classmethod()` transforms a function into a class method that receives the class (`cls`) as its first argument instead of an instance (`self`). Use the `@classmethod` decorator in class bodies.

## What problem it solves

Alternate constructors, shared configuration, and operations that need the class object—not a particular instance—belong on the class itself. Class methods keep that logic colocated with the type while remaining inheritable.

## Implementation options

### Alternate constructor pattern

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])

u = User.from_dict({"name": "Ada", "email": "ada@example.com"})
assert u.name == "Ada" and u.email == "ada@example.com"
```

### Inherited class methods use the derived type

```python
class Base:
    tag = "base"

    @classmethod
    def label(cls):
        return cls.tag

class Derived(Base):
    tag = "derived"

assert Base.label() == "base"
assert Derived.label() == "derived"
```

## Best practices

- Use `@classmethod` for factory methods; use `@staticmethod` when neither `cls` nor `self` is needed.
- Class methods are not C++/Java static methods—they still participate in inheritance and receive the runtime class.
- Prefer explicit `cls(...)` construction in factories so subclasses get the correct type when called on a subclass.
