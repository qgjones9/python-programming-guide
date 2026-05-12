# [Python Initialization Configuration](https://docs.python.org/3/c-api/init_config.html)

Local notes aligned with [**Python Initialization Configuration**](https://docs.python.org/3/c-api/init_config.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [PyInitConfig C API](https://docs.python.org/3/c-api/init_config.html#pyinitconfig-c-api)

- Official docs: [PyInitConfig C API](https://docs.python.org/3/c-api/init_config.html#pyinitconfig-c-api) — behaviors, return values, and error conventions.
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

### [Configuration Options](https://docs.python.org/3/c-api/init_config.html#configuration-options)

- Official docs: [Configuration Options](https://docs.python.org/3/c-api/init_config.html#configuration-options) — behaviors, return values, and error conventions.
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

### [Runtime Python configuration API](https://docs.python.org/3/c-api/init_config.html#runtime-python-configuration-api)

- Official docs: [Runtime Python configuration API](https://docs.python.org/3/c-api/init_config.html#runtime-python-configuration-api) — behaviors, return values, and error conventions.
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

### [PyConfig C API](https://docs.python.org/3/c-api/init_config.html#pyconfig-c-api)

- Official docs: [PyConfig C API](https://docs.python.org/3/c-api/init_config.html#pyconfig-c-api) — behaviors, return values, and error conventions.
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

### [Py_GetArgcArgv()](https://docs.python.org/3/c-api/init_config.html#py-getargcargv)

- Official docs: [Py_GetArgcArgv()](https://docs.python.org/3/c-api/init_config.html#py-getargcargv) — behaviors, return values, and error conventions.
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

### [Delaying main module execution](https://docs.python.org/3/c-api/init_config.html#delaying-main-module-execution)

- Official docs: [Delaying main module execution](https://docs.python.org/3/c-api/init_config.html#delaying-main-module-execution) — behaviors, return values, and error conventions.
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

- [PyInitConfig C API](pyinitconfig-c-api/index.md)
- [Configuration Options](configuration-options/index.md)
- [Runtime Python configuration API](runtime-python-configuration-api/index.md)
- [PyConfig C API](pyconfig-c-api/index.md)
- [Py_GetArgcArgv()](py-getargcargv/index.md)
- [Delaying main module execution](delaying-main-module-execution/index.md)
