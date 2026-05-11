# [Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)

Condensed notes for **§9.7** of [Classes](https://docs.python.org/3/tutorial/classes.html): deriving classes, overriding methods, **`super()`**, and cooperating hierarchies.

```python
class Animal:
    def speak(self) -> str:
        return "…"


class Dog(Animal):
    def speak(self) -> str:
        return "woof"


assert Dog().speak() == "woof"
```

## Sections in this repo

- [Multiple Inheritance](multiple-inheritance/index.md)

Parent: [Classes](../index.md)
