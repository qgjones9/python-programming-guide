# [Defining extension modules](https://docs.python.org/3/c-api/extension-modules.html)

Local notes aligned with [**Defining extension modules**](https://docs.python.org/3/c-api/extension-modules.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Multiple module instances](https://docs.python.org/3/c-api/extension-modules.html#multiple-module-instances)

- Official docs: [Multiple module instances](https://docs.python.org/3/c-api/extension-modules.html#multiple-module-instances) — behaviors, return values, and error conventions.
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

### [Initialization function](https://docs.python.org/3/c-api/extension-modules.html#initialization-function)

- Official docs: [Initialization function](https://docs.python.org/3/c-api/extension-modules.html#initialization-function) — behaviors, return values, and error conventions.
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

### [Multi-phase initialization](https://docs.python.org/3/c-api/extension-modules.html#multi-phase-initialization)

- Official docs: [Multi-phase initialization](https://docs.python.org/3/c-api/extension-modules.html#multi-phase-initialization) — behaviors, return values, and error conventions.
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

### [Legacy single-phase initialization](https://docs.python.org/3/c-api/extension-modules.html#legacy-single-phase-initialization)

- Official docs: [Legacy single-phase initialization](https://docs.python.org/3/c-api/extension-modules.html#legacy-single-phase-initialization) — behaviors, return values, and error conventions.
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

- [Multiple module instances](multiple-module-instances/index.md)
- [Initialization function](initialization-function/index.md)
- [Multi-phase initialization](multi-phase-initialization/index.md)
- [Legacy single-phase initialization](legacy-single-phase-initialization/index.md)
