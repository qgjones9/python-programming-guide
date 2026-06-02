# [Built-in Types](https://docs.python.org/3/library/stdtypes.html)

The sections below walk through the standard types that Python provides out of the box—no import required. These types are built into the interpreter itself, so they are always available in any Python program.

At a high level, built-in types fall into a few main groups: **numerics** (numbers), **sequences** (ordered collections like lists and strings), **mappings** (key–value structures like dictionaries), plus **classes**, **instances**, and **exceptions**. Each group behaves differently, and the linked sections explain those differences in detail.

Some collection types are **mutable**, meaning you can change their contents after creation. When a method adds, removes, or rearranges items *in place*—and does not return a single extracted item—it returns `None`, not the collection itself. That pattern shows up often with lists and dictionaries, so it is worth remembering when chaining method calls.

Many operations work across several object types. Almost every object can be compared for equality, tested in a boolean context (for example, in an `if` statement), and turned into text. Use [`repr()`](../built-in-functions/repr/index.md) when you want a developer-oriented representation, or [`str()`](../built-in-functions/str/index.md) when you want something more readable; [`print()`](../built-in-functions/print/index.md) calls [`str()`](../built-in-functions/str/index.md) for you automatically.




| Module/Link | Description |
|-------------|-------------|
| [Truth Value Testing](truth-value-testing/index.md) | How Python decides whether a value counts as true or false in `if`, `while`, and other boolean contexts. |
| [Boolean Operations — and, or, not](boolean-operations-and-or-not/index.md) | Short-circuit `and`, `or`, and `not`, including operator precedence and return values. |
| [Comparisons](comparisons/index.md) | Equality, ordering, identity (`is` / `is not`), and chained comparisons such as `x < y <= z`. |
| [Numeric Types — int, float, complex](numeric-types-int-float-complex/index.md) | Built-in integers, floats, and complex numbers, literals, and the operations they support. |
| [Boolean Type - bool](boolean-type-bool/index.md) | The `bool` type as a subclass of `int`, with constants `True` and `False`. |
| [Iterator Types](iterator-types/index.md) | Iterator objects from `iter()` and generator expressions, and the iterator protocol. |
| [Sequence Types — list, tuple, range](sequence-types-list-tuple-range/index.md) | Mutable lists, immutable tuples, and the `range` type for arithmetic progressions. |
| [Text and Binary Sequence Type Methods Summary](text-and-binary-sequence-type-methods-summary/index.md) | Methods shared by `str`, `bytes`, and `bytearray` as sequence types. |
| [Text Sequence Type — str](text-sequence-type-str/index.md) | Unicode text strings, formatting, encoding, and string methods. |
| [Binary Sequence Types — bytes, bytearray, memoryview](binary-sequence-types-bytes-bytearray-memoryview/index.md) | Immutable and mutable byte buffers and zero-copy `memoryview` slices. |
| [Set Types — set, frozenset](set-types-set-frozenset/index.md) | Unordered collections of unique hashable elements, mutable and immutable. |
| [Mapping Types — dict](mapping-types-dict/index.md) | Key–value mappings, views, and dict-specific methods and semantics. |
| [Context Manager Types](context-manager-types/index.md) | Objects used with `with` through `__enter__` and `__exit__`. |
| [Type Annotation Types — Generic Alias, Union](type-annotation-types-generic-alias-union/index.md) | Runtime objects behind annotations such as `list[int]` and `Union`. |
| [Other Built-in Types](other-built-in-types/index.md) | Singletons and related types including `None`, `NotImplemented`, and `Ellipsis`. |
| [Special Attributes](special-attributes/index.md) | Attributes present on (nearly) every object, such as `__class__` and `__doc__`. |
| [Integer string conversion length limitation](integer-string-conversion-length-limitation/index.md) | Security limits on converting very large integers to or from decimal strings. |
