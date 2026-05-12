# [Initializing and finalizing the interpreter](https://docs.python.org/3/c-api/interp-lifecycle.html#initializing-and-finalizing-the-interpreter)

Local notes on **Initializing and finalizing the interpreter**, part of [*Interpreter initialization and finalization*](https://docs.python.org/3/c-api/interp-lifecycle.html). This page summarizes patterns; authoritative text stays upstream.

- Follow the **[official section](https://docs.python.org/3/c-api/interp-lifecycle.html#initializing-and-finalizing-the-interpreter)** for exact signatures, deprecation notes, and edge cases.
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

Parent: [Interpreter initialization and finalization](../index.md)
