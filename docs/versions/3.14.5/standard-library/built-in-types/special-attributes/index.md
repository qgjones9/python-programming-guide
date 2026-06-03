# [Special Attributes](https://docs.python.org/3/library/stdtypes.html#special-attributes)

The interpreter attaches **read-only metadata attributes** to **definitions**—classes, functions, methods, descriptors, and generator instances. They support introspection, documentation tools, and generic typing. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#special-attributes); this page explains what each attribute means in practice.

!!! note
    Some of these attributes are **not** listed by **`dir()`**, though you can still read them directly.

---

## Role in Python programs

| Attribute | Typical consumer | Question it answers |
|-----------|------------------|-------------------|
| **`__name__`** | Tracebacks, `repr` | What is this object called? |
| **`__qualname__`** | Logging, pickling, debuggers | What is its dotted path (nested scopes)? |
| **`__module__`** | Import machinery, `pydoc` | Which module defined it? |
| **`__doc__`** | `help()`, Sphinx | What is its docstring? |
| **`__type_params__`** | Generic introspection (3.12+) | What type parameters does it declare? |

These attributes appear on **definition objects**, not necessarily on every **instance** (instances use **`type(obj).__name__`**, etc.).

---

## Special attributes (reference)

| Attribute | On | Meaning |
|-----------|-----|---------|
| [`__name__`](#definition__name__) | Class, function, method, descriptor, generator | Short name |
| [`__qualname__`](#definition__qualname__) | Same (3.3+) | Qualified name with nesting |
| [`__module__`](#definition__module__) | Class, function | Defining module name |
| [`__doc__`](#definition__doc__) | Class, function | Docstring or `None` |
| [`__type_params__`](#definition__type_params__) | Generic class, function, type alias (3.12+) | Declared type parameters |

---

<a id="definition__name__"></a>

### `definition.__name__`

The **short name** of the class, function, method, descriptor, or generator instance.

```python
def greet(name):
    return f'hello, {name}'

assert greet.__name__ == 'greet'
assert type(greet).__name__ == 'function'
```

---

<a id="definition__qualname__"></a>

### `definition.__qualname__`

The **qualified name**—dotted path reflecting lexical nesting (classes inside classes, methods, nested functions).

```python
class Outer:
    class Inner:
        pass

    def method(self):
        pass

assert Outer.__qualname__ == 'Outer'
assert Outer.Inner.__qualname__ == 'Outer.Inner'
assert Outer.method.__qualname__ == 'Outer.method'
```

> **Added in version 3.3.**

---

<a id="definition__module__"></a>

### `definition.__module__`

The **`__name__`** of the module in which the class or function was **defined** (for example `'json'`). Code run as **`python script.py`** often sets top-level definitions to **`'__main__'`** instead of the file’s import name.

```python
import json

assert json.dumps.__module__ == 'json'
# Top-level functions in an imported module use that module's __name__.
```

---

<a id="definition__doc__"></a>

### `definition.__doc__`

The **documentation string** from the first literal after the definition, or **`None`** if omitted. Instance docstrings live on the **class** unless overridden per instance (unusual).

```python
def greet(name):
    return f'hello, {name}'

def documented():
    """Explain behavior here."""
    pass

assert documented.__doc__ == 'Explain behavior here.'
assert greet.__doc__ is None
```

Tools such as **`help()`** and **`pydoc`** read **`__doc__`** (and may fall back to **`__module__`** / **`__qualname__`** for location).

---

<a id="definition__type_params__"></a>

### `definition.__type_params__`

A tuple of **type parameters** for **generic** classes, functions, and type aliases ([PEP 695](https://peps.python.org/pep-0695/) syntax and **`typing`** generics). Non-generic definitions expose an **empty tuple**.

```python
def greet(name):
    return f'hello, {name}'

def identity[T](x: T) -> T:
    return x

assert identity.__type_params__ == (identity.__type_params__[0],)
assert len(identity.__type_params__) == 1
assert greet.__type_params__ == ()
assert identity('hi') == 'hi'
```

> **Added in version 3.12.**

See also [Type Annotation Types — Generic Alias, Union](../type-annotation-types-generic-alias-union/index.md) for runtime generic aliases.

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Other Built-in Types](../other-built-in-types/index.md) | Functions, methods, and modules that carry these attributes. |
| [Type Annotation Types — Generic Alias, Union](../type-annotation-types-generic-alias-union/index.md) | `list[int]`, `X \| Y`, and **`__type_params__`** on generic definitions. |
| [Built-in Types](../index.md) | Overview of all standard interpreter types. |

**See also:** [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function) · [Class definitions](https://docs.python.org/3/reference/compound_stmts.html#class) · [`typing` — Generics](https://docs.python.org/3/library/typing.html#generics)
