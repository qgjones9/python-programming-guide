# [C API Stability](https://docs.python.org/3/c-api/stable.html)

Local notes aligned with [**C API Stability**](https://docs.python.org/3/c-api/stable.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Unstable C API](https://docs.python.org/3/c-api/stable.html#unstable-c-api)

- Official docs: [Unstable C API](https://docs.python.org/3/c-api/stable.html#unstable-c-api) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

/* Reference borrowing vs new refs: borrowed pointers stay alive only while outer
 * invariants guarantee the owner is not mutated; call Py_INCREF if you stash them. */
PyObject *borrowed = PyTuple_GET_ITEM(tuple_arg, 0);  /* borrowed from tuple */
Py_INCREF(borrowed);
/* ... stash borrowed where needed ... */
Py_DECREF(borrowed);
```

### [Stable Application Binary Interface](https://docs.python.org/3/c-api/stable.html#stable-application-binary-interface)

- Official docs: [Stable Application Binary Interface](https://docs.python.org/3/c-api/stable.html#stable-application-binary-interface) — behaviors, return values, and error conventions.
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

### [Platform Considerations](https://docs.python.org/3/c-api/stable.html#platform-considerations)

- Official docs: [Platform Considerations](https://docs.python.org/3/c-api/stable.html#platform-considerations) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// Memory layers: prefer PyMem_Raw*/PyMem_* as documented for the lifetime you own;
// never mix allocators on the same pointer.
void *buf = PyMem_Malloc(64);
if (buf == NULL) {
    return PyErr_NoMemory();
}
PyMem_Free(buf);
```

### [Contents of Limited API](https://docs.python.org/3/c-api/stable.html#contents-of-limited-api)

- Official docs: [Contents of Limited API](https://docs.python.org/3/c-api/stable.html#contents-of-limited-api) — behaviors, return values, and error conventions.
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

## Sections in this repo

- [Unstable C API](unstable-c-api/index.md)
- [Stable Application Binary Interface](stable-application-binary-interface/index.md)
- [Platform Considerations](platform-considerations/index.md)
- [Contents of Limited API](contents-of-limited-api/index.md)
