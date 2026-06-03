# [borrowed reference](https://docs.python.org/3.14/glossary.html#term-borrowed-reference)

In Python’s C API, a borrowed reference is a reference to an object, where the code using the object does not own the reference. It becomes a dangling pointer if the object is destroyed. For example, a garbage collection can remove the last [strong reference](../strong-reference/index.md) to the object and so destroy it.

Calling [Py_INCREF()](https://docs.python.org/3.14/c-api/refcounting.html#c.Py_INCREF) on the [borrowed reference](../borrowed-reference/index.md) is recommended to convert it to a [strong reference](../strong-reference/index.md) in-place, except when the object cannot be destroyed before the last usage of the borrowed reference. The [Py_NewRef()](https://docs.python.org/3.14/c-api/refcounting.html#c.Py_NewRef) function can be used to create a new strong reference.
