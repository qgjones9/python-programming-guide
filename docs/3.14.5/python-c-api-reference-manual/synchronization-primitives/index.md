# [Synchronization primitives](https://docs.python.org/3/c-api/synchronization.html)

Local notes aligned with [**Synchronization primitives**](https://docs.python.org/3/c-api/synchronization.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Python critical section API](https://docs.python.org/3/c-api/synchronization.html#python-critical-section-api)

- Official docs: [Python critical section API](https://docs.python.org/3/c-api/synchronization.html#python-critical-section-api) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

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

### [Legacy locking APIs](https://docs.python.org/3/c-api/synchronization.html#legacy-locking-apis)

- Official docs: [Legacy locking APIs](https://docs.python.org/3/c-api/synchronization.html#legacy-locking-apis) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// Raising in C: use PyErr_SetString / PyErr_Format; return NULL or -1 as documented.
if (arg == NULL) {
    PyErr_SetString(PyExc_TypeError, "argument must not be NULL");
    return NULL;
}
```

## Sections in this repo

- [Python critical section API](python-critical-section-api/index.md)
- [Legacy locking APIs](legacy-locking-apis/index.md)
