# [Exception Handling](https://docs.python.org/3/c-api/exceptions.html)

Local notes aligned with [**Exception Handling**](https://docs.python.org/3/c-api/exceptions.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Printing and clearing](https://docs.python.org/3/c-api/exceptions.html#printing-and-clearing)

- Official docs: [Printing and clearing](https://docs.python.org/3/c-api/exceptions.html#printing-and-clearing) — behaviors, return values, and error conventions.
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

### [Raising exceptions](https://docs.python.org/3/c-api/exceptions.html#raising-exceptions)

- Official docs: [Raising exceptions](https://docs.python.org/3/c-api/exceptions.html#raising-exceptions) — behaviors, return values, and error conventions.
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

### [Issuing warnings](https://docs.python.org/3/c-api/exceptions.html#issuing-warnings)

- Official docs: [Issuing warnings](https://docs.python.org/3/c-api/exceptions.html#issuing-warnings) — behaviors, return values, and error conventions.
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

### [Querying the error indicator](https://docs.python.org/3/c-api/exceptions.html#querying-the-error-indicator)

- Official docs: [Querying the error indicator](https://docs.python.org/3/c-api/exceptions.html#querying-the-error-indicator) — behaviors, return values, and error conventions.
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

### [Signal Handling](https://docs.python.org/3/c-api/exceptions.html#signal-handling)

- Official docs: [Signal Handling](https://docs.python.org/3/c-api/exceptions.html#signal-handling) — behaviors, return values, and error conventions.
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

### [Exception Classes](https://docs.python.org/3/c-api/exceptions.html#exception-classes)

- Official docs: [Exception Classes](https://docs.python.org/3/c-api/exceptions.html#exception-classes) — behaviors, return values, and error conventions.
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

### [Exception Objects](https://docs.python.org/3/c-api/exceptions.html#exception-objects)

- Official docs: [Exception Objects](https://docs.python.org/3/c-api/exceptions.html#exception-objects) — behaviors, return values, and error conventions.
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

### [Unicode Exception Objects](https://docs.python.org/3/c-api/exceptions.html#unicode-exception-objects)

- Official docs: [Unicode Exception Objects](https://docs.python.org/3/c-api/exceptions.html#unicode-exception-objects) — behaviors, return values, and error conventions.
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

### [Recursion Control](https://docs.python.org/3/c-api/exceptions.html#recursion-control)

- Official docs: [Recursion Control](https://docs.python.org/3/c-api/exceptions.html#recursion-control) — behaviors, return values, and error conventions.
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

### [Exception and warning types](https://docs.python.org/3/c-api/exceptions.html#exception-and-warning-types)

- Official docs: [Exception and warning types](https://docs.python.org/3/c-api/exceptions.html#exception-and-warning-types) — behaviors, return values, and error conventions.
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

### [Tracebacks](https://docs.python.org/3/c-api/exceptions.html#tracebacks)

- Official docs: [Tracebacks](https://docs.python.org/3/c-api/exceptions.html#tracebacks) — behaviors, return values, and error conventions.
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

## Sections in this repo

- [Printing and clearing](printing-and-clearing/index.md)
- [Raising exceptions](raising-exceptions/index.md)
- [Issuing warnings](issuing-warnings/index.md)
- [Querying the error indicator](querying-the-error-indicator/index.md)
- [Signal Handling](signal-handling/index.md)
- [Exception Classes](exception-classes/index.md)
- [Exception Objects](exception-objects/index.md)
- [Unicode Exception Objects](unicode-exception-objects/index.md)
- [Recursion Control](recursion-control/index.md)
- [Exception and warning types](exception-and-warning-types/index.md)
- [Tracebacks](tracebacks/index.md)
