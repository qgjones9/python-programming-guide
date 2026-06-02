# [Thread states and the global interpreter lock](https://docs.python.org/3/c-api/threads.html)

Local notes aligned with [**Thread states and the global interpreter lock**](https://docs.python.org/3/c-api/threads.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Detaching the thread state from extension code](https://docs.python.org/3/c-api/threads.html#detaching-the-thread-state-from-extension-code)

- Official docs: [Detaching the thread state from extension code](https://docs.python.org/3/c-api/threads.html#detaching-the-thread-state-from-extension-code) — behaviors, return values, and error conventions.
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

### [Non-Python created threads](https://docs.python.org/3/c-api/threads.html#non-python-created-threads)

- Official docs: [Non-Python created threads](https://docs.python.org/3/c-api/threads.html#non-python-created-threads) — behaviors, return values, and error conventions.
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

### [Legacy API](https://docs.python.org/3/c-api/threads.html#legacy-api)

- Official docs: [Legacy API](https://docs.python.org/3/c-api/threads.html#legacy-api) — behaviors, return values, and error conventions.
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

### [Cautions about fork()](https://docs.python.org/3/c-api/threads.html#cautions-about-fork)

- Official docs: [Cautions about fork()](https://docs.python.org/3/c-api/threads.html#cautions-about-fork) — behaviors, return values, and error conventions.
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

### [High-level APIs](https://docs.python.org/3/c-api/threads.html#high-level-apis)

- Official docs: [High-level APIs](https://docs.python.org/3/c-api/threads.html#high-level-apis) — behaviors, return values, and error conventions.
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

### [GIL-state APIs](https://docs.python.org/3/c-api/threads.html#gil-state-apis)

- Official docs: [GIL-state APIs](https://docs.python.org/3/c-api/threads.html#gil-state-apis) — behaviors, return values, and error conventions.
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

### [Low-level APIs](https://docs.python.org/3/c-api/threads.html#low-level-apis)

- Official docs: [Low-level APIs](https://docs.python.org/3/c-api/threads.html#low-level-apis) — behaviors, return values, and error conventions.
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

## Sections in this repo

- [Detaching the thread state from extension code](detaching-the-thread-state-from-extension-code/index.md)
- [Non-Python created threads](non-python-created-threads/index.md)
- [Legacy API](legacy-api/index.md)
- [Cautions about fork()](cautions-about-fork/index.md)
- [High-level APIs](high-level-apis/index.md)
- [GIL-state APIs](gil-state-apis/index.md)
- [Low-level APIs](low-level-apis/index.md)
