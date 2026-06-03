# [strong reference](https://docs.python.org/3.14/glossary.html#term-strong-reference)

In Python’s C API, a strong reference is a reference to an object
which is owned by the code holding the reference.  The strong
reference is taken by calling [Py_INCREF()](https://docs.python.org/3.14/c-api/refcounting.html#c.Py_INCREF) when the
reference is created and released with [Py_DECREF()](https://docs.python.org/3.14/c-api/refcounting.html#c.Py_DECREF)
when the reference is deleted.

The [Py_NewRef()](https://docs.python.org/3.14/c-api/refcounting.html#c.Py_NewRef) function can be used to create a strong reference
to an object. Usually, the [Py_DECREF()](https://docs.python.org/3.14/c-api/refcounting.html#c.Py_DECREF) function must be called on
the strong reference before exiting the scope of the strong reference, to
avoid leaking one reference.

See also [borrowed reference](../borrowed-reference/index.md).
