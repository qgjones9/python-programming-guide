# [Multiple interpreters in a Python process](https://docs.python.org/3/c-api/subinterpreters.html)

Local notes aligned with [**Multiple interpreters in a Python process**](https://docs.python.org/3/c-api/subinterpreters.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [A per-interpreter GIL](https://docs.python.org/3/c-api/subinterpreters.html#a-per-interpreter-gil)

- Official docs: [A per-interpreter GIL](https://docs.python.org/3/c-api/subinterpreters.html#a-per-interpreter-gil) — behaviors, return values, and error conventions.
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

### [Bugs and caveats](https://docs.python.org/3/c-api/subinterpreters.html#bugs-and-caveats)

- Official docs: [Bugs and caveats](https://docs.python.org/3/c-api/subinterpreters.html#bugs-and-caveats) — behaviors, return values, and error conventions.
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

### [High-level APIs](https://docs.python.org/3/c-api/subinterpreters.html#high-level-apis)

- Official docs: [High-level APIs](https://docs.python.org/3/c-api/subinterpreters.html#high-level-apis) — behaviors, return values, and error conventions.
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

### [Low-level APIs](https://docs.python.org/3/c-api/subinterpreters.html#low-level-apis)

- Official docs: [Low-level APIs](https://docs.python.org/3/c-api/subinterpreters.html#low-level-apis) — behaviors, return values, and error conventions.
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

### [Advanced debugger support](https://docs.python.org/3/c-api/subinterpreters.html#advanced-debugger-support)

- Official docs: [Advanced debugger support](https://docs.python.org/3/c-api/subinterpreters.html#advanced-debugger-support) — behaviors, return values, and error conventions.
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

- [A per-interpreter GIL](a-per-interpreter-gil/index.md)
- [Bugs and caveats](bugs-and-caveats/index.md)
- [High-level APIs](high-level-apis/index.md)
- [Low-level APIs](low-level-apis/index.md)
- [Advanced debugger support](advanced-debugger-support/index.md)
