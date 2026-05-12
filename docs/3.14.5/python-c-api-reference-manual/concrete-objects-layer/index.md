# [Concrete Objects Layer](https://docs.python.org/3/c-api/concrete.html)

Local notes aligned with [**Concrete Objects Layer**](https://docs.python.org/3/c-api/concrete.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Fundamental Objects](https://docs.python.org/3/c-api/concrete.html#fundamental-objects)

- Official docs: [Fundamental Objects](https://docs.python.org/3/c-api/concrete.html#fundamental-objects) — behaviors, return values, and error conventions.
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

### [Numeric Objects](https://docs.python.org/3/c-api/concrete.html#numeric-objects)

- Official docs: [Numeric Objects](https://docs.python.org/3/c-api/concrete.html#numeric-objects) — behaviors, return values, and error conventions.
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

### [Sequence Objects](https://docs.python.org/3/c-api/concrete.html#sequence-objects)

- Official docs: [Sequence Objects](https://docs.python.org/3/c-api/concrete.html#sequence-objects) — behaviors, return values, and error conventions.
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

### [Container Objects](https://docs.python.org/3/c-api/concrete.html#container-objects)

- Official docs: [Container Objects](https://docs.python.org/3/c-api/concrete.html#container-objects) — behaviors, return values, and error conventions.
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

### [Function Objects](https://docs.python.org/3/c-api/concrete.html#function-objects)

- Official docs: [Function Objects](https://docs.python.org/3/c-api/concrete.html#function-objects) — behaviors, return values, and error conventions.
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

### [Other Objects](https://docs.python.org/3/c-api/concrete.html#other-objects)

- Official docs: [Other Objects](https://docs.python.org/3/c-api/concrete.html#other-objects) — behaviors, return values, and error conventions.
- When calling from C: hold the **GIL** unless the section explicitly documents otherwise; match **borrowed** vs **new** reference semantics.
- Prefer the linked page for exact macro/function availability across Python versions (Limited API / unstable API vary by section).

```c
#include <Python.h>

// When holding the GIL, most object APIs expect the main interpreter state;
// embedding code must bracket calls appropriately (see official section on threads).
PyGILState_STATE gstate = PyGILState_Ensure();
(void)PyRun_SimpleStringFlags("pass\n", NULL);
PyGILState_Release(gstate);
```

### [C API for extension modules](https://docs.python.org/3/c-api/concrete.html#c-api-for-extension-modules)

- Official docs: [C API for extension modules](https://docs.python.org/3/c-api/concrete.html#c-api-for-extension-modules) — behaviors, return values, and error conventions.
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

- [Fundamental Objects](fundamental-objects/index.md)
- [Numeric Objects](numeric-objects/index.md)
- [Sequence Objects](sequence-objects/index.md)
- [Container Objects](container-objects/index.md)
- [Function Objects](function-objects/index.md)
- [Other Objects](other-objects/index.md)
- [C API for extension modules](c-api-for-extension-modules/index.md)
