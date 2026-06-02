# [property()](https://docs.python.org/3/library/functions.html#property)

## Description

`property(fget=None, fset=None, fdel=None, doc=None)` returns a property descriptor. The `@property` decorator builds read-only or read-write attributes that run methods on access, assignment, or deletion.

## What problem it solves

Encapsulation—validate on set, compute on get, deprecate direct attribute access—while keeping a clean `obj.attr` syntax.

## Implementation options

### Read-only computed attribute

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

c = Circle(2)
assert round(c.area, 4) == 12.5664
```

### Getter, setter, and validation

```python
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value

acct = Account(100)
acct.balance = 150
assert acct.balance == 150
```

### Functional property() constructor form

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    def get_c(self):
        return self._celsius

    def set_c(self, value):
        self._celsius = value

    celsius = property(get_c, set_c)

t = Temperature(20)
t.celsius = 25
assert t.celsius == 25
```

## Best practices

- Prefer `@property` decorator syntax over manual `property(get, set)` when methods already exist.
- Keep property methods cheap—heavy work belongs in explicit methods.
- Document managed attributes in the property docstring; it becomes the attribute's help text.
