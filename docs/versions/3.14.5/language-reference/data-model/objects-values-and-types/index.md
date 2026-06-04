# [3.1. Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types)

All data in a Python program is represented by **objects** or relations between objects—even functions, classes, and modules are objects. Each object has three facets the reference treats as fundamental: **identity**, **type**, and **value**. This page distills §3.1; see the [official section](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types) for footnotes and implementation notes.

## Identity, type, and value

| Facet | Meaning | Typical access |
|-------|---------|----------------|
| **Identity** | The object’s address in the abstract model; never changes after creation. | `is`, `id()` |
| **Type** | Which operations the object supports and which values are possible. Immutable after creation. | `type()`, `isinstance()` |
| **Value** | The payload the object represents; may change for **mutable** types. | Contents (`x[i]`, attributes, etc.) |

```python
a = [1]
b = a
assert a is b          # same identity
assert type(a) is list # type is fixed
b.append(2)
assert a == [1, 2]     # value changed through either name
```

## Mutability

| Category | Examples | Value after creation |
|----------|----------|----------------------|
| **Immutable** | `int`, `float`, `str`, `tuple`, `frozenset`, `bytes` | Cannot change in place |
| **Mutable** | `list`, `dict`, `set`, `bytearray` | Can change in place |

Immutability is subtle for **containers**: a `tuple` is immutable, but if it holds a mutable list, mutating that list changes the tuple’s effective value while the tuple object itself remains the same immutable container.

```python
inner = [1]
t = (inner,)
inner.append(2)
assert t == ([1, 2],)  # tuple identity unchanged; nested value changed
```

## Aliasing and identity tests

Multiple names can refer to one object (**aliasing**). Assignment never copies a mutable object—it binds another name to the same identity.

For **immutable** types, implementations *may* reuse one object for equal values (for example small integers), so `a is b` after `a = 1; b = 1` is not guaranteed. For **mutable** types, distinct literals create distinct objects:

```python
c, d = [], []
assert c is not d  # two empty lists are always distinct objects

e = f = []
assert e is f      # one object, two names
```

Prefer `==` for value equality; reserve `is` for singletons (`None`, `True`, `False`) and intentional identity checks.

## Containers

**Containers** hold references to other objects (for example `tuple`, `list`, `dict`). When people speak of a container’s “value,” they usually mean the values of the contained objects, not their identities—except when discussing whether the container itself is mutable.

## Lifetime and resources

Objects are not destroyed explicitly; when unreachable they may be **garbage-collected** (timing is implementation-defined). Objects wrapping external resources (files, sockets) should be **closed** explicitly—`try`/`finally` and `with` are the usual patterns. Do not rely on `__del__` running promptly or at interpreter shutdown.

## Best practices

| Practice | Why |
|----------|-----|
| Use `is` only for `None` and other singletons | Value equality (`==`) is almost always what you want |
| Treat `id()` as a debugging aid | In CPython it is often the address, but that is not portable |
| Close files and similar resources explicitly | GC may delay cleanup indefinitely |
| Remember nested mutability | Immutable containers can still “change” via mutable elements |

Parent: [3. Data model](../index.md)
