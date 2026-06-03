# [C API for extension modules](https://docs.python.org/3/c-api/concrete.html#c-api-for-extension-modules)

Local notes on **C API for extension modules**, part of [*Concrete Objects Layer*](https://docs.python.org/3/c-api/concrete.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/concrete.html#c-api-for-extension-modules)** for exact signatures, deprecation notes, and edge cases.
- Most helpers advertise failures via `NULL` / `-1` and the **error indicator**; treat success paths carefully when references are borrowed vs new.
- Threading semantics are easy to violate in C extensions; skim the threading chapter alongside this section.

```c
#include <Python.h>

// Many C APIs return either a pointer or NULL; NULL means failure and the error
// indicator may be set (check with PyErr_Occurred()). Clear or propagate when appropriate.
PyObject *value = PyLong_FromLong(2026);
if (value == NULL) {
    return NULL;  /* let the interpreter surface the pending exception */
}
Py_DECREF(value);
```

Parent: [Concrete Objects Layer](../index.md)
