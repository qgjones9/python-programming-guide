# [Memory Management](https://docs.python.org/3/c-api/memory.html)

Local notes aligned with [**Memory Management**](https://docs.python.org/3/c-api/memory.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Overview](https://docs.python.org/3/c-api/memory.html#overview)

- Official docs: [Overview](https://docs.python.org/3/c-api/memory.html#overview) — behaviors, return values, and error conventions.
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

### [Allocator Domains](https://docs.python.org/3/c-api/memory.html#allocator-domains)

- Official docs: [Allocator Domains](https://docs.python.org/3/c-api/memory.html#allocator-domains) — behaviors, return values, and error conventions.
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

### [Raw Memory Interface](https://docs.python.org/3/c-api/memory.html#raw-memory-interface)

- Official docs: [Raw Memory Interface](https://docs.python.org/3/c-api/memory.html#raw-memory-interface) — behaviors, return values, and error conventions.
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

### [Memory Interface](https://docs.python.org/3/c-api/memory.html#memory-interface)

- Official docs: [Memory Interface](https://docs.python.org/3/c-api/memory.html#memory-interface) — behaviors, return values, and error conventions.
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

### [Object allocators](https://docs.python.org/3/c-api/memory.html#object-allocators)

- Official docs: [Object allocators](https://docs.python.org/3/c-api/memory.html#object-allocators) — behaviors, return values, and error conventions.
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

### [Default Memory Allocators](https://docs.python.org/3/c-api/memory.html#default-memory-allocators)

- Official docs: [Default Memory Allocators](https://docs.python.org/3/c-api/memory.html#default-memory-allocators) — behaviors, return values, and error conventions.
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

### [Customize Memory Allocators](https://docs.python.org/3/c-api/memory.html#customize-memory-allocators)

- Official docs: [Customize Memory Allocators](https://docs.python.org/3/c-api/memory.html#customize-memory-allocators) — behaviors, return values, and error conventions.
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

### [Debug hooks on the Python memory allocators](https://docs.python.org/3/c-api/memory.html#debug-hooks-on-the-python-memory-allocators)

- Official docs: [Debug hooks on the Python memory allocators](https://docs.python.org/3/c-api/memory.html#debug-hooks-on-the-python-memory-allocators) — behaviors, return values, and error conventions.
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

### [The pymalloc allocator](https://docs.python.org/3/c-api/memory.html#the-pymalloc-allocator)

- Official docs: [The pymalloc allocator](https://docs.python.org/3/c-api/memory.html#the-pymalloc-allocator) — behaviors, return values, and error conventions.
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

### [The mimalloc allocator](https://docs.python.org/3/c-api/memory.html#the-mimalloc-allocator)

- Official docs: [The mimalloc allocator](https://docs.python.org/3/c-api/memory.html#the-mimalloc-allocator) — behaviors, return values, and error conventions.
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

### [tracemalloc C API](https://docs.python.org/3/c-api/memory.html#tracemalloc-c-api)

- Official docs: [tracemalloc C API](https://docs.python.org/3/c-api/memory.html#tracemalloc-c-api) — behaviors, return values, and error conventions.
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

### [Examples](https://docs.python.org/3/c-api/memory.html#examples)

- Official docs: [Examples](https://docs.python.org/3/c-api/memory.html#examples) — behaviors, return values, and error conventions.
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

- [Overview](overview/index.md)
- [Allocator Domains](allocator-domains/index.md)
- [Raw Memory Interface](raw-memory-interface/index.md)
- [Memory Interface](memory-interface/index.md)
- [Object allocators](object-allocators/index.md)
- [Default Memory Allocators](default-memory-allocators/index.md)
- [Customize Memory Allocators](customize-memory-allocators/index.md)
- [Debug hooks on the Python memory allocators](debug-hooks-on-the-python-memory-allocators/index.md)
- [The pymalloc allocator](the-pymalloc-allocator/index.md)
- [The mimalloc allocator](the-mimalloc-allocator/index.md)
- [tracemalloc C API](tracemalloc-c-api/index.md)
- [Examples](examples/index.md)
