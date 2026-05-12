# [Interpreter initialization and finalization](https://docs.python.org/3/c-api/interp-lifecycle.html)

Local notes aligned with [**Interpreter initialization and finalization**](https://docs.python.org/3/c-api/interp-lifecycle.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Before Python initialization](https://docs.python.org/3/c-api/interp-lifecycle.html#before-python-initialization)

- Official docs: [Before Python initialization](https://docs.python.org/3/c-api/interp-lifecycle.html#before-python-initialization) — behaviors, return values, and error conventions.
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

### [Global configuration variables](https://docs.python.org/3/c-api/interp-lifecycle.html#global-configuration-variables)

- Official docs: [Global configuration variables](https://docs.python.org/3/c-api/interp-lifecycle.html#global-configuration-variables) — behaviors, return values, and error conventions.
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

### [Initializing and finalizing the interpreter](https://docs.python.org/3/c-api/interp-lifecycle.html#initializing-and-finalizing-the-interpreter)

- Official docs: [Initializing and finalizing the interpreter](https://docs.python.org/3/c-api/interp-lifecycle.html#initializing-and-finalizing-the-interpreter) — behaviors, return values, and error conventions.
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

### [Cautions regarding runtime finalization](https://docs.python.org/3/c-api/interp-lifecycle.html#cautions-regarding-runtime-finalization)

- Official docs: [Cautions regarding runtime finalization](https://docs.python.org/3/c-api/interp-lifecycle.html#cautions-regarding-runtime-finalization) — behaviors, return values, and error conventions.
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

### [Process-wide parameters](https://docs.python.org/3/c-api/interp-lifecycle.html#process-wide-parameters)

- Official docs: [Process-wide parameters](https://docs.python.org/3/c-api/interp-lifecycle.html#process-wide-parameters) — behaviors, return values, and error conventions.
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

## Sections in this repo

- [Before Python initialization](before-python-initialization/index.md)
- [Global configuration variables](global-configuration-variables/index.md)
- [Initializing and finalizing the interpreter](initializing-and-finalizing-the-interpreter/index.md)
- [Cautions regarding runtime finalization](cautions-regarding-runtime-finalization/index.md)
- [Process-wide parameters](process-wide-parameters/index.md)
