# [iterable](https://docs.python.org/3.14/glossary.html#term-iterable)

An object capable of returning its members one at a time. Examples of
iterables include all sequence types (such as [list](https://docs.python.org/3.14/library/stdtypes.html#list), [str](https://docs.python.org/3.14/library/stdtypes.html#str),
and [tuple](https://docs.python.org/3.14/library/stdtypes.html#tuple)) and some non-sequence types like [dict](https://docs.python.org/3.14/library/stdtypes.html#dict),
[file objects](../file-object/index.md), and objects of any classes you define
with an [__iter__()](https://docs.python.org/3.14/reference/datamodel.html#object.__iter__) method or with a
[__getitem__()](https://docs.python.org/3.14/reference/datamodel.html#object.__getitem__) method
that implements [sequence](../sequence/index.md) semantics.

Iterables can be
used in a [for](https://docs.python.org/3.14/reference/compound_stmts.html#for) loop and in many other places where a sequence is
needed ([zip()](https://docs.python.org/3.14/library/functions.html#zip), [map()](https://docs.python.org/3.14/library/functions.html#map), …).  When an iterable object is passed
as an argument to the built-in function [iter()](https://docs.python.org/3.14/library/functions.html#iter), it returns an
iterator for the object.  This iterator is good for one pass over the set
of values.  When using iterables, it is usually not necessary to call
`iter()` or deal with iterator objects yourself.  The `for`
statement does that automatically for you, creating a temporary unnamed
variable to hold the iterator for the duration of the loop.  See also
[iterator](../iterator/index.md), [sequence](../sequence/index.md), and [generator](../generator/index.md).
