# [reference count](https://docs.python.org/3.14/glossary.html#term-reference-count)

The number of references to an object.  When the reference count of an
object drops to zero, it is deallocated.  Some objects are
[immortal](../immortal/index.md) and have reference counts that are never modified, and
therefore the objects are never deallocated.  Reference counting is
generally not visible to Python code, but it is a key element of the
[CPython](../CPython/index.md) implementation.  Programmers can call the
[sys.getrefcount()](https://docs.python.org/3.14/library/sys.html#sys.getrefcount) function to return the
reference count for a particular object.

In [CPython](../CPython/index.md), reference counts are not considered to be stable
or well-defined values; the number of references to an object, and how
that number is affected by Python code, may be different between
versions.
