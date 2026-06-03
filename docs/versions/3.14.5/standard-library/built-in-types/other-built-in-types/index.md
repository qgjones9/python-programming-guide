# [Other Built-in Types](https://docs.python.org/3/library/stdtypes.html#other-built-in-types)

Beyond numbers, sequences, mappings, and sets, the interpreter exposes several **other object kinds**—modules, callables, code objects, type objects, and a few **singleton** sentinels. Most support only one or two operations. Full specification remains on [docs.python.org](https://docs.python.org/3/library/stdtypes.html#other-built-in-types); this page summarizes how they appear in everyday code.

---

## Overview

| Kind | Primary operation | Typical example |
|------|-------------------|-----------------|
| [Module](#modules) | Attribute access `m.name` | `import sys; sys.version` |
| [Function](#functions) | Call `func(...)` | `def f(): ...` |
| [Method](#methods) | Call via attribute | `lst.append(x)` |
| [Code object](#code-objects) | Pass to `exec()` / `eval()` | `fn.__code__` |
| [Type object](#type-objects) | Introspection via `type()` | `<class 'int'>` |
| [Singletons](#singleton-objects) | Identity / protocol hooks | `None`, `...`, `NotImplemented` |

**Classes and class instances** are covered in the [Language Reference — Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types) and [Class definitions](https://docs.python.org/3/reference/compound_stmts.html#class). **Internal objects** (frames, tracebacks, slices) are described in [The standard type hierarchy](https://docs.python.org/3/c-api/typeobj.html#the-standard-type-hierarchy).

---

## [Modules](https://docs.python.org/3/library/stdtypes.html#modules)

<a id="modules"></a>

The main operation on a **module** is **attribute access**: `m.name` reads or writes names in the module’s symbol table.

!!! note
    **`import foo`** is not an operation on an existing module object—it loads (or finds) a module definition. Attribute access happens **after** import.

Every module has **`__dict__`**, the mapping backing its namespace. You may mutate **`m.__dict__['a'] = 1`** (which defines **`m.a`**) but **cannot** assign **`m.__dict__ = {}`**. Direct **`__dict__`** surgery is discouraged.

```python
import sys

assert sys.version_info.major >= 3
assert 'version' in sys.__dict__
sys.__dict__['_scratch'] = 1
assert sys._scratch == 1
del sys.__dict__['_scratch']
```

**`repr()`** forms:

| Origin | Example shape |
|--------|-----------------|
| Built-in | `<module 'sys' (built-in)>` |
| From file | `<module 'os' from '.../os.py'>` |

---

## [Functions](https://docs.python.org/3/library/stdtypes.html#functions)

<a id="functions"></a>

**Function objects** come from **`def`** (or **`lambda`**) and support **calling**: `func(arg, ...)`.

| Flavor | Created by | Object type |
|--------|------------|-------------|
| User-defined | `def`, `lambda` | `types.FunctionType` |
| Built-in | C implementation | `builtin_function_or_method` |

Both are callable the same way at the Python level; implementation differs. See [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function) in the Language Reference.

```python
def greet(name):
    return f'hello, {name}'

assert greet('Ada') == 'hello, Ada'
assert callable(greet)
assert greet.__name__ == 'greet'
```

---

## [Methods](https://docs.python.org/3/library/stdtypes.html#methods)

<a id="methods"></a>

**Methods** are functions invoked with **attribute notation**. Two flavors:

| Flavor | Example | Bound? |
|--------|---------|--------|
| Built-in method | `lst.append` | Varies by type |
| Instance method | `obj.method` | Yes — **`self`** injected |

Accessing a function from a **class namespace** through an **instance** yields a **bound method**. Calling **`m(a, b)`** equals **`m.__func__(m.__self__, a, b)`**.

| Read-only attribute | Meaning |
|---------------------|---------|
| **`m.__self__`** | Instance the method is bound to |
| **`m.__func__`** | Underlying function object |

Method attributes live on **`__func__`**, not on the bound method wrapper—assign on the function if you need custom metadata:

```python
class C:
    def method(self):
        pass

c = C()
try:
    c.method.whoami = 'my name is method'
except AttributeError:
    pass

c.method.__func__.whoami = 'my name is method'
assert c.method.whoami == 'my name is method'
assert c.method.__self__ is c
assert c.method.__func__ is C.method
```

See [Instance methods](https://docs.python.org/3/reference/datamodel.html#instance-methods) in the Language Reference.

---

## [Code objects](https://docs.python.org/3/library/stdtypes.html#code-objects)

<a id="code-objects"></a>

**Code objects** represent **pseudo-compiled** Python bytecode (for example a function body). Unlike a function object, a code object has **no** attached global namespace.

| Source | How to obtain |
|--------|---------------|
| **`compile()`** | `compile(source, '<name>', 'exec')` |
| Function | **`fn.__code__`** |

Accessing **`__code__`** raises an auditing event **`object.__getattr__`**. Pass a code object to **`exec()`** or **`eval()`** instead of a source string. See also the [**`code`**](https://docs.python.org/3/library/code.html) module.

```python
source = 'result = 40 + 2'
code = compile(source, '<demo>', 'exec')
ns = {}
exec(code, ns)
assert ns['result'] == 42

def add(a, b):
    return a + b

assert add.__code__.co_name == 'add'
```

---

## [Type objects](https://docs.python.org/3/library/stdtypes.html#type-objects)

<a id="type-objects"></a>

**Type objects** represent object types. Use the built-in **`type()`** to get an object’s type; types themselves have no special operations beyond normal object behavior. The [**`types`**](https://docs.python.org/3/library/types.html) module names standard built-in types.

```python
assert type(42) is int
assert repr(int) == "<class 'int'>"
assert type(int) is type
```

---

## Singleton objects

<a id="singleton-objects"></a>

Three built-in **singletons** have exactly one instance each. **`type(Singleton)()`** returns the same object.

| Singleton | Literal | Role |
|-----------|---------|------|
| **`None`** | `None` | Implicit return when a function has no `return` |
| **`Ellipsis`** | `Ellipsis` or `...` | Placeholder in annotations, stub bodies, NumPy slicing |
| **`NotImplemented`** | `NotImplemented` | Fallback when a comparison or binary op does not apply |

### `None`

```python
def implicit():
    pass

assert implicit() is None
assert type(None)() is None
```

### `Ellipsis` (`...`)

Common uses:

| Context | Purpose |
|---------|---------|
| Type annotations | “Any remaining parameters/elements” |
| Function body | Stub instead of `pass` |
| NumPy / array APIs | Slice / stride placeholder |

**Not** the same as doctest’s **`ELLIPSIS`**, the interactive **`...`** continuation prompt, or prose “…” in documentation.

```python
def todo(): ...

assert Ellipsis is ...
assert type(Ellipsis)() is Ellipsis

def callback(*args: int, **kwargs: str) -> None:
    pass
```

### `NotImplemented`

Returned when an operation is **not defined** for the operand types—allows another type’s reflected method to run. See [Comparisons](../comparisons/index.md).

```python
class Box:
    def __eq__(self, other):
        return NotImplemented

left = Box()
right = Box()
assert left != right  # NotImplemented -> identity comparison
assert left == left
assert type(NotImplemented)() is NotImplemented
```

---

## [Internal objects](https://docs.python.org/3/library/stdtypes.html#internal-objects)

Stack **frame** objects, **traceback** objects, and **slice** objects are implementation-facing types used by the interpreter and debuggers. See [The standard type hierarchy](https://docs.python.org/3/c-api/typeobj.html#the-standard-type-hierarchy) in the C API manual.

---

## Related topics in this guide

| Subject | Description |
|---------|-------------|
| [Built-in Types](../index.md) | Top-level map of numeric, sequence, mapping, and set types. |
| [Comparisons](../comparisons/index.md) | How `NotImplemented` participates in rich comparisons. |
| [Special Attributes](../special-attributes/index.md) | `__name__`, `__doc__`, `__module__`, and related metadata on definitions. |

**See also:** [`types` — Dynamic type creation](https://docs.python.org/3/library/types.html) · [`code` — Code object utilities](https://docs.python.org/3/library/code.html)
