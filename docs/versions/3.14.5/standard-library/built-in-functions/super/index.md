# [super()](https://docs.python.org/3/library/functions.html#super)

## Description

`super()` returns a proxy object that delegates attribute access according to the method resolution order (MRO). In methods, zero-argument `super()` refers to the enclosing class and the instance (`self`).

## What problem it solves

Cooperative multiple inheritance and overridden methods: call parent implementations without hard-coding base class names, so refactors and diamond hierarchies stay maintainable.

## Implementation options

### Single inheritance: extend parent behavior

```python
class Animal:
    def speak(self):
        return "sound"

class Dog(Animal):
    def speak(self):
        return super().speak() + ": woof"

assert Dog().speak() == "sound: woof"
```

### Cooperative multiple inheritance

```python
class A:
    def task(self):
        return ["A"]

class B(A):
    def task(self):
        return super().task() + ["B"]

class C(A):
    def task(self):
        return super().task() + ["C"]

class D(B, C):
    def task(self):
        return super().task() + ["D"]

assert D().task() == ["A", "C", "B", "D"]
```

### Explicit two-argument form (classmethods)

```python
class Base:
    @classmethod
    def name(cls):
        return "Base"

class Sub(Base):
    @classmethod
    def name(cls):
        return super(Sub, cls).name() + "Sub"

assert Sub.name() == "BaseSub"
```

## Best practices

- Use zero-argument `super()` inside instance and class methods—avoid brittle `super(Class, self)` when possible.
- Zero-argument `super()` does not work inside nested functions or generator expressions.
- Design cooperative methods with compatible signatures so MRO dispatch succeeds at runtime.
