# [setattr()](https://docs.python.org/3/library/functions.html#setattr)

## Description

`setattr(object, name, value)` assigns `value` to the attribute identified by `name` on `object`, when the object allows it. It is the counterpart of `getattr()`.

## What problem it solves

Attribute names are only known at runtime—configuration loaders, serializers, and ORMs need to set fields dynamically without dot notation.

## Implementation options

### Dynamic field from a mapping

```python
class User:
    pass

user = User()
fields = {"username": "ada", "role": "admin"}
for key, val in fields.items():
    setattr(user, key, val)
assert user.username == "ada"
assert user.role == "admin"
```

### Equivalent to dot assignment

```python
class Config:
    pass

cfg = Config()
setattr(cfg, "timeout", 30)
cfg.timeout = 45
assert getattr(cfg, "timeout") == 45
```

### Set a non-identifier attribute name

```python
class Record:
    pass

record = Record()
setattr(record, "field-with-dashes", 99)
assert getattr(record, "field-with-dashes") == 99
```

## Best practices

- Prefer normal dot syntax when the attribute name is a valid identifier known at compile time.
- For private names (`__x`), name mangling happens at class definition time—mangle manually if using `setattr` on instances.
- Validate `name` and `value` in application code; `setattr` will raise if the object rejects the assignment.
