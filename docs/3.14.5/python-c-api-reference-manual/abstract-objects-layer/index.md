# [Abstract Objects Layer](https://docs.python.org/3/c-api/abstract.html)

Local notes aligned with [**Abstract Objects Layer**](https://docs.python.org/3/c-api/abstract.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Object Protocol](https://docs.python.org/3/c-api/object.html)

- Official docs: [Object Protocol](https://docs.python.org/3/c-api/object.html) — behaviors, return values, and error conventions.
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

### [Call Protocol](https://docs.python.org/3/c-api/call.html)

- Official docs: [Call Protocol](https://docs.python.org/3/c-api/call.html) — behaviors, return values, and error conventions.
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

### [Number Protocol](https://docs.python.org/3/c-api/number.html)

- Official docs: [Number Protocol](https://docs.python.org/3/c-api/number.html) — behaviors, return values, and error conventions.
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

### [Sequence Protocol](https://docs.python.org/3/c-api/sequence.html)

- Official docs: [Sequence Protocol](https://docs.python.org/3/c-api/sequence.html) — behaviors, return values, and error conventions.
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

### [Mapping Protocol](https://docs.python.org/3/c-api/mapping.html)

- Official docs: [Mapping Protocol](https://docs.python.org/3/c-api/mapping.html) — behaviors, return values, and error conventions.
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

### [Iterator Protocol](https://docs.python.org/3/c-api/iter.html)

- Official docs: [Iterator Protocol](https://docs.python.org/3/c-api/iter.html) — behaviors, return values, and error conventions.
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

### [Buffer Protocol](https://docs.python.org/3/c-api/buffer.html)

- Official docs: [Buffer Protocol](https://docs.python.org/3/c-api/buffer.html) — behaviors, return values, and error conventions.
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

- [Object Protocol](object-protocol/index.md)
- [Call Protocol](call-protocol/index.md)
- [Number Protocol](number-protocol/index.md)
- [Sequence Protocol](sequence-protocol/index.md)
- [Mapping Protocol](mapping-protocol/index.md)
- [Iterator Protocol](iterator-protocol/index.md)
- [Buffer Protocol](buffer-protocol/index.md)
