# [Object Implementation Support](https://docs.python.org/3/c-api/objimpl.html)

Local notes aligned with [**Object Implementation Support**](https://docs.python.org/3/c-api/objimpl.html) in the [Python/C API reference](https://docs.python.org/3/c-api/index.html). For full signatures, ownership rules, and thread-safety text, follow the official links below.

### [Allocating objects on the heap](https://docs.python.org/3/c-api/allocation.html)

- Official docs: [Allocating objects on the heap](https://docs.python.org/3/c-api/allocation.html) — behaviors, return values, and error conventions.
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

### [Object Life Cycle](https://docs.python.org/3/c-api/lifecycle.html)

- Official docs: [Object Life Cycle](https://docs.python.org/3/c-api/lifecycle.html) — behaviors, return values, and error conventions.
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

### [Common Object Structures](https://docs.python.org/3/c-api/structures.html)

- Official docs: [Common Object Structures](https://docs.python.org/3/c-api/structures.html) — behaviors, return values, and error conventions.
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

### [Type Object Structures](https://docs.python.org/3/c-api/typeobj.html)

- Official docs: [Type Object Structures](https://docs.python.org/3/c-api/typeobj.html) — behaviors, return values, and error conventions.
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

### [Supporting Cyclic Garbage Collection](https://docs.python.org/3/c-api/gcsupport.html)

- Official docs: [Supporting Cyclic Garbage Collection](https://docs.python.org/3/c-api/gcsupport.html) — behaviors, return values, and error conventions.
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

- [Allocating objects on the heap](allocating-objects-on-the-heap/index.md)
- [Object Life Cycle](object-life-cycle/index.md)
- [Common Object Structures](common-object-structures/index.md)
- [Type Object Structures](type-object-structures/index.md)
- [Supporting Cyclic Garbage Collection](supporting-cyclic-garbage-collection/index.md)
