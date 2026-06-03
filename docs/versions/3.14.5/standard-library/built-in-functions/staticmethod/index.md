# [staticmethod()](https://docs.python.org/3/library/functions.html#staticmethod)

## Description

`@staticmethod` (or `staticmethod(function)`) transforms a function into a static method: no implicit first argument is passed. Static methods are useful for namespacing utilities inside a class.

## What problem it solves

A function logically belongs with a class but does not need access to instance or class state—you want it callable as `Class.method()` without creating an instance.

## Implementation options

### Decorator form inside a class

```python
class Math:
    @staticmethod
    def clamp(value, low, high):
        return max(low, min(value, high))

assert Math.clamp(15, 0, 10) == 10
assert Math().clamp(-3, 0, 10) == 0
```

### Assign an existing function

```python
def normalize(text):
    return text.strip().lower()

class Text:
    clean = staticmethod(normalize)

assert Text.clean("  Hello  ") == "hello"
```

### Contrast with instance method (no automatic `self`)

```python
class Demo:
    @staticmethod
    def tags():
        return ("a", "b")

assert Demo.tags() == ("a", "b")
```

## Best practices

- Use `@classmethod` when the method needs the class object (alternate constructors).

  ```python
  class User:
      def __init__(self, name):
          self.name = name

      @classmethod
      def from_email(cls, email):
          name = email.split("@", 1)[0]
          return cls(name)

  assert User.from_email("ada@example.com").name == "ada"
  ```

  ```python
  class Math:
      @staticmethod
      def clamp(value, low, high):
          return max(low, min(value, high))

  # staticmethod does not receive cls—wrong tool for alternate constructors:
  assert Math.clamp(5, 0, 10) == 5
  ```

- Static methods do not participate in overriding the same way instance methods do—design APIs accordingly.

  ```python
  class Base:
      @staticmethod
      def tag():
          return "base"

  class Sub(Base):
      @staticmethod
      def tag():
          return "sub"

  assert Sub.tag() == "sub"  # hides Base.tag, not virtual dispatch
  ```

  ```python
  # Instance methods use the MRO; staticmethods are resolved on the class you call:
  # Sub().tag() still calls Sub.tag, not a cooperative parent chain
  ```

- Keep static methods as pure utilities; reach for module-level functions if the class adds no clarity.

  ```python
  class Text:
      @staticmethod
      def normalize(s):
          return s.strip().lower()

  assert Text.normalize("  Hi  ") == "hi"
  ```

  ```python
  # If the class name adds no namespace value, a module function is simpler:
  # def normalize(s): ...
  ```
