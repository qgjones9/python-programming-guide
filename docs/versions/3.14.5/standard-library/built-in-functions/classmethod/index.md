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

### Registry pattern on the class

```python
class Plugin:
    _registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin._registry[cls.__name__] = cls

    @classmethod
    def create(cls, name, **kwargs):
        return cls._registry[name](**kwargs)

class Echo(Plugin):
    def __init__(self, msg):
        self.msg = msg

obj = Plugin.create("Echo", msg="hi")
assert obj.msg == "hi"
```

## Best practices

- Use `@classmethod` for factory methods; use `@staticmethod` when neither `cls` nor `self` is needed.

  ```python
  class Widget:
      def __init__(self, name):
          self.name = name

      @classmethod
      def from_name(cls, name):
          return cls(name)

      @staticmethod
      def validate(name):
          return bool(name)

  w = Widget.from_name("hi")
  assert w.name == "hi"
  assert Widget.validate("hi")
  ```

- Class methods receive the runtime class, so subclasses get correct polymorphic behavior.

  ```python
  class Base:
      tag = "base"

      @classmethod
      def label(cls):
          return cls.tag

  class Derived(Base):
      tag = "derived"

  assert Derived.label() == "derived"
  ```

- Prefer explicit `cls(...)` construction in factories so subclasses return the correct type.

  ```python
  class Document:
      def __init__(self, title):
          self.title = title

      @classmethod
      def from_slug(cls, slug):
          return cls(slug.replace("-", " ").title())

  class Report(Document):
      pass

  doc = Report.from_slug("q1-summary")
  assert type(doc) is Report
  assert doc.title == "Q1 Summary"
  ```
