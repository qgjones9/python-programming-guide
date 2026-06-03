# [isinstance()](https://docs.python.org/3/library/functions.html#isinstance)

## Description

`isinstance(object, classinfo)` tests whether `object` is an instance of `classinfo`, or of a direct, indirect, or virtual subclass. `classinfo` may be a type, a tuple of types, or a union type.

## What problem it solves

Runtime type checks that respect inheritance—validating API inputs, branching on supported types, or guarding conversions without brittle `type(x) is T` comparisons.

## Implementation options

### Check a single type

```python
assert isinstance(42, int)
assert isinstance("hi", str)
assert not isinstance(3.14, int)
```

### Accept several types with a tuple

```python
def stringify(value):
    if not isinstance(value, (str, int, float)):
        raise TypeError("expected str, int, or float")
    return str(value)

assert stringify(99) == "99"
assert stringify(3.5) == "3.5"
```

### Subclasses match the base type

```python
class AdminUser:
    pass

user = AdminUser()
assert isinstance(user, AdminUser)
assert isinstance(user, object)
```

## Best practices

- Prefer `isinstance()` over `type(x) is T` when subclasses should be accepted.
- Avoid excessive isinstance chains—consider duck typing or a single protocol check.
- Use union types or tuples for “one of several types” rather than nested if/else.
