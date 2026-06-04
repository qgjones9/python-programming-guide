# [3. Data model](https://docs.python.org/3/reference/datamodel.html)

The data model chapter defines what Python programs manipulate at runtime: **objects** with **identity**, **type**, and **value**. Everything in a program—including code—is represented by objects or relations between them. Types determine which operations are legal; special method names wire those operations to class definitions. This folder is a teaching mirror; normative wording and the full type hierarchy live on [docs.python.org](https://docs.python.org/3/reference/datamodel.html).

| Section | What it covers |
|---------|----------------|
| [Objects, values and types](objects-values-and-types/index.md) | Identity (`is`, `id`), type (`type()`), mutability, containers, and garbage collection. |
| [The standard type hierarchy](the-standard-type-hierarchy/index.md) | Built-in types: numbers, sequences, sets, mappings, callables, modules, classes, and internal types. |
| [Special method names](special-method-names/index.md) | Dunder methods that implement operators, protocols, and attribute access. |
| [Coroutines](coroutines/index.md) | Awaitable objects, coroutine objects, async iterators, and async context managers. |

## How the pieces fit together

1. **Objects** are the atoms: each has immutable identity and type, and a value that may or may not change.
2. **Built-in types** form a hierarchy documented in §3.2; extension modules may add more.
3. **User-defined classes** participate in the same model by implementing **special methods** (§3.3)—for example `__getitem__` for `x[i]` or `__add__` for `+`.
4. **`async def`** coroutines and related protocols (§3.4) extend the model with **awaitable** objects and asynchronous iteration/context management.

When behavior seems ambiguous, the language reference wins over tutorial intuition. For day-to-day API details, cross-check [The Python Standard Library](../../standard-library/index.md).

```python
# Every name binds to an object; type() and id() expose the data-model view.
x = [1, 2]
assert type(x) is list
assert id(x) == id(x)  # identity is stable for the object's lifetime
```

## Sections in this repo

| Section | Path |
|---------|------|
| [3.1. Objects, values and types](objects-values-and-types/index.md) | `objects-values-and-types/index.md` |
| [3.2. The standard type hierarchy](the-standard-type-hierarchy/index.md) | `the-standard-type-hierarchy/index.md` |
| [3.3. Special method names](special-method-names/index.md) | `special-method-names/index.md` |
| [3.4. Coroutines](coroutines/index.md) | `coroutines/index.md` |
