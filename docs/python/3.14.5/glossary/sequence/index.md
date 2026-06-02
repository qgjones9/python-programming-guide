# [sequence](https://docs.python.org/3.14/glossary.html#term-sequence)

An [iterable](../iterable/index.md) which supports efficient element access using integer
indices via the [__getitem__()](https://docs.python.org/3.14/reference/datamodel.html#object.__getitem__) special method and defines a
[__len__()](https://docs.python.org/3.14/reference/datamodel.html#object.__len__) method that returns the length of the sequence.
Some built-in sequence types are [list](https://docs.python.org/3.14/library/stdtypes.html#list), [str](https://docs.python.org/3.14/library/stdtypes.html#str),
[tuple](https://docs.python.org/3.14/library/stdtypes.html#tuple), and [bytes](https://docs.python.org/3.14/library/stdtypes.html#bytes). Note that [dict](https://docs.python.org/3.14/library/stdtypes.html#dict) also
supports `__getitem__()` and `__len__()`, but is considered a
mapping rather than a sequence because the lookups use arbitrary
[hashable](../hashable/index.md) keys rather than integers.

The [collections.abc.Sequence](https://docs.python.org/3.14/library/collections.abc.html#collections.abc.Sequence) abstract base class
defines a much richer interface that goes beyond just
[__getitem__()](https://docs.python.org/3.14/reference/datamodel.html#object.__getitem__) and [__len__()](https://docs.python.org/3.14/reference/datamodel.html#object.__len__), adding
[count()](https://docs.python.org/3.14/library/stdtypes.html#sequence.count), [index()](https://docs.python.org/3.14/library/stdtypes.html#sequence.index),
[__contains__()](https://docs.python.org/3.14/reference/datamodel.html#object.__contains__), and [__reversed__()](https://docs.python.org/3.14/reference/datamodel.html#object.__reversed__).
Types that implement this expanded
interface can be registered explicitly using
[register()](https://docs.python.org/3.14/library/abc.html#abc.ABCMeta.register). For more documentation on sequence
methods generally, see
[Common Sequence Operations](https://docs.python.org/3.14/library/stdtypes.html#typesseq-common).
